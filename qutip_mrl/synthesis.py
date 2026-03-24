# synthesis.py
from __future__ import annotations

from typing import Dict, Tuple, Optional, Union, Iterable, Any, List
import logging
import io
import contextlib
from .genetics.genetic_synthesis import synthesize_ops_from_truth_table, ops_to_qudit_circuit, Op
from .qudit_circuit import QuditCircuit

"""
Definition of types for user input and internal processing:
- InKey: A tuple of integers representing the input combination for the truth table.
- OutVal: The output value for a given input, which can be a single integer (for single target) or a 
    tuple of integers (for multiple targets).
- UserMap: A dictionary mapping input combinations (InKey) to their corresponding output values (OutVal) as 
    provided by the user.
- TruthTable: A dictionary mapping complete input combinations (including target qudits initialized to 0) to their 
    expected output combinations, used internally for synthesis. 
"""
InKey = Tuple[int, ...]
OutVal = Union[int, Tuple[int, ...]]
UserMap = Dict[InKey, OutVal]
TruthTable = Dict[Tuple[int, ...], Tuple[int, ...]]

def _as_tuple(v: OutVal, m: int) -> Tuple[int, ...]:
    """
    Convert an output value to a tuple of integers of length m. If m=1, allow single int or single-element tuple.
    :param v: The output value, which can be an int or a tuple of ints
    :param m: The expected length of the output tuple. If m=1, a single int is also accepted.
    :return: A tuple of integers representing the output value, with length m.
    """
    if m == 1:
        return (int(v),) if not isinstance(v, tuple) else (int(v[0]),)
    if not isinstance(v, tuple):
        raise TypeError(f"Expected a tuple of length {m} for outputs.")
    if len(v) != m:
        raise ValueError(f"Output tuple must have length {m}.")
    return tuple(int(x) for x in v)


def _output_indices(*, num_qudits: int, num_targets: int, output_on: str) -> Tuple[int, ...]:
    """
    Determine the indices of the target/output qudits based on the total number of qudits, 
    number of target qudits, and their position (first or last).
    :param num_qudits: Total number of qudits (variables + targets).
    :param num_targets: Number of target/output qudits.
    :param output_on: Position of target qudits, either "last" or "first".
    :return: A tuple of indices indicating the positions of the target qudits.
    """
    if num_targets < 1:
        raise ValueError("num_targets must be >= 1")
    if output_on == "last":
        return tuple(range(num_qudits - num_targets, num_qudits))
    if output_on == "first":
        return tuple(range(0, num_targets))
    raise ValueError("output_on must be 'last' or 'first'")


def _build_truth_table(
    user_map: UserMap,
    *,
    base: int,
    num_variables: int,
    num_targets: int,
    output_on: str,
) -> TruthTable:
    """
    Build a complete truth table from the user-provided mapping of input combinations to output values.
    The function validates the user input, constructs the full input combinations (including target qubits initialized to 0), and maps them to the expected output combinations based on the specified output indices.
    :param user_map: A dictionary mapping input combinations (InKey) to their corresponding output values (OutVal) as provided by the user.
    :param base: The base for the input and output values (e.g., 3 for ternary).
    :param num_variables: The number of input variable qubits.
    :param num_targets: The number of target/output qubits.
    :param output_on: The position of the target qubits, either "last" or "first".
    :return: A complete truth table mapping full input combinations (including targets initialized to 0) to their expected output combinations. 
    """
    num_qudits = num_variables + num_targets
    outs = _output_indices(num_qudits=num_qudits, num_targets=num_targets, output_on=output_on)

    tt: TruthTable = {}
    for x, y in user_map.items():
        if len(x) != num_variables:
            raise ValueError(f"Input key {x} must have length num_variables={num_variables}.")
        for d in x:
            if not (0 <= int(d) < base):
                raise ValueError(f"Input digit {d} outside base={base}.")
        y_tup = _as_tuple(y, num_targets)
        for d in y_tup:
            if not (0 <= int(d) < base):
                raise ValueError(f"Output digit {d} outside base={base}.")

        inp = [int(v) for v in x]
        for _ in range(num_targets):
            inp.append(0)

        exp = inp[:]
        for idx, val in zip(outs, y_tup):
            exp[idx] = int(val)

        tt[tuple(inp)] = tuple(exp)

    return tt


