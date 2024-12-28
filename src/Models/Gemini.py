from src.Models.Model import Model
import google.generativeai as genai
import os
from dotenv import load_dotenv

from IPython.display import display, Markdown
import webbrowser
import tempfile



class Gemini(Model):
    """
       Example concrete implementation of the Model class 
    """
    def __init__(self, system_prompt:str, temperature: float, model = "gemini-2.0-flash-thinking-exp-1219"):
        super().__init__(system_prompt, temperature)
        
        # Load environment variables
        load_dotenv()
        
        self.model = model
        
        # Set temperature and system prompt
        self.temperature = temperature
        self.system_prompt = system_prompt
        
        # Models parameters used in generation
        self.generation_config = {
            "temperature": temperature,
            }
        
        # Initialize Gemini Client
        
        genai.configure(api_key=os.environ.get('GEMINI_API_KEY'))
        self.client = genai.GenerativeModel(
            model_name = self.model,
            generation_config = self.generation_config,
            system_instruction = system_prompt
            )
        # Initialize Gemini Model Message
        print(f"Gemini created with system_prompt: {system_prompt} and temperature: {temperature}")

    def run(self, prompt:str)->str:
        response = self.client.generate_content(prompt).candidates[0]
        
        if self.model.__contains__("thinking"):
            return f'''<thought>{response.content.parts[0].text}</thought>
                    <output>{response.content.parts[1].text}</output>'''
        else:
            return response.content.parts[0].text

    def set_temperature(self, temperature: float):
        self.temperature = temperature
        self.generation_config["temperature"] = temperature
        
        self.client = genai.GenerativeModel(
            model_name = "gemini-2.0-flash-thinking-exp-1219",
            generation_config = self.generation_config,
            system_instruction = self.system_prompt
            )
        print(f"Temperature set to {temperature}")
        # set llm temp
        

# Example Usage 
gem = Gemini("You are Albert Einstein", 1.1)
response = gem.run("who are you?")

# Create temporary HTML file with Markdown content
with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html') as f:
    markdown_content = f"""
    <html>
    <head>
        <title>Gemini Response</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .container {{ max-width: 800px; margin: 0 auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Thought Process:</h2>
            <p>{response['thought']}</p>
            <h2>Response:</h2>
            <p>{response['response']}</p>
        </div>
    </body>
    </html>
    """
    f.write(markdown_content)
    filepath = f.name

# Open in default browser
webbrowser.open('file://' + filepath)