from abc import abstractmethod

class Model:
    """
    Abstract base class for the LLMs
    Any interaction with the LLMs should be done through this class
    to facilitate easy swapping of LLMs
    """

    def __init__(self, system_prompt:str, temperature: int):
        self.system_prompt = system_prompt
        self.temperature = temperature

    @abstractmethod
    def run(self, prompt:str)->str:
        """
        Send a prompt to the LLM and get the response
        """
        pass

    @abstractmethod
    def set_temperature(self, temperature:int):
        pass