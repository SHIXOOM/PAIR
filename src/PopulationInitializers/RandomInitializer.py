import tsplib95
from src.PopulationInitializers.PopulationInitializer import PopulationInitializer
import random

class RandomInitializer(PopulationInitializer):
    def __init__(self):
        self.problem = None
    
    def initialize(self, population_size: int, problem: tsplib95.models.StandardProblem) -> list[tuple[list, int]]:
        """ returns a list of tuples. each tuple contains a 1-based tsp trace and its length """
        self.problem = problem

        node_count = problem.dimension
        population = []
        for i in range(population_size*6):
            tour = [point for point in range(1, node_count + 1)]
            random.shuffle(tour)
            traceDistance = problem.trace_tours([tour])
            population.append((tour, traceDistance[0]))
            
            
        
        population.sort(key=lambda x: x[1], reverse=True)
        population = population[-population_size:]
        return population

# problem = tsplib95.load('/Users/shadyali/Downloads/clu_25_10.tsp')
# ri = RandomInitializer(problem)
# print(ri.initialize(16, problem))
