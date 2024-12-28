from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model
from src.PopulationInitializers.PopulationInitializer import  PopulationInitializer
from src.PromptResponseManager.PromptResponseManager import PromptResponseManager as PRManager


class ExampleSolver1(LLMTSPSolver):
    def __init__(self, model: Model, population_initializer: PopulationInitializer):
        super().__init__(model, population_initializer)

        self.population_initializer = population_initializer
        
    def solve(self, problem):
        # initialize population
        population = self.population_initializer.initialize(30, problem)
         
        # solve the problem
        MAX_GENERATIONS = 250
        for generation in range(MAX_GENERATIONS):
            points_coords = problem.get_nodes()
            print(points_coords)
            
            new_gen_prompt = PRManager.getNewGenerationPrompt(population, points_coords)
            new_generation = self.model.run(new_gen_prompt)
             
            
            pass
