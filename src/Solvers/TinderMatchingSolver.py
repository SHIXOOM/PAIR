import tsplib95
from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model
from src.PopulationInitializers.PopulationInitializer import PopulationInitializer
from src.PromptResponseManager.PromptResponseManager import PromptResponseManager as PRManager
from src.DataManager import DataManager

import logging
import pandas as pd

class TinderMatchingSolver(LLMTSPSolver):
    def __init__(self, model: Model, population_initializer: PopulationInitializer):
        super().__init__(model, population_initializer)

        self.population_initializer = population_initializer

    def solve(self, problem, problem_optimal_distance=301) -> tuple[list[int], float]:
        """
        Args:
            problem: tsp problem instance
            problem_optimal_distance(optional): problem optimal solution length
        Returns:
            tuple[list[int],int]
            best found solution, generation number found in
        """

        
        """ Set the maximum number of generations """
        MAX_GENERATIONS = 250
        
        """ Set the number of nodes in the problem """
        NODE_COUNT = problem.dimension

        populationSize = 16
        
        """ Configure model with the system prompt and temperature """
        systemPrompt = PRManager.getSystemPrompt(populationSize=populationSize)
        currentModelTemperature = 1
        self.model.configure(systemPrompt, currentModelTemperature)
        
        
        """ Initialize population and get the best solution length """
        currentPopulation = self.population_initializer.initialize(populationSize, problem)
        bestSolutionLength = currentPopulation[-1][1]
        
        

        """ Get points coordinates pairs """
        pointsCoordinatesPairs = {i: (j[0], j[1]) for i, j in problem.node_coords.items()}
        
        
        
        """ Counter for how many consecutive bad iterations occured
        to update the model's temperature and population size """
        worseIterations = 0
        
        #####
        problem_optimal_distance = 350
        iterationPath = "rue_15_4.csv"
        iterationsDataStructure = {"model": [], "node number": [],
                           "problem": [], "iteration": [], "distance": [],
                           "optimal distance": [], "gap": [], "temperature": [], "population size": [], "variance": []}
        #####
        
        for generation in range(1, MAX_GENERATIONS + 1):
            ############################################################ temporary csv storage:
            variance = DataManager.getGenerationVariance(populationDistances = [x[1] for x in currentPopulation])
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
            if currentPopulation[-1][1] == problem_optimal_distance:
                ############################################################
                pd.DataFrame(iterationsDataStructure).to_csv(iterationPath)
                ############################################################
                return currentPopulation[-1][0], generation

            """
            - use current generation(population) to generate prompt
            - prompt the model to generate new generation
            - parse response
            """
            # get new population
            newPopulation = self.getNewPopulation(problem, currentPopulation,
                                                  NODE_COUNT, pointsCoordinatesPairs,
                                                  populationSize)
            
            # update temperature and population size
            currentModelTemperature, populationSize, worseIterations = self.updateTemperatureAndPopulationSize(newPopulation, bestSolutionLength,
                                                                      currentModelTemperature, systemPrompt,
                                                                      populationSize, worseIterations)
            
            # combine populations
            currentPopulation = self.combinePopulations(currentPopulation, newPopulation,
                                                        populationSize)
            
            print(f"""
                  {currentPopulation}
                  """)        
            bestSolutionLength = currentPopulation[-1][1] if currentPopulation[-1][1] < bestSolutionLength else bestSolutionLength
            
            
        # if the optimal distance is not reached, return the best tour and the generation number
        
        ############################################################ temporary csv storage:
        pd.DataFrame(iterationsDataStructure).to_csv(iterationPath)
        ############################################################ 
        
        return currentPopulation[-1][0], MAX_GENERATIONS


    def getNewPopulation(self, problem, currentPopulation, NODE_COUNT, pointsCoordinatesPairs, populationSize) -> list[tuple[list[int], float]]:
        # get new generation prompt
        newGenPrompt = PRManager.getNewGenerationPrompt(currentPopulation, pointsCoordinatesPairs, populationSize)
        
        # get new generation response from the llm
        newGenResponse = self.model.run(newGenPrompt, nodeCount = NODE_COUNT)
        print(f"""___________________________________________________________________________
            {newGenResponse}
            """)
        
        # parse new generation traces
        newGenerationTraces = PRManager.parseNewGeneration(newGenResponse, nodeCount=NODE_COUNT)
        # TODO: ADD logging

        # calculate the lengths of the new generation traces
        newPopulation = []
        for trace in newGenerationTraces:
            length = round(problem.trace_tours([trace])[0], 3)
            newPopulation.append((trace, length))
        
        # remove duplicates from the new population
        newPopulation = list(filter(lambda newIndividual: all(newIndividual[0] != currentIndividual[0] for currentIndividual in currentPopulation), newPopulation))
        
        # sort new population by length descendingly
        newPopulation = sorted(newPopulation, key=lambda x: x[1], reverse=True)
        
        return newPopulation
        
        
    def updateTemperatureAndPopulationSize(self, newPopulation, bestSolutionLength, currentModelTemperature, systemPrompt, populationSize, worseIterations) -> tuple[float, int, int]:
        # check if the new population has individuals
        if len(newPopulation) > 0:
            # if the new population's best individual is worse than the best solution, increment worseIterations
            if newPopulation[-1][1] >= bestSolutionLength:
                worseIterations += 1
            # reset, you broke the cycle of no positive improvement
            else:
                worseIterations = 0
        
        # if we passed 20 worse iterations, we need to increase the model's temperature and population size
        if worseIterations > 20:
            worseIterations = 0
            if currentModelTemperature < 2:
                currentModelTemperature += 0.05
                self.model.configure(systemPrompt, currentModelTemperature)
                populationSize += 2
                
        return round(currentModelTemperature, 3), populationSize, worseIterations
    
    
    def combinePopulations(self, currentPopulation, newPopulation, populationSize) -> list[tuple[list[int], float]]:
        # add the new population to the current population
        currentPopulation.extend(newPopulation)
        
        # sort the population by the tour lengths descendingly
        currentPopulation = sorted(currentPopulation, key=lambda x: x[1], reverse=True)
        
        # keep the best populationSize individuals
        currentPopulation = currentPopulation[-populationSize:]
        
        return currentPopulation


