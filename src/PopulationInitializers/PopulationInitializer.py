from abc import ABC, abstractmethod
import tsplib95

class PopulationInitializer(ABC):
    """ 
    Abstract class for TSP problem population initialization for Genetic
    alogirthms solutions.
    """

    @abstractmethod
    def initialize(self, population_size: int, problem: tsplib95.models.StandardProblem) -> list[list]:
        """ Initializes a population of chromosomes. """
        pass