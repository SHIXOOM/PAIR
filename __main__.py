from src.ExperimentRunner import ExperimentRunner
from src.Models.Gemini import Gemini
from src.PopulationInitializers.RandomInitializer import RandomInitializer
from src.PopulationInitializers.SAPopulationInitializer import (
    SAPopulationInitializer as SAInitializer,
)
from src.Solvers.TinderMatchingSolver import TinderMatchingSolver


def get_user_input(prompt):
    return input(prompt)


def select_option(options, prompt):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = int(get_user_input("Enter the number of your choice: "))
    return options[choice - 1]


def get_experiment_inputs():
    problem_name = get_user_input("Enter the name of the problem: ")
    tsp_path = get_user_input("Enter the path to the problem file: ")
    optimal_distance = float(
        get_user_input("Enter the optimal solution for the problem: ")
    )

    solvers = ["TinderMatching"]
    solver_name = select_option(solvers, "Select the solver to use:")

    models = [
        "gemini-2.0-flash-thinking-exp-1219",
        "gemini-2.0-flash-exp",
        "gemini-2.5-flash-preview-04-17",
    ]
    model_name = select_option(models, "Select the model to use:")

    population_initializers = ["simulated-annealing", "random"]
    population_initializer_name = select_option(
        population_initializers, "Select the population initializer to use:"
    )

    return {
        "problem_name": problem_name,
        "tsp_path": tsp_path,
        "optimal_distance": optimal_distance,
        "solver_name": solver_name,
        "model_name": model_name,
        "population_initializer_name": population_initializer_name,
    }


def initialize_experiment(inputs):
    """Sets Experiment up based on given inputs"""

    """ Can be refactored using Factory pattern but 
        for simplicity, we settled for current approach,
        if same logic is needed elsewhere, this should
        be refactored. """

    """ Initialize population initializer """
    if inputs["population_initializer_name"] == "simulated-annealing":
        population_initializer = SAInitializer()
    elif inputs["population_initializer_name"] == "random":
        population_initializer = RandomInitializer()
    else:
        raise Exception("Population initializer not found.")

    """ Initialize model """
    if inputs["model_name"] == "gemini-2.0-flash-thinking-exp-1219":
        model = Gemini("system_prompt", 1, inputs["model_name"])
    elif inputs["model_name"] == "gemini-2.0-flash-exp":
        model = Gemini("system_prompt", 1, inputs["model_name"])
    elif inputs["model_name"] == "gemini-2.5-flash-preview-04-17":
        model = Gemini("system_prompt", 1, inputs["model_name"])
    else:
        raise Exception("Model not found")

    """ Initialize solver"""
    if inputs["solver_name"] == "TinderMatching":
        solver = TinderMatchingSolver(model, population_initializer)
    else:
        raise Exception("Solver not found")

    return ExperimentRunner(
        inputs["problem_name"],
        inputs["tsp_path"],
        inputs["optimal_distance"],
        solver,
        model,
    )


def main():
    inputs = get_experiment_inputs()
    experiment_runner = initialize_experiment(inputs)
    experiment_runner.run()


if __name__ == "__main__":
    main()
