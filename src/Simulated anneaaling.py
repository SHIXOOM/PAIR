import numpy as np
import random

def calculate_total_distance(tour, distance_matrix):
    """Calculate the total distance of the TSP tour."""
    return sum(distance_matrix[tour[i], tour[i + 1]] for i in range(len(tour) - 1)) + distance_matrix[tour[-1], tour[0]]

def swap_cities(tour):
    """Generate a neighboring solution by swapping two cities."""
    new_tour = tour.copy()
    i, j = random.sample(range(len(tour)), 2)
    new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    return new_tour

def simulated_annealing(distance_matrix, initial_temperature, cooling_rate, max_iterations):
    """Perform Simulated Annealing to find a good initial solution."""
    num_cities = len(distance_matrix)
    current_solution = list(range(num_cities))
    random.shuffle(current_solution)
    current_cost = calculate_total_distance(current_solution, distance_matrix)
    
    best_solution = current_solution
    best_cost = current_cost
    
    temperature = initial_temperature
    
    for iteration in range(max_iterations):
        new_solution = swap_cities(current_solution)
        new_cost = calculate_total_distance(new_solution, distance_matrix)
        
        if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temperature):
            current_solution = new_solution
            current_cost = new_cost
            
            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost
        
        temperature *= cooling_rate
    
    return best_solution, best_cost

def initialize_population_with_sa(distance_matrix, population_size, initial_temperature, cooling_rate, max_iterations):
    """Initialize a population using Simulated Annealing."""
    population = []
    for _ in range(population_size):
        solution, cost = simulated_annealing(distance_matrix, initial_temperature, cooling_rate, max_iterations)
        population.append((solution, cost))
    return population

# Example usage
if __name__ == "__main__":
    num_cities = 15
    distance_matrix = np.random.rand(num_cities, num_cities) * 100  # Random distance matrix for demonstration
    distance_matrix = (distance_matrix + distance_matrix.T) / 2  # Make sure the matrix is symmetric
    np.fill_diagonal(distance_matrix, 0)  # Distance from a city to itself is zero

    population_size = 30
    initial_temperature = 1000
    cooling_rate = 0.99
    max_iterations = 1000

    population = initialize_population_with_sa(distance_matrix, population_size, initial_temperature, cooling_rate, max_iterations)

    for i, (solution, cost) in enumerate(population):
        print(f"Solution {i+1}: {solution} with cost {cost}")