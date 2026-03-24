from __future__ import annotations
from typing import Dict, Tuple, List, Optional, Union, Literal, Iterable
from jmetal.operator.selection import BinaryTournamentSelection
from jmetal.util.termination_criterion import TerminationCriterion
from .qudit_circuit import QuditCircuit
from .quantumcircuitproblem import QuantumCircuitProblem
from .safemutation import CircuitMutation
from .circuitcrossover import CircuitCrossover
from .geneticalgorithm import ElitistGeneticAlgorithm
from .util import *
import numpy as np

"""
Definition of types for user input and internal processing:
- Gate: A tuple representing a quantum gate, consisting of a control qudit index, target qudit index, and gate type as a string.
- TruthTable: A dictionary mapping complete input combinations (including target qubits initialized to 0) to their expected output 
    combinations, used internally for synthesis.
- OpShift: A tuple representing a shift operation, consisting of the string "shift", the shift label, and the target qudit index.
- OpMS: A tuple representing a multi-qudit MS operation, consisting of the string "ms", the MS label, control qudit index, target 
    qudit index, and a list of control values that trigger the operation.
- Op: A union type that can be either an OpShift or an OpMS, representing the supported operations in the synthesized circuit.
"""
Gate = Tuple[int, int, str]
TruthTable = Dict[Tuple[int, ...], Tuple[int, ...]]
OpShift = Tuple[Literal["shift"], str, int]
OpMS = Tuple[Literal["ms"], str, int, int, List[int]]
Op = Union[OpShift, OpMS]

class TerminationByEvaluations(TerminationCriterion):
    """
    Termination criterion based on a maximum number of evaluations. The criterion is met when the total number of 
    evaluations performed by the algorithm reaches or exceeds the specified maximum. This is useful for controlling the 
    runtime of the genetic algorithm, especially when the evaluation of solutions is computationally expensive. The class 
    keeps track of the number of evaluations and provides a method to update this count as the algorithm progresses.
    """
    
    def __init__(self, max_evaluations: int):
        super().__init__()
        self.max_evaluations = max_evaluations
        self.evaluations = 0

    @property
    def is_met(self):
        return self.evaluations >= self.max_evaluations

    def update(self, *args, **kwargs):
        self.evaluations = kwargs.get("EVALUATIONS", self.evaluations)


def _get_algorithm_result(algorithm):
    """
    Retrieve the best solution from a jMetal algorithm instance after it has finished running. The function checks for 
    common attributes and methods that jMetal algorithms use to store their results, such as `get_result()`, 
    `result()`, or a list of `solutions`. It returns the best solution based on the highest fitness value (objective) 
    if multiple solutions are available. If the algorithm does not have
    """
    
    if hasattr(algorithm, "get_result"):
        return algorithm.get_result()
    if hasattr(algorithm, "result"):
        return algorithm.result()
    if hasattr(algorithm, "solutions") and algorithm.solutions:
        return max(algorithm.solutions, key=lambda s: s.objectives[0])
    raise AttributeError("Cannot retrieve result from jMetal algorithm.")


def _perm_to_matrix(perm: List[int]):
    """
    Convert a permutation of integers into a corresponding permutation matrix. The input is a list of integers 
    where the value at each index indicates the new position of that index in the permuted order. The output is 
    a square matrix where each row and column has exactly one entry of 1 (indicating the mapping) and 0s elsewhere. T
    his is used to represent the action of a gate on the state space in quantum circuit synthesis.
    :param perm: A list of integers representing a permutation, where the value at each index indicates the new 
        position of that index in the permuted order.
    :return: A 2D numpy array representing the permutation matrix corresponding to the input permutation.
    """
    d = len(perm)
    M = np.zeros((d, d), dtype=complex)
    for j in range(d):
        M[perm[j], j] = 1.0
    return M


def _register_gate_table(qc: QuditCircuit):
    """
    Register the gate table in the given QuditCircuit instance using the predefined QSG_TABLE from util. 
    This allows the QuditCircuit to recognize and apply the gates defined in the genetic algorithm's representation 
    when constructing the circuit. The gate table maps gate labels to their corresponding permutation matrices, 
    enabling the synthesis process to translate the genetic algorithm's output into actual quantum gates that can be 
    executed on a qudit system.   

    :param qc: An instance of QuditCircuit where the gate table will be registered. The gate table is a dictionary
        mapping gate labels (strings) to their corresponding permutation matrices (numpy arrays), which define 
        the behavior of the gates in the circuit.    
    """
    table = {k: _perm_to_matrix(v) for k, v in QSG_TABLE.items()}
    qc.set_gate_table(table)


