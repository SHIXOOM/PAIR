from src.ExperimentRunner import ExperimentRunner
from src.Models.Gemini import Gemini
from src.Solvers.ExampleSolver1 import ExampleSolver1

def main():
   
    # Input taking
    # TODO: This should be replaced by a proper input mechanism
    problem_name = "A"
    problem_file_path =  "path to problem file"
    solver_name = "solver1" 
    model_name = "gemini"

    # Create Solver and Model Instance
    # technically, we can use a factory pattern here
    # but for simplicity, we will just use if-else
    # if same logic is needed in another place, it should be replaced by factory pattern

    if(model_name == "gemini"):
        model = Gemini("system_prompt", 1)
    else:
        raise Exception("Model not found")

    if(solver_name == "solver1"):
        solver = ExampleSolver1(model)
    else:
        raise Exception("Solver not found")


    # ExperimentRunner
    experiment_runner = ExperimentRunner(problem_name, problem_file_path, solver, model)


if __name__ == '__main__':
    main()