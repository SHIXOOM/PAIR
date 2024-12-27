from src.Solvers.LLMTSPSolver import LLMTSPSolver
from src.Models.Model import Model

class ExampleSolver1(LLMTSPSolver):
    """
    Example concrete implementation of the LLMTSPSolver class
    TODO: Remove. Not an actual implementation
    """

    def __init__(self, model: Model):
        super().__init__(model)
        print(f"Solver created with model: {model}")

    def solve(self, problem):
        print("Solving problem:", problem)
        return "solution"