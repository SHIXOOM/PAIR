import tsplib95


class DataManger:
    """
    A class to manage all interactions with files
    Serves more like a namespace or a utility class for
    file operations.

    That is, it's a functional encapsulation of file operations
    """ 
    @staticmethod
    def load_problem(file_path:str) -> tsplib95.models.StandardProblem:
        """
        loads a tsp problem from a .tsp file

        Args:
            file_path: the path to the .tsp file

        Returns:
            a tsplib95.models.StandardProblem object representing the problem
        """
        problem = tsplib95.load(file_path)
        return problem