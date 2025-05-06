import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.Models.Model import Model
from src.PromptResponseManager.PromptResponseManager import (
    PromptResponseManager as PRManager,
)

class Gemini(Model):
    """
    Example concrete implementation of the Model class
    """

    def __init__(
        self,
        systemPrompt: str,
        temperature: float,
        modelName="gemini-2.0-flash-thinking-exp",
    ):
        super().__init__(systemPrompt, temperature, modelName)

        self.systemPrompt = None
        self.client = None

        # Load environment variables
        load_dotenv()

        self.modelName = modelName
        self.configure(systemPrompt, temperature)

    def configure(self, systemPrompt: str, temperature: float):
        # Set temperature and system prompt
        self.temperature = temperature
        self.systemPrompt = systemPrompt

        # Initialize Gemini Client
        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))

    def run(self, prompt: str) -> str:
        errors = 0
        while True:
            try:
                response = self.client.models.generate_content(
                    model=self.modelName,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=self.systemPrompt,
                        temperature=self.temperature,
                    ),
                )
                return response.text
            except Exception as e:
                print(f"Error while making the Model's call: {e}")
                if (errors + 1) % 10 == 0:
                    shouldContinue = (
                        input(
                            f"Api provider responded with {errors} errors in a row. do you want to continue? (Y/N)"
                        )
                        == "Y"
                    )

                    if not shouldContinue:
                        raise e

                time.sleep(1)  # Sleep for 1s before retrying
                errors += 1
                continue

    def set_temperature(self, temperature: float):
        self.temperature = temperature

        self.client = genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))
        print(f"Temperature set to {temperature}")
        # set llm temp