def _ops_to_code(ops: List[Op], *, var_name: str = "qc") -> str:
    """
    Convert a list of operations (gates) into a string of code that can be executed to construct the same circuit. 
    This is useful for users who want to see how to build the synthesized circuit using the QuditCircuit API.
    :param ops: A list of operations (gates) represented as tuples, where the first element is the gate type and the rest are parameters.
    :param var_name: The variable name to use for the QuditCircuit instance in the generated code string. Defaults to "qc".
    :return: A string of code that, when executed, will construct the same circuit using the QuditCircuit API.
    """  
    lines: List[str] = []
    for op in ops:
        if op[0] == "shift":
            _, label, tgt = op
            lines.append(f'{var_name}.shift("{label}", {tgt})')
        elif op[0] == "ms":
            _, label, ctrl, tgt, cvals = op
            lines.append(f'{var_name}.ms("{label}", {ctrl}, {tgt}, {cvals})')
        else:
            raise ValueError(op)
    return "\n".join(lines)


def synth_qc(
    truth_table: UserMap,
    *,
    base: int = 3,
    num_variables: int = 2,
    num_targets: int = 1,
    output_on: str = "last",
    pop_size: int = 100,
    generations: int = 10000,
    restoring: bool = True,
    quiet: bool = True,
    retries: int = 1,
    gate_list: bool = False,
    as_calls: bool = True,
) -> Union[QuditCircuit, Tuple[QuditCircuit, str]]:
    """
    Synthesize a reversible multi-valued circuit from a partial truth table.

    - Total qudits = num_variables + num_targets.
    - Inputs are the 'variable' qudits.
    - Targets are initialized to 0 and must become the desired outputs.
    - Missing input combinations are treated as don't-care (ignored by fitness).

    Parameters:
      base: 3 or 4
      num_variables: number of input variable wires
      num_targets: number of target/output wires (initialized to 0)
      output_on: "last" or "first" (where the target wires are located)
    """
    if base not in (3, 4):
        raise ValueError("Circuit synthesis is supported only for base 3 or 4")

    num_qudits = num_variables + num_targets
    outs = _output_indices(num_qudits=num_qudits, num_targets=num_targets, output_on=output_on)

    if quiet:
        logging.getLogger("jmetal").setLevel(logging.ERROR)

    tt = _build_truth_table(
        truth_table,
        base=base,
        num_variables=num_variables,
        num_targets=num_targets,
        output_on=output_on,
    )

    best_qc: Optional[QuditCircuit] = None
    best_ops: Optional[List[Op]] = None
    best_len = 10**9

    for _ in range(max(1, retries)):
        if quiet:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                ops = synthesize_ops_from_truth_table(
                    tt,
                    base=base,
                    num_qudits=num_qudits,
                    output_indices=outs,
                    pop_size=pop_size,
                    generations=generations,
                    restoring=restoring,
                )
        else:
            ops = synthesize_ops_from_truth_table(
                tt,
                base=base,
                num_qudits=num_qudits,
                output_indices=outs,
                pop_size=pop_size,
                generations=generations,
                restoring=restoring,
            )

        qc = ops_to_qudit_circuit(ops, num_qudits=num_qudits, base=base)

        bad = 0
        for inp, exp in tt.items():
            out = qc.get_output(inp)
            for j in outs:
                if out[j] != exp[j]:
                    bad += 1
                    break

        if bad != 0:
            continue

        if len(ops) < best_len:
            best_len = len(ops)
            best_qc = qc
            best_ops = ops

    if best_qc is None or best_ops is None:
        raise RuntimeError(
            "No perfect circuit found in the given retries. "
            "Increase generations/pop_size/retries."
        )

    if gate_list:
        if as_calls:
            return best_qc, _ops_to_code(best_ops, var_name="qc")
        return best_qc, str(best_ops)

    return best_qc
