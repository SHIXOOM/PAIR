from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.ExperimentDataManager import ExperimentDataManager
from src.Models.Model import Model


class ExperimentRunner:
    def __init__(self,
                 problemName: str,
                 problemFilePath: str,
                 problemOptimalDistance: float,
                 solver: LLMTSPSolver,
                 model: Model,
                 ):
        # initialize member variables
        self.solver = solver
        self.problemName = problemName
        self.problemOptimalDistance = problemOptimalDistance
        self.problemFilePath = problemFilePath
        self.model = model

        # load tsp problem
        self.expDataManager = \
            ExperimentDataManager(problemFilePath, problemName, self.model.modelName, problemOptimalDistance)
        self.problem = self.expDataManager.problem

        print(f"ExperimentRunner created with solver: {solver}")

    def run(self):
        print("running experiment")

        # run the solver
        self.solver.solve(self.expDataManager)
        print("experiment finished")