def ga_circuit_to_qudit_circuit(ga_circuit: List[Gate], *, num_qudits: int, base: int, control_fire_value: Optional[int] = None, ) -> QuditCircuit:
    """
    Convert a circuit represented in the genetic algorithm's format (a list of Gate tuples) into a QuditCircuit instance. 
    This involves interpreting the gate types and their parameters, registering the appropriate gates in the QuditCircuit, 
    and constructing the circuit according to the specified control and target qudit indices. The function also handles the
    control fire value, which determines when controlled gates are activated based on the state of the control qudits.
    :param ga_circuit: A list of Gate tuples representing the circuit in the genetic algorithm
        format, where each tuple consists of a control qudit index, target qudit index, and gate type as a string.
    :param num_qudits: The total number of qudits in the circuit, which is needed to initialize the QuditCircuit 
        and interpret the gate parameters correctly.
    :param base: The base of the qudits (e.g., 3 for ternary), which is necessary for understanding the gate types 
        and their effects on the qudits.
    :param control_fire_value: An optional integer specifying the value of the control qudit that triggers the 
        controlled gates. If not provided, it defaults to base - 1, meaning the controlled gate will activate when 
        the control qudit is in its highest state. This allows for flexibility in how the controlled gates are 
        defined and can be adjusted based on the specific requirements of the synthesis task.    
    :return: A QuditCircuit instance that represents the same circuit as defined by the input ga_circuit, with gates 
        registered and arranged according to the control and target qudit indices. The resulting QuditCircuit can be 
        used for further processing, optimization, or execution on a quantum system.
    """
    if control_fire_value is None:
        control_fire_value = base - 1

    qc = QuditCircuit(num_qudits, base)
    _register_gate_table(qc)

    control_prefix = f"C{base-1}Z"

    for ctrl, tgt, gtype in ga_circuit:
        if gtype.startswith("Z") and not gtype.startswith("C"):
            qc.shift(gtype[1:], tgt)
        elif gtype.startswith(control_prefix):
            qc.ms(gtype[len(control_prefix):], ctrl, tgt, [control_fire_value])
        elif gtype.startswith("C2Z") and base == 3:
            qc.ms(gtype[3:], ctrl, tgt, [control_fire_value])
        else:
            raise ValueError(f"Unsupported gate type: {gtype}")

    return qc


def ga_to_shift_ms_ops(ga_circuit: List[Gate], *, base: int, control_fire_value: Optional[int] = None) -> List[Op]:
    """
    Convert a circuit represented in the genetic algorithm's format (a list of Gate tuples) into a list of operations (Op) 
    that can be executed to construct the same circuit. This function translates the genetic algorithm's gate 
    representation into a more explicit format of operations, distinguishing between shift
    and multi-qudit MS operations. The resulting list of operations can be used to build a QuditCircuit or to understand 
    the sequence of gates in a more detailed way. The function also handles the control fire value for controlled gates, 
    allowing for flexibility in how the operations are defined based on the state of the control qudits.
    :param ga_circuit: A list of Gate tuples representing the circuit in the genetic algorithm format, where each tuple 
    consists of a control qudit index, target qudit index, and gate type as a string.
    :param base: The base of the qudits (e.g., 3 for ternary), which is necessary for understanding the gate types and their 
    effects on the qudits, as well as for determining the control fire value if it is not provided.
    :param control_fire_value: An optional integer specifying the value of the control qudit that triggers the controlled gates. 
    If not provided, it defaults to base - 1, meaning the controlled gate will activate when the control qudit is in its 
    highest state. This allows for flexibility in how the controlled gates are defined and can be adjusted based on the 
    specific requirements of the synthesis task.    
    
    :return: A list of Op tuples representing the operations needed to construct the same circuit as defined by the 
        input ga_circuit, with each operation explicitly defined as either a shift or an MS operation, along with 
        the necessary parameters for execution. The resulting list of operations can be used for further
    """
    if control_fire_value is None:
        control_fire_value = base - 1

    control_prefix = f"C{base-1}Z"
    ops: List[Op] = []

    for ctrl, tgt, gtype in ga_circuit:
        if gtype.startswith("Z") and not gtype.startswith("C"):
            ops.append(("shift", gtype[1:], tgt))
        elif gtype.startswith(control_prefix):
            ops.append(("ms", gtype[len(control_prefix):], ctrl, tgt, [control_fire_value]))
        elif gtype.startswith("C2Z") and base == 3:
            ops.append(("ms", gtype[3:], ctrl, tgt, [control_fire_value]))
        else:
            raise ValueError(f"Unsupported gate type: {gtype}")

    return ops


