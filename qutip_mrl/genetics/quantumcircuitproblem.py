# quantumcircuitproblem.py

from __future__ import annotations

from typing import Dict, Tuple, List, Optional

from jmetal.core.problem import Problem

from .circuitsolution import CircuitSolution
from . import util

"""
Definition of types for user input and internal processing:
- TruthTable: A dictionary mapping complete input combinations (including target qubits initialized to 0) 
    to their expected output combinations, used internally for synthesis. 
"""
TruthTable = Dict[Tuple[int, ...], Tuple[int, ...]]


class QuantumCircuitProblem(Problem):
    """
    Single-objective GA problem: maximize correctness/compactness for a reversible qudit circuit.
    """
    
    def __init__(
        self,
        truth_table: TruthTable,
        *,
        output_indices: Optional[List[int]] = None,
        min_genes: Optional[int] = None,
        max_genes: Optional[int] = None,
    ):
        """Initialize the QuantumCircuitProblem with a given truth table, output indices, and gene length constraints.
        :param truth_table: A dictionary mapping complete input combinations (including target qubits initialized to 0) to their expected output combinations, used internally for synthesis.
        :param output_indices: An optional list of indices indicating which wires are treated as outputs for fitness evaluation. If None, defaults to the last qubit.
        :param min_genes: The minimum number of gates in the circuit. If None, defaults to util.MIN_GENES or 1.
        :param max_genes: The maximum number of gates in the circuit. If None, defaults to util.MAX_GENES or 60.
        """
        super().__init__()
        self.truth_table = truth_table
        self.output_indices = output_indices

        # Use limits from util if available; otherwise fall back.
        self.min_genes = int(min_genes if min_genes is not None else getattr(util, "MIN_GENES", 1))
        self.max_genes = int(max_genes if max_genes is not None else getattr(util, "MAX_GENES", 60))
        if self.min_genes < 0:
            self.min_genes = 0
        if self.max_genes < max(1, self.min_genes):
            self.max_genes = max(1, self.min_genes)

        # jMetalPy bookkeeping
        self._number_of_variables = 1
        self._number_of_objectives = 1
        self._number_of_constraints = 0

        # Maximize fitness
        self.obj_directions = [self.MAXIMIZE]
        self.obj_labels = ["fitness"]

    @property
    def number_of_variables(self) -> int:
        return self._number_of_variables

    @property
    def number_of_objectives(self) -> int:
        return self._number_of_objectives

    @property
    def number_of_constraints(self) -> int:
        return self._number_of_constraints

    @property
    def name(self) -> str:
        return "QuantumCircuitProblem"

    def create_solution(self) -> CircuitSolution:
        """
        Create a new random solution for the quantum circuit problem. The solution consists of a randomly 
            generated circuit (a list of gates) with a length between min_genes and max_genes. The fitness 
            is initialized to 0.0.
        :return: A new CircuitSolution instance with a random circuit and initialized fitness.
        """
        sol = CircuitSolution()
        length = 0
        if self.max_genes > 0:
            length = util.random.randint(self.min_genes, self.max_genes) if hasattr(util, "random") else __import__("random").randint(self.min_genes, self.max_genes)
        # Build circuit
        circ = [util.random_gate() for _ in range(length)]
        sol.variables = [circ]
        sol.objectives = [0.0]
        sol.constraints = []
        sol.attributes = {}
        return sol

    def evaluate(self, solution: CircuitSolution) -> CircuitSolution:
        """
        Evaluate the fitness of a given solution by computing how well the circuit matches the expected outputs 
            defined in the truth table. The fitness is calculated using util.fitness and stored in the solution's objectives.
        :param solution: The CircuitSolution instance to be evaluated, containing a quantum circuit and its
            fitness value.
        :return: The same CircuitSolution instance with its fitness value updated based on the evaluation.
        """
        circuit = solution.variables[0]
        try:
            fit = util.fitness(circuit, self.truth_table, output_indices=self.output_indices)
        except TypeError:
            # Backward-compatible util.fitness signature
            fit = util.fitness(circuit, self.truth_table)
        solution.objectives[0] = float(fit)
        return solution

    def get_name(self) -> str:
        return self.name
