from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.PopulationInitializers.PopulationInitializer import PopulationInitializer
from src.DataManager import DataManger
from src.Models.Model import Model


class ExperimentRunner:
    def __init__(self,
                problem_name:str,
                problem_file_path:str,
                solver: LLMTSPSolver,
                model:Model,
                ):

        # initialize member variables
        self.solver = solver
        self.problem_name = problem_name
        self.problem_file_path = problem_file_path
        self.model = model
        
        # load ts problem
        self.problem = DataManger.load_problem(problem_file_path)

        print(f"ExperimentRunner created with solver: {solver}")
    
    def run(self):
        print("running experiment")

        # run the solver
        self.solver.solve(self.problem)
        print("experiment finished")