def ops_to_qudit_circuit(ops: List[Op], *, num_qudits: int, base: int) -> QuditCircuit:
    """
    Convert a list of operations (gates) into a QuditCircuit instance that can be executed to construct the same circuit.
    This function takes a list of operations, where each operation is explicitly defined as either a shift or an MS operation,
    and builds a QuditCircuit by applying these operations in sequence. The function also handles the
    registration of the gate table in the QuditCircuit to ensure that the operations are recognized and can be executed correctly.

    :param ops: A list of Op tuples representing the operations needed to construct a circuit, where each operation is explicitly 
        defined as either a shift or an MS operation, along with the necessary parameters for execution.
    :param num_qudits: The total number of qudits in the circuit, which is needed to initialize the QuditCircuit and interpret 
        the operation parameters correctly.
    :param base: The base of the qudits (e.g., 3 for ternary), which is necessary for understanding the operation types and 
        their effects on the qudits, as well as for determining the control fire value if it is not provided in the operations. 
        This allows for flexibility in how the
        operations are defined based on the specific requirements of the synthesis task.
    """
    qc = QuditCircuit(num_qudits, base)
    rebuild_tables(base=base, num_qulines=num_qudits)
    _register_gate_table(qc)

    for op in ops:
        if op[0] == "shift":
            _, label, tgt = op
            qc.shift(label, tgt)
        elif op[0] == "ms":
            _, label, ctrl, tgt, cvals = op
            qc.ms(label, ctrl, tgt, cvals)
        else:
            raise ValueError(op)

    return qc


def genetic_synthesize(
    truth_table: TruthTable,
    *,
    base: int,
    num_qudits: int,
    output_indices: Iterable[int],
    pop_size: int = 100,
    generations: int = 10000,
    mutation_rate: float = 0.2,
    crossover_rate: float = 0.7,
    elite_size: int = 10,
    restoring: bool = False,
    return_ga: bool = False,
):
    """
    Synthesize a quantum circuit that implements the functionality defined by the given truth table using a genetic algorithm.
    The function sets up the genetic algorithm with the specified parameters, runs the algorithm to evolve a circuit, and then
    converts the resulting circuit from the genetic algorithm's format into a QuditCircuit instance. The
    synthesis process involves evaluating candidate circuits against the truth table, applying genetic operators such as 
    mutation and crossover, and selecting the best-performing circuits over multiple generations. The function also includes 
    options for restoring the circuit to a specific form and returning the raw genetic algorithm output if desired.

    Args:
        truth_table: A dictionary mapping complete input combinations (including target qubits initialized to 0) to their expected 
            output combinations, used internally for synthesis.
        base: The base of the qudits (e.g., 3 for ternary), which is necessary for understanding the gate types and their 
            effects on the qudits, as well as for determining the control fire value if it is not provided in the operations. 
            This allows for flexibility in how the operations are defined based on the specific requirements of the synthesis task.
        num_qudits: The total number of qudbits in the circuit, which is needed to initialize the QuditCircuit and interpret 
            the gate parameters correctly.
        output_indices: An iterable of indices indicating which wires are treated as outputs for fitness evaluation. 
            This allows the synthesis process to focus on matching the expected outputs defined in the truth table for 
            those specific wires.
        pop_size: The size of the population in the genetic algorithm, which determines how many candidate circuits are 
            evaluated and evolved in each generation. A larger population size can lead to better solutions but may increase 
            the runtime of the algorithm.
        generations: The number of generations to run the genetic algorithm, which controls how long the algorithm will 
            evolve the population of circuits. More generations can lead to better solutions but will also increase the runtime.
        mutation_rate: The rate at which mutations are applied to the candidate circuits in the genetic algorithm, which 
            introduces variability and allows the algorithm to explore the solution space. A higher mutation rate can help 
            avoid local minima but may also disrupt good solutions.
        crossover_rate: The rate at which crossover is applied between candidate circuits in the genetic algorithm, which 
            allows for the combination of features from different circuits to create new candidate solutions. A higher 
            crossover rate can promote diversity in the population but may also lead to less stable convergence.
        elite_size: The number of top-performing circuits to retain as elites in each generation of the genetic algorithm, 
            which ensures that the best solutions are preserved and can contribute to the next generation. A larger elite 
            size can help maintain good solutions but may reduce diversity in the population.
        restoring: A boolean flag indicating whether to apply a restoring transformation to the resulting circuit, which 
            can help ensure that the circuit has a specific form or structure. This is useful for certain applications 
            where the circuit needs to be in a particular format for execution or further processing.
        return_ga: A boolean flag indicating whether to return the raw output from the genetic algorithm (a list of 
            Gate tuples) instead of converting it to a QuditCircuit. This can be useful for users who want to see
    """
    rebuild_tables(base=base, num_qulines=num_qudits)

    problem = QuantumCircuitProblem(truth_table, output_indices=output_indices)

    algorithm = ElitistGeneticAlgorithm(
        problem=problem,
        population_size=pop_size,
        offspring_population_size=pop_size,
        mutation=CircuitMutation(mutation_rate, truth_table, output_indices=output_indices),
        crossover=CircuitCrossover(crossover_rate),
        termination_criterion=TerminationByEvaluations(pop_size * generations),
        elite_size=elite_size,
        selection=BinaryTournamentSelection(),
    )

    algorithm.run()
    result = _get_algorithm_result(algorithm)
    ga_circuit = result.variables[0]

    ga_circuit = simplify_circuit(ga_circuit)

    if restoring:
        ga_circuit = make_restoring_circuit(ga_circuit, protected_indices=output_indices)
        ga_circuit = simplify_circuit(ga_circuit)

    if return_ga:
        return ga_circuit

    return ga_circuit_to_qudit_circuit(
        ga_circuit,
        num_qudits=num_qudits,
        base=base,
    )


