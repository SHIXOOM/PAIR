import tsplib95
from src.PopulationInitializers.PopulationInitializer import PopulationInitializer
import random
import numpy as np


class SAPopulationInitializer(PopulationInitializer):

    def __init__(self):
        self.problem = None

    def initialize(self, population_size: int, problem: tsplib95.models.StandardProblem) -> list[tuple[list, int]]:
        """ returns a list of tuples. each tuple contains a 1-based tsp trace and its length """

        self.problem = problem

        """Initialize population using Simulated Annealing with variable cooling rates."""
        cooling_rate_range = (0.90, 0.99)
        population = []

        for _ in range(population_size):
            cooling_rate = random.uniform(*cooling_rate_range)
            tour, length = self._simulated_annealing(cooling_rate=cooling_rate)
            population.append((tour, length))

        """ convert to one-based indexing """
        population = [([city + 1 for city in tour], length) for tour, length in population]
        return population

    def _calculate_total_distance(self, tour):
        """Calculate the total distance of the TSP tour."""
        return sum(self.problem.get_weight(tour[i] + 1, tour[i + 1] + 1) for i in
                   range(len(tour) - 1)) + self.problem.get_weight(tour[-1] + 1, tour[0] + 1)

    def _swap_cities(self, tour):
        """Generate a neighboring solution by swapping two cities."""
        new_tour = tour.copy()
        i, j = random.sample(range(len(tour)), 2)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        return new_tour

    def _simulated_annealing(self, cooling_rate=0.95, initial_temperature=1000, max_iterations=1000):
        """Perform Simulated Annealing to find a good initial solution."""
        num_cities = len(list(self.problem.get_nodes()))
        current_solution = list(range(0, num_cities))  # Start from 0 for internal representation
        random.shuffle(current_solution)
        current_cost = self._calculate_total_distance(current_solution)

        best_solution = current_solution
        best_cost = current_cost
        temperature = initial_temperature

        for _ in range(max_iterations):
            new_solution = self._swap_cities(current_solution)
            new_cost = self._calculate_total_distance(new_solution)

            if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temperature):
                current_solution = new_solution
                current_cost = new_cost

                if new_cost < best_cost:
                    best_solution = new_solution
                    best_cost = new_cost

            temperature *= cooling_rate

        return best_solution, best_cost
