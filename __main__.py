from src.PopulationInitializers.RandomInitializer import RandomInitializer
from src.PopulationInitializers.SAPopulationInitializer import SAPopulationInitializer as SAInitializer
from src.ExperimentRunner import ExperimentRunner
from src.Models.Gemini import Gemini
from src.Solvers.TinderMatchingSolver import TinderMatchingSolver


def main():
    # Input taking
    problem_name = input("Enter the name of the problem: ")
    tsp_path = input("Enter the path to the problem file: ")
    optimal_distance = float(input("Enter the optimal solution for the problem : "))

    # Prompt user to select solver
    solvers = ["TinderMatching"]
    print("Select the solver to use:")
    for i, solver in enumerate(solvers, 1):
        print(f"{i}. {solver}")
    solver_choice = int(input("Enter the number of the solver: "))
    solver_name = solvers[solver_choice - 1]

    # Prompt user to select model
    models = ["gemini-2.0-flash-thinking"]
    print("Select the model to use:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    model_choice = int(input("Enter the number of the model: "))
    model_name = models[model_choice - 1]

    # Prompt user to select population initializer
    population_initializers = ["simulated-annealing", "random"]
    print("Select the population initializer to use:")
    for i, pop_init in enumerate(population_initializers, 1):
        print(f"{i}. {pop_init}")
    pop_init_choice = int(input("Enter the number of the population initializer: "))
    population_initializer_name = population_initializers[pop_init_choice - 1]

    # Create Solver and Model Instance
    if population_initializer_name == "simulated-annealing":
        population_initializer = SAInitializer()
    elif population_initializer_name == "random":
        population_initializer = RandomInitializer()
    else:
        raise Exception("Population initializer not found.")

    if model_name == "gemini-2.0-flash-thinking":
        model = Gemini("system_prompt", 1,model_name)
    else:
        raise Exception("Model not found")

    if solver_name == "TinderMatching":
        solver = TinderMatchingSolver(model, population_initializer)
    else:
        raise Exception("Solver not found")

    # ExperimentRunner
    experiment_runner = ExperimentRunner(problem_name, tsp_path, optimal_distance, solver, model)
    experiment_runner.run()


if __name__ == '__main__':
    main()
