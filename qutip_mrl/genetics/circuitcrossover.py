import random
from jmetal.operator.crossover import Crossover
from .circuitsolution import CircuitSolution
from .config import *

class CircuitCrossover(Crossover):
    """
    Implements a single-point crossover for quantum circuits represented as lists of gates.
    The crossover combines two parent circuits to produce two child circuits by cutting each parent at a random point 
    and swapping the tails.
    The resulting child circuits are truncated to a maximum length defined by MAX_GENES to ensure they do not exceed 
    the allowed number of gates.
    """
    
    def __init__(self, probability: float = 0.7):
        """
        Initializes the CircuitCrossover operator with a given crossover probability.
        :param probability: The probability of performing crossover. If a random number exceeds this value, the parents are returned unchanged.
        """
        super(CircuitCrossover, self).__init__(probability)

    def execute(self, parents):
        """
        Executes the crossover operation on the given parent solutions.
        :param parents: A list of two parent solutions, each containing a quantum circuit.
        :return: A list of two child solutions resulting from the crossover.
        """
        
        if len(parents) != 2:
            return parents

        parent1, parent2 = parents[0], parents[1]
        circuit1 = parent1.variables[0]
        circuit2 = parent2.variables[0]

        if random.random() > self.probability:
            return [parent1.copy(), parent2.copy()]

        # Single-point crossover
        if len(circuit1) > 1 and len(circuit2) > 1:
            cut1 = random.randint(1, len(circuit1))
            cut2 = random.randint(1, len(circuit2))

            child1_circuit = circuit1[:cut1] + circuit2[cut2:]
            child2_circuit = circuit2[:cut2] + circuit1[cut1:]

            # Ensure length constraints
            if len(child1_circuit) > MAX_GENES:
                child1_circuit = child1_circuit[:MAX_GENES]
            if len(child2_circuit) > MAX_GENES:
                child2_circuit = child2_circuit[:MAX_GENES]

            child1 = CircuitSolution(child1_circuit)
            child2 = CircuitSolution(child2_circuit)

            return [child1, child2]

        return [parent1.copy(), parent2.copy()]

    def get_number_of_parents(self):
        return 2

    def get_number_of_children(self):
        return 2

    def get_name(self):
        return "CircuitCrossover"