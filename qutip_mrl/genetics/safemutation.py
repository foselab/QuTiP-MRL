# safemutation.py
from __future__ import annotations

import random
from copy import deepcopy
from typing import List
from config import *

from jmetal.operator.mutation import Mutation

from .circuitsolution import CircuitSolution
from . import util


Gate = util.Gate


class CircuitMutation(Mutation):
    """
    Implements a safe mutation operator for quantum circuits represented as lists of gates.
    The mutation adapts its behavior based on the current fitness of the solution, allowing for more aggressive 
    mutations when the fitness is low and more conservative changes as the solution improves.
    The operator supports various mutation types, including adding, removing, changing, swapping, splitting gates, 
    and optimizing the circuit
    based on a provided truth table. The mutation ensures that the resulting circuit remains within defined length 
    constraints and can optionally optimize the circuit if it is already correct.
    """

    def __init__(self, mutation_probability: float = 0.1, truth_table=None, output_indices=None):
        """
        Initializes the CircuitMutation operator with a given mutation probability, truth table, and output indices.
        :param mutation_probability: The base probability of performing mutation. This will be adapted based on fitness.
        :param truth_table: An optional truth table used to evaluate the correctness of the circuit and enable optimization mutations.
        :param output_indices: The indices of the qulines that are considered outputs for fitness evaluation. Defaults to the last quline if not provided.  
        """        
        super().__init__(mutation_probability)
        self.mutation_probability = mutation_probability
        self.truth_table = truth_table
        self.output_indices = tuple(output_indices) if output_indices is not None else (util.NUM_QULINES - 1,)

    def execute(self, solution):
        """
        Executes the mutation operation on the given solution.
        The mutation type is chosen based on the current fitness of the solution and the structure of the circuit.
        :param solution: The solution to be mutated, containing a quantum circuit and its fitness value.
        :return: A new mutated solution.   
        """
        new_solution = CircuitSolution()
        new_solution.variables = [deepcopy(solution.variables[0])]
        new_solution.objectives = [None]
        new_solution.constraints = []
        new_solution.attributes = {}

        fitness_val = solution.objectives[0] if solution.objectives[0] is not None else 0.0
        adaptive_rate = self.mutation_probability * (1.0 - fitness_val * 0.5)

        if random.random() >= adaptive_rate:
            return new_solution

        circuit: List[Gate] = new_solution.variables[0]

        mutation_types = []
        if len(circuit) < MAX_GENES:
            mutation_types.append("add")
        if len(circuit) > MIN_GENES:
            mutation_types.append("remove")
        if len(circuit) > 0:
            mutation_types.extend(["change", "change", "swap", "split"])
        if self.is_circuit_correct(circuit):
            mutation_types.append("optimize")

        if not mutation_types:
            return new_solution

        mtype = random.choice(mutation_types)

        if mtype == "add":
            pos = random.randint(0, len(circuit))
            circuit.insert(pos, util.random_gate())

        elif mtype == "remove":
            idx = random.randint(0, len(circuit) - 1)
            del circuit[idx]

        elif mtype == "change":
            idx = random.randint(0, len(circuit) - 1)
            circuit[idx] = util.random_gate()

        elif mtype == "swap":
            if len(circuit) > 1:
                i, j = random.sample(range(len(circuit)), 2)
                circuit[i], circuit[j] = circuit[j], circuit[i]

        elif mtype == "split":
            if len(circuit) > 2:
                start = random.randint(0, len(circuit) - 2)
                end = random.randint(start + 1, len(circuit) - 1)
                new_solution.variables[0] = circuit[start:end]

        elif mtype == "optimize":
            new_solution.variables[0] = util.simplify_circuit(circuit)

        return new_solution

    def get_name(self) -> str:
        """Returns the name of the mutation operator."""
        return "CircuitMutation"

    def is_circuit_correct(self, circuit: List[Gate]) -> bool:
        """Checks if the given circuit is correct based on the provided truth table and output indices."""
        if self.truth_table is None:
            return False
        
        return util.fitness(circuit, self.truth_table, output_indices=self.output_indices) >= 1.0
