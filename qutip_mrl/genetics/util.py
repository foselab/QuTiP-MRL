# util.py
from __future__ import annotations
from .config import QUBASE, NUM_QULINES
from typing import Dict, Tuple, List, Iterable, Optional
import random


CONTROL_VALUE: int = 2   # default control firing value (d-1)
CONTROL_PREFIX: str = "C2Z"
QSG_TABLE: Dict[str, List[int]] = {}
GATE_TYPES: List[str] = []
MERGE_PATTERNS: Dict[Tuple[str, str], str] = {}
Gate = Tuple[int, int, str]


def _gate_table_base3() -> Dict[str, List[int]]:
    """
    List of single-qutrit gates.
    """
    return {
        "+0": [0, 1, 2],
        "+1": [1, 2, 0],
        "+2": [2, 0, 1],
        "01": [1, 0, 2],
        "02": [2, 1, 0],
        "12": [0, 2, 1],
    }


def _gate_table_base4() -> Dict[str, List[int]]:
    """
    List of single-qudit quaternary gates.
    """
    return {
        "+0":  [0, 1, 2, 3],
        "+1":  [1, 0, 3, 2],
        "+2":  [2, 3, 0, 1],
        "+3":  [3, 2, 1, 0],
        "123": [0, 3, 1, 2],
        "013": [3, 0, 2, 1],
        "021": [1, 2, 0, 3],
        "032": [2, 1, 3, 0],
        "132": [0, 2, 3, 1],
        "012": [2, 0, 1, 3],
        "023": [3, 1, 0, 2],
        "031": [1, 3, 2, 0],
        "23":  [0, 1, 3, 2],
        "01":  [1, 0, 2, 3],
        "0213":[3, 2, 0, 1],
        "0312":[2, 3, 1, 0],
        "12":  [0, 2, 1, 3],
        "0132":[2, 0, 3, 1],
        "0231":[1, 3, 0, 2],
        "03":  [3, 1, 2, 0],
        "13":  [0, 3, 2, 1],
        "0123":[3, 0, 1, 2],
        "02":  [2, 1, 0, 3],
        "0321":[1, 2, 3, 0],
    }


def rebuild_tables(*, base: Optional[int] = None, num_qulines: Optional[int] = None) -> None:
    """
    Update all global tables for the selected base and circuit width.
    Must be called before running the GA when base or num_qulines changes.

    Args:
        base: The qudit base (e.g., 3 for qutrits, 4 for ququarts). If None, keeps the current base.
        num_qulines: The number of qudit lines in the circuit. If None, keeps the current number.
    """
    global GATE_TYPES, QSG_TABLE
    
    if base is not None:
        if base not in (3, 4):
            raise ValueError(f"Unsupported base={base}. Only 3 or 4 are supported.")
        QUBASE = int(base)

    if num_qulines is not None:
        if int(num_qulines) < 1:
            raise ValueError("num_qulines must be >= 1")
        NUM_QULINES = int(num_qulines)

    CONTROL_VALUE = QUBASE - 1
    CONTROL_PREFIX = f"C{CONTROL_VALUE}Z"

    if QUBASE == 3:
        QSG_TABLE = _gate_table_base3()
    else:
        QSG_TABLE = _gate_table_base4()

    GATE_TYPES = []
    for k in QSG_TABLE.keys():
        GATE_TYPES.append(f"Z{k}")
        GATE_TYPES.append(f"{CONTROL_PREFIX}{k}")

    MERGE_PATTERNS = _generate_merge_patterns()

def random_gate() -> Gate:
    """
    Generate a random gate based on the current global GATE_TYPES and NUM_QULINES.
    The gate is represented as a tuple (ctrl, tgt, gtype), where:
    - ctrl: the control quline index (for controlled gates) or the target index (for single-qudit gates)
    - tgt: the target quline index (for controlled gates) or the same as ctrl for single-qudit gates
    - gtype: the type of gate, which can be a single-qudit gate (e.g., "Z+1") or a controlled gate (e.g., "C2Z+1")
    """    
    gtype = random.choice(GATE_TYPES)
    if gtype.startswith("C"):
        ctrl = random.randint(0, NUM_QULINES - 1)
        tgt = random.choice([i for i in range(NUM_QULINES) if i != ctrl])
        return (ctrl, tgt, gtype)
    t = random.randint(0, NUM_QULINES - 1)
    return (t, t, gtype)


