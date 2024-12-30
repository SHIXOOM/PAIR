from abc import ABC, abstractmethod
import tsplib95

class PopulationInitializer(ABC):
    """ 
    Abstract class for TSP problem population initialization for Genetic
    alogirthms solutions.
    """

    @abstractmethod
    def initialize(self, population_size: int, problem: tsplib95.models.StandardProblem) -> list[tuple[list,int]]:
        """ returns a list of tuples. each tuple contains a 1-based tsp trace and its length """
        pass