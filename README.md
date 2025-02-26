# PAIR: A Novel Large Language Model-Guided Selection Strategy for Evolutionary Algorithms  
This is the implementation for the experiments used for PAIR paper results section
-We facilitated the design and implementation for this code to make all experiments easily repeatable and transparent
## Utilizing LLMs in Evolutionary Algorithms as Evolutionary Optimizers and to imitate human-based selection (PAIR-Driven Selection)
Our main tests and experiments are on the *Travelling Salesman Problem* using *TSPLIB95* and *PyConcorde* Libraries to generate problems and find their optimal solutions.  
All problems are on a **2-D Euclidean plane**.  

# How to Run:

1. Create an environment variable to store your Gemini API's key, you can get a key from [Google AI Studio](https://aistudio.google.com/apikey)
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
2. You would need to have created TSP problem files and found their optimal solutions using [PyConcorde](https://github.com/jvkersch/pyconcorde).  
We did not implement this part as the library didn't work locally, so we did that part on google colab instead and used the files directly.

3. Move to your LLMsGA directory in the terminal:
```zsh
cd LLMsGA
```
4. Run the main.py
```zsh
Python .
```  
  
**In the following steps, you would be provided with options to choose from**  
5. Enter the name of the problem you want to solve
```zsh
Enter the name of the problem: *Problem_Name*

```
6. Enter the problem's TSP file path
```zsh
Enter the path to the problem file: */file_path/problem.tsp*
```
7. Enter the problem's optimal solution you found through PyConcorde
```zsh
Enter the optimal solution for the problem: *Optimal_Solution*
```
8. Choose which solver to use (which methodology you want to solve with)
```zsh
Select the solver to use:
1. TinderMatching
Enter the number of your choice: *Solver_Number*
```
9. Select the Large Language Model you want to use (only Gemini is implemented so far)
```zsh
Select the model to use:
1. gemini-2.0-flash-thinking-exp-1219
2. gemini-2.0-flash-exp
Enter the number of your choice: *Model_Number*
```
10. Select which Population Initializer you want to use (only Random and Simulated Annealing Initializers are implemented so far)
```zsh
Select the population initializer to use:
1. simulated-annealing
2. random
Enter the number of your choice: *Population_Initializer_Number*
```

The Experiment should run now, you can find the run's results in /data folder.
If any errors happened with the LLM during the run, the code will retry several times and if fails again will ask if you want to try again or terminate.

# Running Visualizations Manager

To generate graphs for the experiments data, run the Visualizations Manager:

1. Move to your LLMsGA directory in the terminal:
```zsh
cd LLMsGA
```
2. Run the Visualizations Manager:
```zsh
python src/VisualizationsManager.py
```

# Running TSP Visualizer

To visualize the behavior of Genetic Algorithms in solving TSP, follow these steps:

1. Ensure you have the parsed JSON data from the experiments. You can generate this using the `parser.py` script:
```zsh
python TSP-Visualizer/parser.py
```
2. Open the `index.html` file using a web server to start the TSP Visualizer frontend.


![tsp-vis-start](https://github.com/user-attachments/assets/0c936a60-9a56-4eae-a73b-b097d8d37bf9)

