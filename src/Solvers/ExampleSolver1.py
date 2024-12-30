from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model
from src.PopulationInitializers.PopulationInitializer import  PopulationInitializer
from src.PromptResponseManager.PromptResponseManager import PromptResponseManager as PRManager


class ExampleSolver1(LLMTSPSolver):
    def __init__(self, model: Model, population_initializer: PopulationInitializer):
        super().__init__(model, population_initializer)

        self.population_initializer = population_initializer
        
    def solve(self, problem):
        # initialize population
        population = self.population_initializer.initialize(30, problem)
         
        # solve the problem
        MAX_GENERATIONS = 250
        for generation in range(MAX_GENERATIONS):
            # if optimal distance is reached, return the best tour and the generation number
            if population[-1][1] == optimalDistance: # TODO: get optimal distance for the problem, MAHMOUD
                return population[-1][0], generation
            
            # get the point-coordinates pairs, this is necessary to follow the prompt format for the point-coordinates pairs
            pointsCoordinatesPairs = {i: (j[0], j[1]) for i, j in problem.node_coords.items()}
            # get the node count
            nodeCount = problem.dimension
            print(pointsCoordinatesPairs)
            
            # get the new generation prompt and parse the new generation traces
            newGenPrompt = PRManager.getNewGenerationPrompt(population, pointsCoordinatesPairs, 30)
            newGenerationTraces = PRManager.parseNewGeneration(self.model.run(newGenPrompt), nodeCount = nodeCount)
            
            # get the lengths of the new generation traces
            population = [] 
            for trace in newGenerationTraces:
                length = self.getTourLength(trace, problem)
                population.append((trace, length))
            
            # sort the population by the tour lengths descendingly
            population = sorted(population, key=lambda x: x[1], reverse = True)
        
        # if the optimal distance is not reached, return the best tour and the generation number
        return population[-1][0], generation
        
    def getTourLength(self, tour:list[int], problem:tsplib95.models.StandardProblem)->int:
        tourLength = 0
        for i in range(problem.dimension - 1, -1, -1):
            tourLength += problem.get_weight(tour[i], tour[i - 1])
            
        return tourLength
