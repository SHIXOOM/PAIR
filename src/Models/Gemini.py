from src.Models.Model import Model
import google.generativeai as genai

import os
from dotenv import load_dotenv
import time

from src.PromptResponseManager.PromptResponseManager import PromptResponseManager as PRManager


class Gemini(Model):
    """
       Example concrete implementation of the Model class 
    """

    def __init__(self, systemPrompt: str, temperature: float, modelName="gemini-2.0-flash-thinking-exp"):
        super().__init__(systemPrompt, temperature, modelName)

        self.generation_config = None
        self.systemPrompt = None
        self.client = None
        self.generationConfig = None

        # Load environment variables
        load_dotenv()

        self.modelName = modelName
        self.configure(systemPrompt, temperature)

    def configure(self, systemPrompt: str, temperature: float):
        # Set temperature and system prompt
        self.temperature = temperature
        self.systemPrompt = systemPrompt

        # Models parameters used in generation
        self.generationConfig = {
            "temperature": temperature,
        }

        # Initialize Gemini Client
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
        self.client = genai.GenerativeModel(
            model_name=self.modelName,
            generation_config=self.generationConfig,
            system_instruction=systemPrompt
        )

    def run(self, prompt: str) -> str:
        errors = 0
        while True:
            try:
                response = self.client.generate_content(prompt).candidates[0].content.parts[1].text
                return response
            except Exception as e:
                print(f"Error while making the Model's call: {e}")
                if (errors+1) % 10 == 0:
                    shouldContinue = \
                        input(f"Api provider responded with {errors} errors in a row. do you want to continue? (Y/N)"
                            ) == "Y"

                    if not shouldContinue:
                        raise e

                time.sleep(1)  # Sleep for 1s before retrying
                errors += 1
                continue

    def set_temperature(self, temperature: float):
        self.temperature = temperature
        self.generation_config["temperature"] = temperature

        self.client = genai.GenerativeModel(
            model_name=self.modelName,
            generation_config=self.generation_config,
            system_instruction=self.systemPrompt
        )
        print(f"Temperature set to {temperature}")
        # set llm temp
