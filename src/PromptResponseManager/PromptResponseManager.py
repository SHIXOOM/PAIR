import re
import random


class PromptResponseManager:
    """
    A static class to manage prompt templates and generation
    """

    @staticmethod
    def getSystemPrompt(selfHints: str = '', populationSize: int = 16) -> str:
        # get default crossover and mutation prompt and instructions for them
        crossoverPrompt, crossoverInstruction = PromptResponseManager.getCrossoverPrompt()
        mutationPrompt, mutationInstruction = PromptResponseManager.getMutationPrompt()

        # get the tinder selection prompt
        tinderSelectionPrompt = PromptResponseManager.getTinderCrossoverPrompt()

        # get self hints
        selfHints = '''
            '''

        # get the system prompt
        prompt = f'''You are an evolutionary computing expert for the Traveling Salesman Problem.
            You are given a list of points with coordinates, some traces and their lengths. 
            The traces are arranged in descending order based on their lengths, where lower values are better.
            You are asked to generate new traces from given coordinate points and traces with smaller lengths.

            For example, given the following input:
            -----START OF EXAMPLE INPUT-----
            **coordinates:** 0:(10,41),1:(16,37),2:(65,17),3:(1,79),4:(29,12),5:(90,55),6:(94,89),7:(30,63)
            **iteration number:** 2
            **traces and lengths:** <trace>0,1,2,3,4,5,6,7</trace>,length:430; <trace>2,6,4,0,5,7,1,3</trace>,length:520;
            -----END OF EXAMPLE INPUT-----
            **EC knowledge:** {crossoverPrompt}\n{mutationPrompt}\n
            
            You should follow the below instruction step-by-step to generate new traces from given coordinate points and traces. 
            {selfHints}
            Ensure you preserve selected corssover operator in Step 2, selected mutation operator in Step 3, and the traces at each step, repeat Step 1, 2, 3 for a given iteration number.
            1. {tinderSelectionPrompt} Save the two choosen traces, bracketed them with <sel> and </sel>.
            2. {crossoverInstruction} the two traces got in Step 1 and generate a new trace that is different from all traces, and has a length lower than any of these two traces. 
            The generated trace should traverse all points exactly once. Save the selected crossover operator and bracketed it with <c> and </c>. Save the generated trace and bracketed it with <cross> and </cross>.
            3. {mutationInstruction} the trace generated in Step 2 and generate a new trace that is different from all traces, and has a lower length.
            The trace should traverse all points exactly once. Save the selected mutation operator and bracketed it with <m> and </m>. Save the generated trace and bracketed it with <trace> and </trace>.
            
            Directly give me all the saved selected crossover operator from Step 2, the mutation operator from Step 3, and the traces from each Step without any explanations.
            The output format should be similiar with below, and the output should contain {populationSize} iterations:
            Iteration 1:
            Step 1: <sel>0,1,2,3,4,5,6,7</sel>, <sel>2,6,4,0,5,7,1,3</sel>
            Step 2: <c>PMX (Partially Mapped Crossover)</c><cross>2,6,7,3,4,5,1,0</cross>
            Step 3: <m>Swap Mutation</m><trace>2,6,5,3,4,7,1,0</trace>
            Iteration 2:
            Step 1: <sel>2,6,4,0,5,7,1,3</sel>, <sel>0,1,2,3,4,5,6,7</sel>
            Step 2: <c>OX (Ordered Crossover)</c><cross>2,6,0,3,4,5,7,1</cross>
            Step 3: <m>Inversion Mutation</m><trace>2,6,5,4,3,0,7,1</trace>
            '''
        return prompt

    @staticmethod
    def getNewGenerationPrompt(population: list[tuple[list, int]], points: dict, populationSize: int) -> str:
        prompt = f'''**coordinates:** {PromptResponseManager.structureCoordinates(points)}
            **iteration number:** {populationSize}
            **traces and lengths:** {PromptResponseManager.structureTracesAndLengths(population)}
            '''

        return prompt

    # endregion public methods

    @staticmethod
    def structureCoordinates(points: dict) -> str:
        # make coordinates into a string format for the llm prompt
        # coordinates: 0:(10,41),1:(16,37),2:(65,17),3:(1,79),4:(29,12),5:(90,55),6:(94,89),7:(30,63)
        coordinates = ''
        for point, pointCoordinates in points.items():
            coordinates += f'{point}:{pointCoordinates},'

        # remove the extra comma at the end "[:-1]"
        return coordinates[:-1]

    @staticmethod
    def structureTracesAndLengths(population: list[tuple[list, int]]) -> str:
        # make traces and lengths into a string format for the llm prompt
        # <trace>0,1,2,3,4,5,6,7</trace>,length:430; <trace>2,6,4,0,5,7,1,3</trace>,length:520;....

        traces = ''
        for trace, length in population:
            traces += f"<trace>{','.join(str(point) for point in trace)}</trace>,length:{length};"

        return traces

    @staticmethod
    def getTinderCrossoverPrompt() -> str:
        prompt = '''consider yourself a trace of one of the available traces, and you want to match with another trace as if you are using Tinder dating app, match yourself with the most suitable individual from the dating pool for crossover, aiming to produce an offspring with an optimized solution and length lower than you and your partner.
        You can, but not limited to, evaluate potential partners based on the following criteria:

        A. **Genetic Diversity:**
        - **Complementary Traits:** Identify individual whose genetic makeup introduces beneficial variations when combined with yours, enhancing the offspring's potential to explore new solution spaces.

        B. **Fitness Level:**
        - **High Performance:** Prioritize individuals demonstrating less lengths, indicating effective solutions to the Traveling Salesman Problem, to increase the likelihood of producing a high-quality offspring.

        C. **Crossover Compatibility:**
        - **Effective Combination:** Assess the compatibility of your genetic representation with potential partners to ensure that the chosen crossover operator can effectively merge the genomes, maintaining valid the Traveling Salesman Problem routes.
        Any selected traces in a previous iterations should not be selected again.
        You can select an offspring from the previous iterations for crossover in the next iterations.'''
        return prompt

    @staticmethod
    def getCrossoverPrompt() -> tuple[str, str]:
        crossoverOperatorsExplanation = '''There are 2 different crossover operators you can use:
                1. **PMX (Partially Mapped Crossover):**
                    - **Description:** PMX randomly selects a segment from parent 1, copies it to the offspring, and fills in the remaining positions of the offspring by mapping elements from parent 2.
                    Below is an example.
                        - **Parent 1:** 1 2 3 4 5 6 7 8
                        - **Parent 2:** 3 7 5 1 6 8 2 4
                        - **Randomly select a segment from parent 1 (e.g., positions 4 to 6):** 4 5 6
                        - **Copy the segment from Parent 1 to offspring solution:** _ _ _ 4 5 6 _ _ 
                        - **Fill in the remaining positions by mapping elements from parent 2 (note elements cannot be repeated) to the offspring:** 3 7 8 4 5 6 2 1
                2. **OX (Ordered Crossover):**
                    - **Description:** OX randomly selects a segment from parent 1, copies it to the offspring, and fills in the remaining positions with the missing elements in the order in which they appear in parent 2.
                    Below is an example.
                        - **Parent 1:** 1 2 3 4 5 6 7 8
                        - **Parent 2:** 3 7 5 1 6 8 2 4
                        - **Randomly select a segment from parent 1 (e.g., positions 4 to 6):** 4 5 6
                        - **Copy the segment from Parent 1 to the offspring:** _ _ _ 4 5 6 _ _ 
                        - **The missing elements in the order in which they appear in parent 2 are {3, 7, 1, 8, 2}**
                        - **Fill in the remaining positions of the offspring based on the above sorted elements:** 3 7 1 4 5 6 8 2'''

        crossoverOperatorsInstruction = "Select one of the crossover operators based on above EC knowledge , use the selected crossover operator to crossover"

        return crossoverOperatorsExplanation, crossoverOperatorsInstruction

    @staticmethod
    def getMutationPrompt() -> tuple[str, str]:
        mutationOperatorsExplanation = '''There are 3 different mutation operators you can use:
                1. **Swap Mutation:**
                    - **Description:** swap mutation randomly selects two positions in an individual and swaps the elements at those two positions.
                    - **Example:**
                        - **original:** 5 2 8 4 1 7 6 3
                        - **Randomly select two positions, e.g., position 3 and posision 6:** 3 6
                        - **Swap the elements 8 and 7 at position 3 and position 6:** 5 2 7 4 1 8 6 3
                2. **Insert Mutation:**
                    - **Description:** insert mutation randomly selects one position in the individual and moves the element at that position to another randomly chosen position.
                    - **Example:**
                        - **original:** 5 2 8 4 1 7 6 3
                        - **Randomly select one position, e.g., position 3:** 3
                        - **Move the element 8 at position 3 to another randomly chosen position 6:** 5 2 4 1 7 8 6 3
                3. **Inversion Mutation:**
                    - **Description:** inversion mutation randomly selects two positions in an individual and inverts the order of the elements between those positions.
                    - **Example:**
                        - **original:** 5 2 8 4 1 7 6 3
                        - **Randomly select two positions, e.g., position 3 and posision 6:** 3 6
                        - **inverts the order of the elements between position 3 and position 6:** 5 2 7 1 4 8 6 3'''

        mutationOperatorsInstruction = "Select one of the Mutation operators based on above EC knowledge, use the selected crossover operator to mutate"

        return mutationOperatorsExplanation, mutationOperatorsInstruction

    @staticmethod
    def getInitialPopulationPrompt(points: dict, populationSize: int) -> tuple[str, str]:
        systemPrompt = f'''**You are an evolutionary computing expert for the Traveling Salesman Problem.**
        You are given a list of points with coordinates in a 2-Dimensional plane.
        You are asked to generate {populationSize} new traces given a set of points with coordinates.
        Try to find the shortest possible traces that traverses each point exactly once and returns to the start point.
        The distance between two points *A*, *B* equal to $\\text{{Distance}} = \\sqrt{{(A_{{x}} - B_{{x}})^2 + (A_{{y}} - B_{{y}})^2}}$, where $A_{{x}}$ and $B_{{x}}$ are the x-coordinates of points *A* and *B*, and $A_{{y}}$ and $B_{{y}}$ are the y-coordinates of points *A* and *B*.
        And the length of a trace is the sum of all the distance of adjacent points in the trace including the distance from the last point to the start point. $\\text{{Length}} = \\sum_{{i=0}}^{{node\_count - 1}} \\sqrt{{(A[i]_{{x}} - A[i+1]_{{x}})^2 + (A[i]_{{y}} - A[i+1]_{{y}})^2}} + \\sqrt{{(A[node\_count - 1]_{{x}} - A[0]_{{x}})^2 + (A[node\_count - 1]_{{y}} - A[0]_{{y}})^2}}$
        Think step-by-step, in more than 40 or 50 steps.
        
        For example, given the following input:
            -----START OF EXAMPLE INPUT-----
            **coordinates:** 0:(10,41),1:(16,37),2:(65,17),3:(1,79),4:(29,12),5:(90,55),6:(94,89),7:(30,63)
            **population size:** 2
            -----END OF EXAMPLE INPUT-----

        Directly give me the traces only.
        You should save and output the generated traces in the following format:
        <trace>0,1,2,3,4,5,6,7</trace>,length:430;
        <trace>2,6,4,0,5,7,1,3</trace>,length:520;
        '''

        userPrompt = f'''**coordinates:** {PromptResponseManager.structureCoordinates(points)}
        **population size:** {populationSize}
        '''
        return systemPrompt, userPrompt

    @staticmethod
    def parseInitialPopulationResponse(response: str, nodeCount: int) -> list[list[int]]:
        return PromptResponseManager.parseNewGeneration(response, nodeCount)

    @staticmethod
    def parseNewGeneration(response: str, nodeCount: int) -> list[list[int]]:
        """Find all traces in the response -> list of lists,
        Each list is a trace, each element is an integer, which is a point

        Example output:
        [[0, 1, 2, 3, 4, 5, 6, 7],
        [2, 6, 4, 0, 5, 7, 1, 3],
        [2, 6, 5, 3, 4, 7, 1, 0],
        [2, 6, 5, 4, 3, 0, 7, 1]]
        """

        # Find all traces in the response -> list of strings, each string is a trace
        tracesStrings = re.findall(r'<trace>(.*?)</trace>', response)
        # Convert each trace string into a list of integers -> each integer is a point
        traces = [list(map(lambda pointChar: int(pointChar), traceString.split(','))) for traceString in tracesStrings]

        # Validate the traces
        validTraces = []
        for trace in traces:
            if PromptResponseManager.validateTrace(trace, nodeCount):
                validTraces.append(trace)
            else:
                validTraces.append(PromptResponseManager.fixTrace(trace, nodeCount))

        return validTraces

    @staticmethod
    def parseSelectedTraces(response: str) -> list[list[str]]:
        """Find all trace pairs selected for mating -> list of lists
        Each list is a trace pair
        
        
        Example output:
        [['5,2,6,4,3,7,1,8,9,0', '4,3,1,9,0,7,6,8,5,2'],
        ['5,2,6,4,3,7,1,8,9,0', '9,0,5,8,7,3,6,4,2,1'],
        ['5,2,6,4,3,7,1,8,9,0', '9,0,2,5,8,4,6,3,1,7']]
        """

        # Find all traces selected for mating -> list of strings, each string is a trace
        selectedTraces = re.findall(r'<sel>(.*?)</sel>', response)
        # Pair each two traces together (pairwise traces are the ones who mated in each iteration) -> list of lists, each list is a pair of traces
        pairTraces = [list([selectedTraces[i], selectedTraces[i + 1]]) for i in range(0, len(selectedTraces), 2)]
        return pairTraces

    @staticmethod
    def parseCrossoverMethods(response: str) -> list[tuple[str, str]]:
        """Find all crossover methods and the trace resulted from the crossover -> list of tuples
        Each tuple is a crossover method and the trace resulted from the crossover
        
        Example output:
        [('PMX (Partially Mapped Crossover)','4,3,6,8,9,7,1,5,2,0'),
        ('OX (Ordered Crossover)', '5,2,6,4,3,7,8,9,0,1'),
        ('PMX (Partially Mapped Crossover)', '9,0,6,4,3,7,1,8,5,2')]"""

        # Find all crossover methods and the trace resulted from the crossover -> list of tuples
        selectedCrossoversAndTraceResulted = re.findall(r'<c>(.*?)</c><cross>(.*?)</cross>', response)
        return selectedCrossoversAndTraceResulted

    @staticmethod
    def parseMutationMethods(response: str) -> set[tuple[str, int]]:
        """Find all mutation methods used in the iteration and the count of uses of each mutation method -> set of tuples
        Each tuple is a mutation method and the count of usages in the iteration
        Example output: 
        {('Insert Mutation', 5),
        ('Inversion Mutation', 5),
        ('Swap Mutation', 6)}"""

        # Find all mutation methods used in the iteration -> list of strings, each string is a mutation method
        selectedMutations = re.findall(r'<m>(.*?)</m>', response)
        # Pair each mutation method with its count of usages -> set of tuples
        selectedMutationsAndCounts = set(
            (selectedMutation, selectedMutations.count(selectedMutation)) for selectedMutation in selectedMutations)
        return selectedMutationsAndCounts

    @staticmethod
    def parseThoughts(response: str) -> list[str]:
        thoughts = re.findall(r'<thought>(.*?)</thought>', response)
        return thoughts

    @staticmethod
    def validateTrace(trace: list[int], nodeCount: int) -> bool:
        return (len(trace) == nodeCount) and (len(set(trace)) == nodeCount) and all(point in range(1, nodeCount + 1) for point in trace)

    @staticmethod
    def fixTrace(trace: list[int], nodeCount: int) -> list[int]:
        # remove the points that are not in the range of 1 to nodeCount
        trace = [point for point in trace if point in range(1, nodeCount + 1)]
        # get the points in the trace
        setTrace = set(trace)
        # get the points that are not in the trace
        unavailablePoints = [point for point in range(1, nodeCount + 1) if point not in setTrace]
        # shuffle the unavailable points
        random.shuffle(unavailablePoints)
        # add the shuffled unavailable points to the trace
        trace.extend(unavailablePoints)
        return trace
