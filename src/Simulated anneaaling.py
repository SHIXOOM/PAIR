from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model
import numpy as np
import random

class ExampleSolver1(LLMTSPSolver):
    """
    Example concrete implementation of the LLMTSPSolver class
    """

    def __init__(self, model: Model):
        super().__init__(model)
        print(f"Solver created with model: {model}")

    def calculate_total_distance(self, tour, distance_matrix):
        """Calculate the total distance of the TSP tour."""
        return sum(distance_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + distance_matrix[tour[-1], tour[0]]

    def swap_cities(self, tour):
        """Generate a neighboring solution by swapping two cities."""
        new_tour = tour.copy()
        i, j = random.sample(range(len(tour)), 2)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        return new_tour

    def simulated_annealing(self, distance_matrix, initial_temperature, cooling_rate, max_iterations):
        """Perform Simulated Annealing to find a good initial solution."""
        num_cities = len(distance_matrix)
        current_solution = list(range(num_cities))
        random.shuffle(current_solution)
        current_cost = self.calculate_total_distance(current_solution, distance_matrix)
        
        best_solution = current_solution
        best_cost = current_cost
        
        temperature = initial_temperature
        
        for iteration in range(max_iterations):
            new_solution = self.swap_cities(current_solution)
            new_cost = self.calculate_total_distance(new_solution, distance_matrix)
            
            if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temperature):
                current_solution = new_solution
                current_cost = new_cost
                
                if new_cost < best_cost:
                    best_solution = new_solution
                    best_cost = new_cost
            
            temperature *= cooling_rate
        
        return best_solution, best_cost

    def initialize_population_with_sa(self, distance_matrix, population_size):
        """Initialize a population using Simulated Annealing with variable cooling rates."""
        initial_temperature = 1000
        cooling_rate_range = (0.90, 0.99)
        max_iterations = 1000

        population = []
        for _ in range(population_size):
            # Randomly select a cooling rate within the specified range
            cooling_rate = random.uniform(*cooling_rate_range)
            solution, cost = self.simulated_annealing(distance_matrix, initial_temperature, cooling_rate, max_iterations)
            population.append((solution, cost))
        return population

    def solve(self, problem):
        distance_matrix = problem['distance_matrix']
        population_size = problem['population_size']
        num_cities = problem['num_cities']

        print("Solving problem with the following parameters:")
        print(f"Number of cities: {num_cities}")
        print(f"Population size: {population_size}")

        population = self.initialize_population_with_sa(distance_matrix, population_size)

        for i, (solution, cost) in enumerate(population):
            print(f"Solution {i+1}: {solution} with cost {cost}")

        return population
