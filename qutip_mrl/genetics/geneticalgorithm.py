import random
from jmetal.algorithm.singleobjective.genetic_algorithm import GeneticAlgorithm
from .quantumcircuitproblem import QuantumCircuitProblem
from .util import *
from .config import MIN_GENES, MAX_GENES, STAGNATION_LIMIT

class ElitistGeneticAlgorithm(GeneticAlgorithm):
    """
    An elitist genetic algorithm for quantum circuit synthesis that incorporates adaptive mutation rates, local search, 
    and diversity injection to enhance convergence towards optimal solutions while avoiding premature stagnation.
    Key features include:
    - Elitism: Retains the best solutions across generations to ensure that the best found solutions are not lost.
    - Adaptive Mutation: Adjusts mutation rates based on the fitness of solutions to balance exploration and exploitation.
    - Local Search: Applies a hill climbing local search to newly found best solutions to further refine them.
    - Diversity Injection: Introduces new random solutions when the population shows signs of stagnation, especially when 
      close to optimal fitness, to escape local optima and explore new regions of the solution space.
    """
    
    def __init__(self, problem, population_size, offspring_population_size, 
                 mutation, crossover, termination_criterion, selection, elite_size=5):
        """
        Initializes the ElitistGeneticAlgorithm with the given parameters.
        :param problem: The problem instance to solve, which should be a QuantumCircuitProblem.
        :param population_size: The number of solutions in the population.
        :param offspring_population_size: The number of offspring to produce in each generation.
        :param mutation: The mutation operator to apply to offspring.
        :param crossover: The crossover operator to combine parent solutions.
        :param termination_criterion: The criterion to determine when to stop the algorithm.
        :param selection: The selection operator to choose parent solutions for reproduction.
        :param elite_size: The number of top solutions to retain as elites in each generation.
        """
        super().__init__(problem, population_size, offspring_population_size,
                        mutation, crossover, selection, termination_criterion)
        self.elite_size = elite_size
        self.best_fitness_history = []
        self.generation_count = 0
        self.stagnation_count = 0
        self.best_seen = 0.0

    def replacement(self, population, offspring_population):
        """
        Combines the current population with the offspring, applies elitism to retain the best solutions, and injects diversity if stagnation is detected.
        :param population: The current population of solutions.
        :param offspring_population: The newly generated offspring solutions.
        :return: The new population for the next generation after applying elitism and diversity injection if needed.
        """
        self.generation_count += 1

        # Combine populations
        all_solutions = population + offspring_population

        # Sort by fitness (descending for maximization)
        all_solutions.sort(key=lambda x: x.objectives[0] if x.objectives[0] is not None else float('-inf'), 
                          reverse=True)

        # Check for stagnation
        current_best = all_solutions[0].objectives[0] if all_solutions[0].objectives[0] is not None else 0.0
        if current_best <= self.best_seen + 1e-6:
            self.stagnation_count += 1
        else:
            self.best_seen = current_best
            self.stagnation_count = 0
            print(f"NEW BEST FITNESS: {current_best:.6f} at generation {self.generation_count}")

            # Apply local search to new best solutions
            if current_best > 0.8:  # Only for high-fitness solutions
                print("Applying local search to best solution...")
                improved = self.local_search(all_solutions[0])
                if improved.objectives[0] > current_best:
                    all_solutions[0] = improved
                    print(f"Local search improvement: {improved.objectives[0]:.6f}")

        # Diversity injection if stagnated
        if self.stagnation_count > STAGNATION_LIMIT and current_best > 0.8:
            elite_solutions = all_solutions[:self.elite_size]

            # Replace 50% with diverse solutions when close to optimum
            diverse_solutions = []
            for _ in range(int(self.population_size * 0.8)):
                new_solution = self.problem.create_solution()
                self.problem.evaluate(new_solution)
                diverse_solutions.append(new_solution)

            remaining_needed = self.population_size - len(elite_solutions) - len(diverse_solutions)
            remaining_solutions = all_solutions[self.elite_size:self.elite_size + remaining_needed]

            new_population = elite_solutions + diverse_solutions + remaining_solutions
            self.stagnation_count = 0
        elif self.stagnation_count > STAGNATION_LIMIT:
            # Keep elite but replace 30% with new random solutions
            elite_solutions = all_solutions[:self.elite_size]
            diverse_solutions = []

            for _ in range(int(self.population_size * 0.3)):
                new_solution = self.problem.create_solution()
                self.problem.evaluate(new_solution)
                diverse_solutions.append(new_solution)

            remaining_needed = self.population_size - len(elite_solutions) - len(diverse_solutions)
            remaining_solutions = all_solutions[self.elite_size:self.elite_size + remaining_needed]

            new_population = elite_solutions + diverse_solutions + remaining_solutions
            self.stagnation_count = 0
        else:
            # Standard elitist selection
            new_population = all_solutions[:self.population_size]

        # Track fitness
        self.best_fitness_history.append(current_best)

        # Progress reporting
        if self.generation_count % 50 == 0:
            avg_fitness = sum(sol.objectives[0] for sol in new_population[:10] if sol.objectives[0] is not None) / 10
            diversity = self.calculate_diversity(new_population[:20])
            print(f"Gen {self.generation_count:3d}: Best={current_best:.4f}, Avg={avg_fitness:.4f}, Diversity={diversity:.3f}")

        return new_population
    
    def local_search(self, solution):
        """
        Hill climbing local search on a solution to find a better neighboring solution by making small modifications to 
        the circuit and evaluating their fitness.
        """
        best_solution = solution.copy()
        current_fitness = solution.objectives[0] if solution.objectives[0] is not None else 0.0

        # Try multiple local modifications
        for attempt in range(20):  # 20 local search attempts
            # Create a neighbor by small modification
            neighbor = best_solution.copy()
            circuit = neighbor.variables[0]

            if len(circuit) == 0:
                continue

            # Choose modification type
            mod_type = random.choice(['change', 'add', 'remove', 'swap'])

            if mod_type == 'change' and len(circuit) > 0:
                idx = random.randint(0, len(circuit) - 1)
                circuit[idx] = random_gate()
            elif mod_type == 'add' and len(circuit) < MAX_GENES:
                pos = random.randint(0, len(circuit))
                circuit.insert(pos, random_gate())
            elif mod_type == 'remove' and len(circuit) > MIN_GENES:
                idx = random.randint(0, len(circuit) - 1)
                del circuit[idx]
            elif mod_type == 'swap' and len(circuit) > 1:
                i, j = random.sample(range(len(circuit)), 2)
                circuit[i], circuit[j] = circuit[j], circuit[i]

            # Evaluate neighbor
            self.problem.evaluate(neighbor)

            if neighbor.objectives[0] > current_fitness:
                best_solution = neighbor.copy()
                current_fitness = neighbor.objectives[0]

        return best_solution

    def calculate_diversity(self, solutions):
        """
        Calculate diversity based on circuit length variation

        Args:
            solutions (List[Solution]): A list of solutions to evaluate for diversity.
        """
        if not solutions:
            return 0.0
        lengths = [len(sol.variables[0]) for sol in solutions if sol.variables]
        if len(set(lengths)) <= 1:
            return 0.0
        return len(set(lengths)) / len(lengths)