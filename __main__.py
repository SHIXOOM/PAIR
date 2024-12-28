from src.PopulationInitializers.SAPopulationInitializer import SAPopulationInitializer
from src.ExperimentRunner import ExperimentRunner
from src.Models.Gemini import Gemini
from src.Solvers.ExampleSolver1 import ExampleSolver1
import argparse

def main():
   
    # Input taking
    parser = argparse.ArgumentParser(description='Run the experiment with specified parameters.')
    parser.add_argument('--problem_name', type=str,  default="A", help='Name of the problem')
    parser.add_argument('--tsp_path', type=str, required=True, help='Path to the problem file')
    parser.add_argument('--solver_name', type=str,  default="solver1", choices=['solver1'], help='Name of the solver to use')
    parser.add_argument('--model_name', type=str, default="gemini", choices=['gemini'], help='Name of the model to use')
    parser.add_argument('--pop_init', type=str, default="sa", choices=['sa'], help='Name of the population initializer to use')

    args = parser.parse_args()

    problem_name = args.problem_name
    problem_file_path = args.tsp_path
    solver_name = args.solver_name
    model_name = args.model_name
    population_initializer_name = args.pop_init

    # Create Solver and Model Instance
    # technically, we can use a factory pattern here
    # but for simplicity, we will just use if-else
    # if same logic is needed in another place, it should be replaced by factory pattern

    if(population_initializer_name == "sa"):
        population_initializer = SAPopulationInitializer()

    if(model_name == "gemini"):
        model = Gemini("system_prompt", 1)
    else:
        raise Exception("Model not found")

    if(solver_name == "solver1"):
        solver = ExampleSolver1(model, population_initializer)
    else:
        raise Exception("Solver not found")


    # ExperimentRunner
    experiment_runner = ExperimentRunner(problem_name, problem_file_path, solver, model)
    experiment_runner.run()


if __name__ == '__main__':
    main()