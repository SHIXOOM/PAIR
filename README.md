# LLMxGeneticAlgorithms: Tinder-Based Matching
## Trying out Genetic Algorithms using Large Language Models to control evolutionary operations
Our main tests and experiments are on the *Travelling Salesman Problem* using *TSPLIB95* and *PyConcorde* Libraries to generate problems and find their optimal solutions.  
All problems are on a **2-D Euclidean plane**.  

# How to Run:

1-Create an environment variable to store your Gemini API's key, you can get a key from [Google AI Studio](https://aistudio.google.com/apikey)
```env 
GEMINI_API_KEY=your_key
```
You can also change it directly in the Gemini model's Class
```python
def configure(self, systemPrompt: str, temperature: float):
        code.....

        # Initialize Gemini Client
        genai.configure(api_key= "your_API_Key")
        self.client = genai.GenerativeModel(
            model_name=self.modelName,
            generation_config=self.generationConfig,
            system_instruction=systemPrompt
        )
```
2-You would need to have created TSP problem files and found their optimal solutions using [PyConcorde](https://github.com/jvkersch/pyconcorde), we did not implement this part as the library didn't work locally, so we did that part on google colab instead and used the files directly.

3-move to your LLMsGA directory in the terminal:
```zsh
cd LLMsGA
```
4-Run the main.py
```zsh
Python .
```
**In the following steps, you would be provided with options to choose from**  
5-Enter the name of the problem you want to solve
```zsh
Enter the name of the problem: Problem_Name
```
6-Enter the problem's TSP file path
```zsh
Enter the path to the problem file: /file_path/problem.tsp
```
7-Enter the problem's optimal solution you found through PyConcorde
```zsh
Enter the optimal solution for the problem: Optimal_Solution
```
8-Choose which solver to use (which methodology you want to solve with)
```zsh
Select the solver to use:
1. TinderMatching
Enter the number of your choice: Solver\'s_Number
```
9-Select the Large Language Model you want to use (only Gemini is implemented so far)
```zsh
Select the model to use:
1. gemini-2.0-flash-exp
Enter the number of your choice: Model\'s_Number
```
10-Select which Population Initializer you want to use (only Random and Simulated Annealing Initializers are implemented so far)
```zsh
Select the population initializer to use:
1. simulated-annealing
2. random
Enter the number of your choice: Population_Initializer_Number
```

The Experiment should run now, you can find the run's results in /data folder.
If any errors happened with the LLM during the run, the code will retry several times and if fails again will ask if you want to try again or terminate.