def apply_gate(state: Tuple[int, ...], gate: Gate) -> Tuple[int, ...]:
    """
    Apply a gate to a given state. The gate is represented as a tuple (ctrl, tgt, gtype), where:
    - ctrl: the control quline index (for controlled gates) or the target index (for single-qudit gates)
    - tgt: the target quline index (for controlled gates) or the same as ctrl for single-qudit gates
    - gtype: the type of gate, which can be a single-qudit gate (e.g., "Z+1") or a controlled gate (e.g., "C2Z+1")

    The function returns the new state after applying the gate. The state is represented as a tuple of integers,
    where each integer corresponds to the value of a quline. The gate is applied according to the rules defined in the 
    QSG_TABLE and CONTROL_VALUE. 

    Args:
        state: A tuple of integers representing the current state of the qulines.
        gate: A tuple (ctrl, tgt, gtype) representing the gate to be applied. 
    Returns:
        A new tuple of integers representing the state after applying the gate.
    """
    ctrl, tgt, gtype = gate
    lines = list(state)

    if gtype.startswith("Z") and not gtype.startswith("C"):
        key = gtype[1:]
        lines[tgt] = QSG_TABLE[key][lines[tgt]]
        return tuple(lines)

    if gtype.startswith(CONTROL_PREFIX):
        key = gtype[len(CONTROL_PREFIX):]
        if lines[ctrl] == CONTROL_VALUE:
            lines[tgt] = QSG_TABLE[key][lines[tgt]]
        return tuple(lines)

    # backward-compat (ternary only, old label)
    if gtype.startswith("C2Z") and QUBASE == 3:
        key = gtype[3:]
        if lines[ctrl] == 2:
            lines[tgt] = QSG_TABLE[key][lines[tgt]]
        return tuple(lines)

    raise ValueError(f"Unsupported gate type: {gtype}")


def simulate_circuit(circuit: List[Gate], input_state: Tuple[int, ...]) -> Tuple[int, ...]:
    """
    Simulate the application of a quantum circuit (a list of gates) on a given input state. The function iteratively 
    applies each gate in the circuit to the state using the apply_gate function, resulting in the final output state 
    after processing through the entire circuit.
    
    Args:
        circuit: A list of gates, where each gate is represented as a tuple (ctrl, tgt, gtype).
        input_state: A tuple of integers representing the initial state of the qulines before applying the circuit.

    Returns:
        A tuple of integers representing the final state of the qulines after applying all gates in the circuit.
    """
    state = input_state
    for gate in circuit:
        state = apply_gate(state, gate)
    return state


def fitness(circuit: List[Gate], truth_table: Dict[Tuple[int, ...], Tuple[int, ...]], *, output_indices: Iterable[int]) -> float:
    """
    Accuracy-only fitness on specified output indices (do not-care: any missing inputs are ignored).
    Returns:
      < 1.0 : accuracy
      >=1.0 : 1 + 1/len(circuit)  (bonus for shorter) when perfect
    """
    correct = 0
    total = 0
    out_idx = tuple(output_indices)

    for inp, expected in truth_table.items():
        total += 1
        out = simulate_circuit(circuit, inp)
        ok = True
        for j in out_idx:
            if out[j] != expected[j]:
                ok = False
                break
        if ok:
            correct += 1

    if total == 0:
        return 0.0

    acc = correct / total
    if acc < 1.0:
        return acc
    return 1.0 + (1.0 / max(1, len(circuit)))

def normalize_gate(g: Gate) -> Gate:
    """
    Normalize a gate to a canonical form for simplification. For single-qudit gates, we normalize to (tgt, tgt, 'Z..').
    """    
    _, tgt, typ = g
    if typ.startswith("Z") and not typ.startswith("C"):
        return (tgt, tgt, typ)
    return g


def normalize_circuit(circ: List[Gate]) -> List[Gate]:
    """
    Normalize all gates in the circuit to a canonical form for simplification. 
    This is a deterministic transformation that ensures that equivalent circuits have the same representation, 
    which is important for the simplification process.
    """
    return [normalize_gate(g) for g in circ]


def _inverse_perm_key(key: str) -> str:
    """
    Given a permutation key (e.g., "+1", "012", "23"), find the key corresponding to its inverse permutation in the QSG_TABLE.
        This is used for determining the inverse of a gate when performing simplification and cancellation in the circuit.
    """    
    table = QSG_TABLE[key]
    inv = [0] * len(table)
    for i, v in enumerate(table):
        inv[v] = i
    for k, v in QSG_TABLE.items():
        if v == inv:
            return k
    raise ValueError(f"Inverse permutation not found for {key}")


