from src.PopulationInitializers.SAPopulationInitializer import SAPopulationInitializer
from src.ExperimentRunner import ExperimentRunner
from src.Models.Gemini import Gemini
from src.Solvers.TinderMatchingSolver import TinderMatchingSolver
import argparse


def main():
    # Input taking
    parser = argparse.ArgumentParser(description='Run the experiment with specified parameters.')
    parser.add_argument('--problem_name',
                        type=str, default="A",
                        help='Name of the problem')
    parser.add_argument('--solver_name',
                        type=str, default="solver1", choices=['solver1'],
                        help='Name of the solver to use')
    parser.add_argument('--model_name',
                        type=str, default="gemini", choices=['gemini'],
                        help='Name of the model to use')
    parser.add_argument('--pop_init',
                        type=str, default="sa", choices=['sa'],
                        help='Name of the population initializer to use')
    parser.add_argument('--tsp_path',
                        type=str, required=True,
                        help='Path to the problem file')
    parser.add_argument('--optimal_distance',
                        default=0, help="optimal solution for the problem")

    args = parser.parse_args()

    problemName = args.problem_name
    problemFilePath = args.tsp_path
    solverName = args.solver_name
    modelName = args.model_name
    populationInitializerName = args.pop_init
    optimalSolution = args.optimal_distance

    # Create Solver and Model Instance
    # technically, we can use a factory pattern here
    # but for simplicity, we will just use if-else
    # if same logic is needed in another place, it should be replaced by factory pattern

    if populationInitializerName == "sa":
        populationInitializer = SAPopulationInitializer()
    else:
        raise Exception("population analyzer not found. refer to readme.md")

    if modelName == "gemini":
        model = Gemini("system_prompt", 1)
    else:
        raise Exception("Model not found")

    if solverName == "solver1":
        solver = TinderMatchingSolver(model, populationInitializer)
    else:
        raise Exception("Solver not found")

    # ExperimentRunner
    experiment_runner = ExperimentRunner(problemName, problemFilePath, optimalSolution, solver, model)
    experiment_runner.run()


if __name__ == '__main__':
    main()
