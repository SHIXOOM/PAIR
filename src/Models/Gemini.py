from src.Models.Model import Model


class Gemini(Model):
    """
       Example concrete implementation of the Model class 
    """
    def __init__(self, system_prompt:str, temperature: int):
        super().__init__(system_prompt, temperature)
        # initialize Gemini Model
        print(f"Gemini created with system_prompt: {system_prompt} and temperature: {temperature}")

    def run(self, prompt:str)->str:
        return "Gemini is running"

    def set_temperature(self, temperature:int):
        self.temperature = temperature
        print(f"Temperature set to {temperature}")
        # set llm temp