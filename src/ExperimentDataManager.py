import tsplib95
import pandas as pd
from pathlib import Path


class ExperimentDataManager:
    # Base directory for all data files
    DATA_DIR = Path("data")

    def __init__(self, problemFilePath: str, problemName: str, modelName: str, optimalDistance: float):
        """
            loads a tsp problem from a .tsp file
            Args:
                problemFilePath: the path to the .tsp file
        """
        self.problem: tsplib95.models.StandardProblem = tsplib95.load(problemFilePath)
        self.problemFilePath = problemFilePath
        self.problemName = problemName
        self.modelName = modelName
        self.nodeCount = self.problem.dimension
        self.optimalDistance = optimalDistance

    def getProblem(self) -> tsplib95.models.StandardProblem:
        return self.problem

    def addIterationData(self,
                         generationNumber: int, distance: int,
                         modelTemperature: float, generationVariance: float,
                         populationSize: int, optimalityGap: float
                         ):
        """
        Logs iteration data to a CSV file specific to the problem
        """
        ExperimentDataManager._ensure_data_dir()
        file_path = ExperimentDataManager._get_iterations_file(self.problemName)

        data = {
            'model': [self.modelName],
            'node number': [self.nodeCount],
            'problem': [self.problemName],
            'iteration': [generationNumber],
            'distance': [distance],
            'optimal distance': [self.optimalDistance],
            'gap': [optimalityGap],
            'temperature': [modelTemperature],
            'population size': [populationSize],
            'generation': [generationVariance]
        }

        df = pd.DataFrame(data)
        if not file_path.exists():
            df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)

    def saveSolution(self,
                     solution: list, distance: int,
                     optimalDistance: int, optimalityGap: int):
        """
        Saves the final solution and statistics of an experiment
        """
        ExperimentDataManager._ensure_data_dir()
        file_path = ExperimentDataManager._get_solution_file(self.problemName)

        with open(file_path, 'w') as f:
            f.write(f"Problem: {self.problemName}\n")
            f.write(f"Found Distance: {distance}\n")
            f.write(f"Optimal Distance: {optimalDistance}\n")
            f.write(f"Optimality Gap: {optimalityGap}%\n")
            f.write(f"Solution Path: {' -> '.join(map(str, solution))}\n")

    @staticmethod
    def _ensure_data_dir():
        """Creates the data directory if it doesn't exist"""
        ExperimentDataManager.DATA_DIR.mkdir(exist_ok=True)

    @staticmethod
    def _get_iterations_file(problem_name: str) -> Path:
        """Returns the path for the iterations log file"""
        return ExperimentDataManager.DATA_DIR / f"{problem_name}_iterations.csv"

    @staticmethod
    def _get_solution_file(problem_name: str) -> Path:
        """Returns the path for the solution file"""
        return ExperimentDataManager.DATA_DIR / f"{problem_name}_solution.txt"
