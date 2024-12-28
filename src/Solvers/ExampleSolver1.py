from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model
from src.PopulationInitializers import SAPopulationInitializer, PopulationInitializer

class ExampleSolver1(LLMTSPSolver):
    def __init__(self, model: Model, population_initializer: PopulationInitializer):
        super().__init__(model, population_initializer)
        self.population_initializer = population_initializer
        print(f"Solver created with model: {model}")

    def solve(self, problem):
        

        population = self.population_initializer.initialize(30, problem)
         
        print(f"ExampleSolver1 solving problem with initial population: ",population)