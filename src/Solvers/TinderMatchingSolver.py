import tsplib95
from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model
from src.PopulationInitializers.PopulationInitializer import PopulationInitializer
from src.PromptResponseManager.PromptResponseManager import PromptResponseManager as PRManager


class TinderMatchingSolver(LLMTSPSolver):
    def __init__(self, model: Model, population_initializer: PopulationInitializer):
        super().__init__(model, population_initializer)

        self.population_initializer = population_initializer

    def solve(self, problem, problem_optimal_distance=0) -> tuple[list[int], int]:
        """
        Args:
            problem: tsp problem instance
            problem_optimal_distance(optional): problem optimal solution length
        Returns:
            tuple[list[int],int]
            best found solution, generation number found in
        """

        """
        - initialize population
        """

        MAX_GENERATIONS = 250
        POPULATION_SIZE = 30
        NODE_COUNT = problem.dimension

        currentModelTemperature = 1
        population = self.population_initializer.initialize(POPULATION_SIZE, problem)

        """ Configure model """
        systemPrompt = PRManager.getSystemPrompt(populationSize=POPULATION_SIZE)
        self.model.configure(systemPrompt, currentModelTemperature)

        pointsCoordinatesPairs = {i: (j[0], j[1]) for i, j in problem.node_coords.items()}
        for generation in range(1, MAX_GENERATIONS + 1):
            if population[-1][1] == problem_optimal_distance:
                return population[-1][0], generation

            """
            - use current generation(population) to generate prompt
            - prompt the model to generate new generation
            - parse response
            """
            newGenPrompt = PRManager.getNewGenerationPrompt(population, pointsCoordinatesPairs, 30)
            newGenResponse = self.model.run(newGenPrompt)
            newGenerationTraces = PRManager.parseNewGeneration(newGenResponse, nodeCount=NODE_COUNT)
            # TODO: ADD logging

            # get the lengths of the new generation traces
            population = []
            for trace in newGenerationTraces:
                length = problem.trace_tours([trace])
                population.append((trace, length))

            # sort the population by the tour lengths descendingly
            population = sorted(population, key=lambda x: x[1], reverse=True)

        # if the optimal distance is not reached, return the best tour and the generation number
        return population[-1][0], MAX_GENERATIONS