def synthesize_ops_from_truth_table(
    truth_table: TruthTable,
    *,
    base: int,
    num_qudits: int,
    output_indices: Iterable[int],
    pop_size: int = 100,
    generations: int = 10000,
    mutation_rate: float = 0.2,
    crossover_rate: float = 0.7,
    elite_size: int = 10,
    restoring: bool = True,
) -> List[Op]:
    """
    Synthesize a quantum circuit that implements the functionality defined by the given truth table using a genetic algorithm, and return the resulting circuit as a list of operations (Op) that can be executed to construct the same circuit. This function is similar to `genetic_synthesize`, but instead of returning a QuditCircuit instance, it returns a list of operations that represent the gates in the synthesized circuit. The operations are explicitly defined as either shift or MS operations, along with their parameters, allowing for a more detailed understanding of the sequence of gates in the synthesized circuit. The function also includes options for restoring the circuit to a specific form and controlling various parameters of the genetic algorithm.
    Args:
    - truth_table: A dictionary mapping complete input combinations (including target qubits initialized to
        0) to their expected output combinations, used internally for synthesis.
    - base: The base of the qudits (e.g., 3 for ternary), which is necessary for understanding the gate types and their effects on the qudbits, as
        well as for determining the control fire value if it is not provided in the operations. This allows for flexibility in how the operations are defined based on the specific requirements of the synthesis task.
    - num_qudbits: The total number of qubits in the circuit, which is needed to initialize the QuditCircuit and interpret the gate parameters correctly.
    - output_indices: An iterable of indices indicating which wires are treated as outputs for fitness evaluation. This allows the synthesis process to focus on matching the expected outputs defined in the truth table for those specific wires.
    - pop_size: The size of the population in the genetic algorithm, which determines how many candidate circuits are evaluated and evolved in each generation. A larger population size can lead to better solutions but may increase the runtime of the algorithm.
    - generations: The number of generations to run the genetic algorithm, which controls how long the algorithm will evolve the population of circuits. More generations can lead to better solutions but will also increase the runtime.
    - mutation_rate: The rate at which mutations are applied to the candidate circuits in the genetic algorithm, which introduces variability and allows the algorithm to explore the solution space. A higher mutation rate can help avoid local minima but may also disrupt good solutions.
    - crossover_rate: The rate at which crossover is applied between candidate circuits in the genetic algorithm, which allows for the combination of features from different circuits to create new candidate solutions. A higher crossover rate can promote diversity in the population but may also lead to less stable convergence.
    - elite_size: The number of top-performing circuits to retain as elites in each generation of the genetic algorithm, which ensures that the best solutions are preserved and can contribute to the next generation. A larger elite size can help maintain good solutions but may reduce diversity in the population.
    - restoring: A boolean flag indicating whether to apply a restoring transformation to the resulting circuit, which can help ensure that the circuit has a specific form or structure. This is useful for certain applications where the circuit needs to be in a particular format for execution or further processing.
    """
    ga_circuit = genetic_synthesize(
        truth_table,
        base=base,
        num_qudits=num_qudits,
        output_indices=output_indices,
        pop_size=pop_size,
        generations=generations,
        mutation_rate=mutation_rate,
        crossover_rate=crossover_rate,
        elite_size=elite_size,
        restoring=restoring,
        return_ga=True,
    )
    return ga_to_shift_ms_ops(ga_circuit, base=base)
