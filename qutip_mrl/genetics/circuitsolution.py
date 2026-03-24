from jmetal.core.solution import Solution
from copy import deepcopy

class CircuitSolution(Solution):
    """
    Represents a solution in the genetic algorithm for quantum circuit synthesis.
    Each solution encapsulates a quantum circuit (as a list of gates) and its associated fitness value.
    The class provides methods for copying the solution, which is essential for genetic operations like crossover
    """
        
    def __init__(self, variables=None):
        """
        Initializes a CircuitSolution instance.
        :param variables: A list representing the quantum circuit (e.g., a list of gates). If None, initializes with an empty circuit.
        """
        
        # 1 variable, 1 objective, 0 constraints
        super().__init__(1, 1)

        # Internally store variables in a private field
        self._variables = [variables] if variables is not None else []
        self.objectives = [None]
        self.constraints = []
        self.attributes = {}

    # ---- REQUIRED by jMetalPy: variables must be a @property ----
    @property
    def variables(self):
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value

    # ---- REQUIRED by jMetalPy: __copy__ must be implemented ----
    def __copy__(self):
        new_solution = CircuitSolution()

        # deep copy circuit if present
        if self._variables:
            new_solution._variables = [deepcopy(self._variables[0])]
        else:
            new_solution._variables = []

        new_solution.objectives = self.objectives[:]          # shallow copy list
        new_solution.constraints = self.constraints[:]        # shallow copy list
        new_solution.attributes = self.attributes.copy()      # dict copy

        return new_solution

    # Compatibility: some code may call copy()
    def copy(self):
        return self.__copy__()

    def __str__(self):
        return f"Circuit: {self._variables}, Fitness: {self.objectives[0]}"