def _invert_gate(g: Gate) -> Gate:
    """
    Compute the inverse of a given gate. For single-qudit gates, the inverse is determined by finding the key corresponding 
    to the inverse permutation. For controlled gates, the inverse is similarly determined by finding the key for the 
    inverse permutation while keeping the control and target indices the same.
    """
    ctrl, tgt, gtype = g
    if gtype.startswith("Z") and not gtype.startswith("C"):
        inv_key = _inverse_perm_key(gtype[1:])
        return (tgt, tgt, f"Z{inv_key}")
    if gtype.startswith(CONTROL_PREFIX):
        inv_key = _inverse_perm_key(gtype[len(CONTROL_PREFIX):])
        return (ctrl, tgt, f"{CONTROL_PREFIX}{inv_key}")
    if gtype.startswith("C2Z") and QUBASE == 3:
        inv_key = _inverse_perm_key(gtype[3:])
        return (ctrl, tgt, f"C2Z{inv_key}")
    return g


def _generate_merge_patterns() -> Dict[Tuple[str, str], str]:
    """
    Generate patterns for merging adjacent gates on the same wires. For example, applying "Z+1" followed by "Z+2" 
    on the same target is equivalent to "Z+0". This function computes all such combinations based on the current 
    GATE_TYPES and their corresponding permutations in the QSG_TABLE, resulting in a dictionary that maps pairs 
    of gate types to their merged equivalent.
    """
    patterns: Dict[Tuple[str, str], str] = {}

    # Canonical label selection: prefer "+k" when multiple names map to same permutation.
    perm_to_label: Dict[Tuple[int, ...], str] = {}
    preferred = sorted(QSG_TABLE.items(), key=lambda kv: (0 if kv[0].startswith("+") else 1, kv[0]))
    for k, v in preferred:
        perm_to_label.setdefault(tuple(v), k)

    for k1, v1 in QSG_TABLE.items():
        for k2, v2 in QSG_TABLE.items():
            composed = [v2[i] for i in v1]  # apply k1 then k2
            out = perm_to_label.get(tuple(composed))
            if out is None:
                continue
            patterns[(f"Z{k1}", f"Z{k2}")] = f"Z{out}"
            patterns[(f"{CONTROL_PREFIX}{k1}", f"{CONTROL_PREFIX}{k2}")] = f"{CONTROL_PREFIX}{out}"
            if QUBASE == 3:
                patterns[(f"C2Z{k1}", f"C2Z{k2}")] = f"C2Z{out}"
    return patterns


def simplify_circuit(circ: List[Gate]) -> List[Gate]:
    """
    Deterministic cleanup:
      1) normalize single-wire Z gates to (t,t,'Z..')
      2) repeatedly merge adjacent compatible gates on identical (ctrl,tgt) (Z or controlled) using MERGE_PATTERNS
      3) cancel adjacent inverse pairs on identical (ctrl,tgt) within the same family (Z vs controlled)
      4) drop identity gates (Z+0 / C..+0)
    """
    circ = normalize_circuit(circ)

    def is_identity_gtype(gtype: str) -> bool:
        if gtype.startswith("Z") and not gtype.startswith("C"):
            return gtype[1:] == "+0"
        if gtype.startswith(CONTROL_PREFIX):
            return gtype[len(CONTROL_PREFIX):] == "+0"
        if gtype.startswith("C2Z") and QUBASE == 3:
            return gtype[3:] == "+0"
        return False

    changed = True
    while changed:
        changed = False
        out: List[Gate] = []
        i = 0
        while i < len(circ):
            g = circ[i]

            # identity drop
            if is_identity_gtype(g[2]):
                changed = True
                i += 1
                continue

            # merge runs on same wires
            if i + 1 < len(circ):
                g2 = circ[i + 1]
                if g[:2] == g2[:2]:
                    key = (g[2], g2[2])
                    if key in MERGE_PATTERNS:
                        merged = (g[0], g[1], MERGE_PATTERNS[key])
                        out.append(merged)
                        changed = True
                        i += 2
                        continue

                    # inverse cancel: if g2 == inverse(g)
                    if _invert_gate(g) == g2:
                        changed = True
                        i += 2
                        continue

            out.append(g)
            i += 1

        circ = out

    return circ


def make_restoring_circuit(circ: List[Gate], *, protected_indices: Iterable[int]) -> List[Gate]:
    """
    Compute-uncompute restore: append inverses (reverse order) of gates that touched
    any index NOT in protected_indices. This restores variable wires while preserving targets.
    """
    protected = set(protected_indices)
    base = normalize_circuit(circ)
    head_ops = [g for g in base if g[1] not in protected]
    inv_part = [_invert_gate(g) for g in reversed(head_ops)]
    return base + inv_part

# Initialize defaults
rebuild_tables(base=QUBASE, num_qulines=NUM_QULINES)