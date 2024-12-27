from abc import abstractmethod
from src.Models.Model import Model


class LLMTSPSolver:
    """
    Abstract base class for LLM TSP Solvers
    Different solvers can use different LLMs or different
    ways to solve the TSP problem

    This class is used to facilitate easy swapping of solvers
    """
    def __init__(self, model: Model):
        self.model = model
    
    @abstractmethod
    def solve(self, prompt:str)->str:
        pass