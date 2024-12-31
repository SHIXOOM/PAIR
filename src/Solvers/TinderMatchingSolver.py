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
        NODE_COUNT = problem.dimension

        populationSize = 30
        currentModelTemperature = 1
        population = self.population_initializer.initialize(populationSize, problem)

        """ Configure model """
        systemPrompt = PRManager.getSystemPrompt(populationSize=populationSize)
        self.model.configure(systemPrompt, currentModelTemperature)

        pointsCoordinatesPairs = {i: (j[0], j[1]) for i, j in problem.node_coords.items()}
        bestSolutionLength = population[-1][1]
        
        worseIterations  = 0
        for generation in range(1, MAX_GENERATIONS + 1):
            
            print(f"""
                best sol: {bestSolutionLength}
                Generation: {generation}
                _________________________________________________________________________________
                """)
            if population[-1][1] == problem_optimal_distance:
                return population[-1][0], generation

            """
            - use current generation(population) to generate prompt
            - prompt the model to generate new generation
            - parse response
            """
            newGenPrompt = PRManager.getNewGenerationPrompt(population, pointsCoordinatesPairs, 30)
            newGenResponse = self.model.run(newGenPrompt)
            print(f"""___________________________________________________________________________
                {newGenResponse}
                """)
            
            newGenerationTraces = PRManager.parseNewGeneration(newGenResponse, nodeCount=NODE_COUNT)
            # TODO: ADD logging

            # get the lengths of the new generation traces
            newPopulation = []
            for trace in newGenerationTraces:
                length = problem.trace_tours([trace])
                newPopulation.append((trace, length[0]))
            
            # sort new population by length descendingly
            newPopulation = sorted(newPopulation, key=lambda x: x[1], reverse=True)
            
            if len(newPopulation) > 0:
                if newPopulation[-1][1] >= bestSolutionLength:
                    worseIterations += 1
                else:
                    worseIterations = 0
                    
            if worseIterations > 20:
                worseIterations = 0
                if currentModelTemperature < 2:
                    currentModelTemperature += 0.05
                    populationSize += 2
            
            newPopulation = list(filter(lambda x: all(item[0]!=x[0] for item in population), newPopulation))
            
                
            population.extend(newPopulation)
            # sort the population by the tour lengths descendingly
            population = sorted(population, key=lambda x: x[1], reverse=True)
            population = population[-populationSize:]
            print(f"""
                  {population}
                  """)
            
            bestSolutionLength = population[-1][1] if  population[-1][1] < bestSolutionLength else bestSolutionLength
        # if the optimal distance is not reached, return the best tour and the generation number
        return population[-1][0], MAX_GENERATIONS
