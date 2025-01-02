import time

from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model
from src.PopulationInitializers.PopulationInitializer import PopulationInitializer
from src.PromptResponseManager.PromptResponseManager import PromptResponseManager as PRManager
from src.ExperimentDataManager import ExperimentDataManager

import numpy as np


class TinderMatchingSolver(LLMTSPSolver):
    def __init__(self, model: Model, population_initializer: PopulationInitializer):
        super().__init__(model, population_initializer)

        self.population_initializer = population_initializer

    def solve(self, expDataManager: ExperimentDataManager) -> tuple[list[int], float]:
        problem = expDataManager.problem

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

        problem_optimal_distance = expDataManager.optimalDistance
        optimalityGap = 9999
        for generation in range(1, MAX_GENERATIONS + 1):

            """ Saving Generation Data """
            variance = TinderMatchingSolver._getGenerationVariance([x[1] for x in currentPopulation])
            optimalityGap = TinderMatchingSolver._calculateOptimalityGap(bestSolutionLength, problem_optimal_distance)

            expDataManager.addIterationData(generation, bestSolutionLength,
                                            currentModelTemperature, variance,
                                            populationSize, optimalityGap)

            """ Log Generation Data """
            expDataManager.logGenerationStatus(bestSolutionLength, generation,
                                               currentModelTemperature, populationSize)

            """ Exit if reached optimal distance """
            if currentPopulation[-1][1] == problem_optimal_distance:
                expDataManager.saveSolution(currentPopulation[-1][0], bestSolutionLength, problem_optimal_distance,
                                            optimalityGap, generation)
                return currentPopulation[-1][0], generation

            """
            - use current generation(population) to generate prompt
            - prompt the model to generate new generation
            - parse response
            """
            # get new population
            newPopulation = self._getNewPopulation(problem, currentPopulation,
                                                   NODE_COUNT, pointsCoordinatesPairs,
                                                   populationSize, expDataManager)

            # update temperature and population size
            currentModelTemperature, populationSize, worseIterations = self._updateTemperatureAndPopulationSize(
                newPopulation, bestSolutionLength,
                currentModelTemperature, systemPrompt,
                populationSize, worseIterations)

            # combine populations
            currentPopulation = TinderMatchingSolver._combinePopulations(currentPopulation, newPopulation,
                                                                         populationSize)

            expDataManager.logPopulation(currentPopulation)

            bestSolutionLength = currentPopulation[-1][1] if currentPopulation[-1][
                                                                 1] < bestSolutionLength else bestSolutionLength

        # if the optimal distance is not reached, return the best tour and the generation number
        expDataManager.saveSolution(currentPopulation[-1][0], bestSolutionLength, problem_optimal_distance,
                                    optimalityGap)
        return currentPopulation[-1][0], MAX_GENERATIONS

    """ Internal Helper Methods """

    def _getNewPopulation(self, problem, currentPopulation, NODE_COUNT, pointsCoordinatesPairs, populationSize,
                          expDataManager: ExperimentDataManager) -> list[
        tuple[list[int], float]]:

        # get new generation prompt
        newGenPrompt = PRManager.getNewGenerationPrompt(currentPopulation, pointsCoordinatesPairs, populationSize)

        # parse new generation traces
        maxRetries = 10
        while True:
            try:
                # get new generation response from the llm
                newGenResponse = self.model.run(newGenPrompt)
                expDataManager.logModelResponse(newGenResponse)

                newGenerationTraces = PRManager.parseNewGeneration(newGenResponse, nodeCount=NODE_COUNT)
                break
            except Exception as e:
                maxRetries -= 1
                if maxRetries == 0: raise e
                expDataManager.logError(f"Error parsing response: {e}")
                time.sleep(1)

        # calculate the lengths of the new generation traces
        newPopulation = []
        for trace in newGenerationTraces:
            length = round(problem.trace_tours([trace])[0], 3)
            newPopulation.append((trace, length))

        # remove duplicates from the new population
        newPopulation = list(filter(lambda newIndividual: all(
            newIndividual[0] != currentIndividual[0] for currentIndividual in currentPopulation), newPopulation))

        # sort new population by length descendingly
        newPopulation = sorted(newPopulation, key=lambda x: x[1], reverse=True)

        return newPopulation

    def _updateTemperatureAndPopulationSize(self, newPopulation, bestSolutionLength, currentModelTemperature,
                                            systemPrompt, populationSize, worseIterations) -> tuple[float, int, int]:
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

    @staticmethod
    def _calculateOptimalityGap(minDistance: float, optimalDistance: float) -> float:
        return round((((minDistance - optimalDistance) / optimalDistance) * 100), 2)

    @staticmethod
    def _combinePopulations(currentPopulation, newPopulation, populationSize) -> list[tuple[list[int], float]]:
        # add the new population to the current population
        currentPopulation.extend(newPopulation)

        # sort the population by the tour lengths in descending order
        currentPopulation = sorted(currentPopulation, key=lambda x: x[1], reverse=True)

        # keep the best populationSize individuals
        currentPopulation = currentPopulation[-populationSize:]

        return currentPopulation

    @staticmethod
    def _getGenerationVariance(populationDistances: list[float]) -> float:
        return float(np.var(populationDistances))
