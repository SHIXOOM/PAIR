import tsplib95

import pandas as pd
import numpy as np

class DataManager:
    """
    A class to manage all interactions with files
    Serves more like a namespace or a utility class for
    file operations.

    That is, it's a functional encapsulation of file operations
    """

    @staticmethod
    def load_problem(file_path: str) -> tsplib95.models.StandardProblem:
        """
        loads a tsp problem from a .tsp file

        Args:
            file_path: the path to the .tsp file

        Returns:
            a tsplib95.models.StandardProblem object representing the problem
        """
        problem = tsplib95.load(file_path)
        return problem

    @staticmethod
    def getOptimalityGap(minDistance: float, optimalDistance: float) -> float:
        return round((((minDistance - optimalDistance) / optimalDistance) * 100), 2)

    @staticmethod
    def getGenerationVariance(populationDistances: list[float]) -> float:
        return float(np.var(populationDistances))

    @staticmethod
    def logIteration(modelName: str, nodeCount: int, problemName: str, iteration: int, distance: float, optimalDistance: float, variance: float, temperature: float) -> bool:
        pass
