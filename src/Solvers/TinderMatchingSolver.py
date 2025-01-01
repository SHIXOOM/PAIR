import tsplib95
from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model
from src.PopulationInitializers.PopulationInitializer import PopulationInitializer
from src.PromptResponseManager.PromptResponseManager import PromptResponseManager as PRManager
from src.DataManager import DataManager

import pandas as pd

class TinderMatchingSolver(LLMTSPSolver):
    def __init__(self, model: Model, population_initializer: PopulationInitializer):
        super().__init__(model, population_initializer)

        self.population_initializer = population_initializer

    def solve(self, problem, problem_optimal_distance=301) -> tuple[list[int], int]:
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

        populationSize = 16
        currentModelTemperature = 1
        population = self.population_initializer.initialize(populationSize, problem)

        """ Configure model """
        systemPrompt = PRManager.getSystemPrompt(populationSize=populationSize)
        self.model.configure(systemPrompt, currentModelTemperature)

        pointsCoordinatesPairs = {i: (j[0], j[1]) for i, j in problem.node_coords.items()}
        bestSolutionLength = population[-1][1]
        
        worseIterations  = 0
        
        #####
        problem_optimal_distance = 252
        iterationPath = "rue_15_3.csv"
        iterationsDataStructure = {"model": [], "node number": [],
                           "problem": [], "iteration": [], "distance": [],
                           "optimal distance": [], "gap": [], "temperature": [], "population size": [], "variance": []}
        #####
        for generation in range(1, MAX_GENERATIONS + 1):
            variance = DataManager.getGenerationVariance(populationDistances = [x[1] for x in population])
            ############################################################ temporary csv storage:
            iterationsDataStructure["model"].append("gemini-2.0-flash-thinking-exp")
            iterationsDataStructure["node number"].append(NODE_COUNT)
            iterationsDataStructure["problem"].append(problem.name)
            iterationsDataStructure["iteration"].append(generation)
            iterationsDataStructure["distance"].append(bestSolutionLength)
            iterationsDataStructure["optimal distance"].append(problem_optimal_distance)
            iterationsDataStructure["gap"].append(DataManager.getOptimalityGap(bestSolutionLength, problem_optimal_distance))
            iterationsDataStructure["temperature"].append(currentModelTemperature)
            iterationsDataStructure["population size"].append(populationSize)
            iterationsDataStructure["variance"].append(variance)
            ############################################################ 
            
            print(f"""
                Best sol: {bestSolutionLength}
                Generation: {generation}
                Temperature: {currentModelTemperature}
                Population Size: {populationSize}
                _________________________________________________________________________________
                """)
            if population[-1][1] == problem_optimal_distance:
                ############################################################
                pd.DataFrame(iterationsDataStructure).to_csv(iterationPath)
                ############################################################
                return population[-1][0], generation

            """
            - use current generation(population) to generate prompt
            - prompt the model to generate new generation
            - parse response
            """
            newGenPrompt = PRManager.getNewGenerationPrompt(population, pointsCoordinatesPairs, 30)
            newGenResponse = self.model.run(newGenPrompt, nodeCount = NODE_COUNT)
            print(f"""___________________________________________________________________________
                {newGenResponse}
                """)
            
            # get new generation traces
            newGenerationTraces = PRManager.parseNewGeneration(newGenResponse, nodeCount=NODE_COUNT)
            # TODO: ADD logging

            # get the lengths of the new generation traces
            newPopulation = []
            for trace in newGenerationTraces:
                length = problem.trace_tours([trace])
                newPopulation.append((trace, length[0]))
            
            # sort new population by length descendingly
            newPopulation = sorted(newPopulation, key=lambda x: x[1], reverse=True)
            
            # check if the new population has individuals
            if len(newPopulation) > 0:
                # if the new population's best individual is worse than the best solution, increment worseIterations
                if newPopulation[-1][1] >= bestSolutionLength:
                    worseIterations += 1
                # reset, you broke the cycle
                else:
                    worseIterations = 0
            
            # if we passed 20 worse iterations, we need to increase the model's temperature and population size
            if worseIterations > 20:
                worseIterations = 0
                if currentModelTemperature < 2:
                    currentModelTemperature += 0.05
                    self.model.configure(systemPrompt, currentModelTemperature)
                    populationSize += 2
            
            # remove duplicates from the new population
            newPopulation = list(filter(lambda x: all(item[0]!=x[0] for item in population), newPopulation))
            
            # add the new population to the current population
            population.extend(newPopulation)
            # sort the population by the tour lengths descendingly
            population = sorted(population, key=lambda x: x[1], reverse=True)
            # keep the best populationSize individuals
            population = population[-populationSize:]
            print(f"""
                  {population}
                  """)        
            bestSolutionLength = population[-1][1] if  population[-1][1] < bestSolutionLength else bestSolutionLength
            ############################################################
            
            ############################################################
        # if the optimal distance is not reached, return the best tour and the generation number
        
        ############################################################ temporary csv storage:
        pd.DataFrame(iterationsDataStructure).to_csv(iterationPath)
        ############################################################ 
        
        return population[-1][0], MAX_GENERATIONS
