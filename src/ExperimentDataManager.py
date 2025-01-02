import tsplib95
import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil
from typing import Dict, Any


class ExperimentDataManager:
    """Manages experiment data, logging, and file operations for TSP experiments."""

    DATA_DIR = Path("data")

    def __init__(self, problemFilePath: str, problemName: str, modelName: str,
                 optimalDistance: float, solverName: str = "TinderMatching"):
        # Initialize basic properties
        self._init_properties(problemFilePath, problemName, modelName, solverName, optimalDistance)

        # Setup directory structure and files
        self._setup_directory_structure()
        self._init_log_file()

    def _init_properties(self, problemFilePath: str, problemName: str,
                         modelName: str, solverName: str, optimalDistance: float) -> None:
        """Initialize instance properties"""
        self.problem = tsplib95.load(problemFilePath)
        self.problemFilePath = Path(problemFilePath)
        self.problemName = problemName
        self.modelName = modelName
        self.solverName = solverName
        self.nodeCount = self.problem.dimension
        self.optimalDistance = optimalDistance
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    def _setup_directory_structure(self) -> None:
        """Setup directory structure and copy problem file if needed"""
        self.problem_dir = self.DATA_DIR / self.problemName
        problem_dir_exists = self.problem_dir.exists()
        self.problem_dir.mkdir(parents=True, exist_ok=True)

        if not problem_dir_exists:
            self._copy_problem_file()

    def _copy_problem_file(self) -> None:
        """Copy the TSP problem file to the problem directory"""
        shutil.copy2(self.problemFilePath, self.problem_dir / self.problemFilePath.name)

    def _init_log_file(self) -> None:
        """Initialize the log file"""
        self.log_file = self.problem_dir / f"{self._get_file_prefix()}_log.txt"
        with open(self.log_file, 'w') as f:
            f.write(f"Experiment Log: {self.timestamp}\n")
            f.write("=" * 80 + "\n")

    def _get_file_prefix(self) -> str:
        """Generate consistent file prefix for all experiment files"""
        return f"{self.problemName}_{self.modelName}_{self.solverName}_{self.timestamp}"

    def _get_iteration_data(self, generationNumber: int, distance: float,
                            modelTemperature: float, generationVariance: float,
                            populationSize: int, optimalityGap: float) -> Dict[str, list]:
        """Prepare iteration data for CSV storage"""
        return {
            'model': [self.modelName],
            'node number': [self.nodeCount],
            'problem': [self.problemName],
            'iteration': [generationNumber],
            'distance': [distance],
            'optimal distance': [self.optimalDistance],
            'gap': [optimalityGap],
            'temperature': [modelTemperature],
            'population size': [populationSize],
            'variance': [generationVariance]
        }

    def _write_to_csv(self, file_path: Path, data: Dict[str, Any]) -> None:
        """Write data to CSV file"""
        df = pd.DataFrame(data)
        if not file_path.exists():
            df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)

    def _log_to_file(self, message: str) -> None:
        """Append message to log file"""
        with open(self.log_file, 'a') as f:
            f.write(f"{message}\n")

    """ Public interface methods """

    def addIterationData(self, generationNumber: int, distance: int,
                         modelTemperature: float, generationVariance: float,
                         populationSize: int, optimalityGap: float) -> None:
        file_path = self.problem_dir / f"{self._get_file_prefix()}_iterations.csv"
        data = self._get_iteration_data(generationNumber, distance, modelTemperature,
                                        generationVariance, populationSize, optimalityGap)
        self._write_to_csv(file_path, data)

    def _get_solution_data(self, solution: list, distance: float,
                           optimalDistance: float, optimalityGap: float,
                           success_step='None') -> Dict[str, list]:
        """Prepare solution data for CSV storage"""
        return {
            'model': [self.modelName],
            'problem': [self.problemName],
            'node_count': [self.nodeCount],
            'found_distance': [distance],
            'optimal_distance': [optimalDistance],
            'success_step': [success_step],
            'optimality_gap': [optimalityGap],
            'solution_path': [','.join(map(str, solution))],
            'timestamp': [self.timestamp]
        }

    def saveSolution(self, solution: list, distance: float,
                     optimalDistance: float, optimalityGap: float,
                     success_step='None') -> None:
        """Save solution data in CSV format"""
        file_path = self.problem_dir / f"{self._get_file_prefix()}_solution.csv"
        data = self._get_solution_data(solution, distance, optimalDistance, optimalityGap,success_step)
        self._write_to_csv(file_path, data)

    def logGenerationStatus(self, bestSolution: float, generation: int,
                            temperature: float, populationSize: int):
        message = f"""
Best sol: {bestSolution}
Generation: {generation}
Temperature: {temperature}
Population Size: {populationSize}
_________________________________________________________________________________
"""
        self._log_to_file(message)

    def logModelResponse(self, response: str):
        message = f"""___________________________________________________________________________
{response}
"""
        self._log_to_file(message)

    def logPopulation(self, population: list):
        message = f"""
{population}
"""
        self._log_to_file(message)

    def logError(self, error: str):
        message = f"ERROR: {error}"
        self._log_to_file(message)
