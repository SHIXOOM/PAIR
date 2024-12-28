class PromptResponseManager:
    """
    A static class to manage prompt templates and generation
    """
    # region public methods

    @staticmethod
    def getSystemPrompt() -> str:
        prompt = '''You are an evolutionary computing expert for the Traveling Salesman Problem.
        You are given a list of points with coordinates, some traces and their lengths. 
        The traces are arranged in descending order based on their lengths, where lower values are better.
        You are asked to generate new traces from given coordinate points and traces with smaller lengths.

        For example, given the following input:
        -----START OF EXAMPLE INPUT-----
        coordinates: 0:(10,41),1:(16,37),2:(65,17),3:(1,79),4:(29,12),5:(90,55),6:(94,89),7:(30,63)
        iteration number: 2
        traces and lengths: <trace>0,1,2,3,4,5,6,7</trace>,length:430; <trace>2,6,4,0,5,7,1,3</trace>,length:520;
        -----END OF EXAMPLE INPUT-----
        EC knowledge: {crossover}\n{mutation}\n
        
        You should follow the below instruction step-by-step to generate new traces from given coordinate points and traces. 
        {self_hints}
        Ensure you preserve selected corssover operator in Step 2, selected mutation operator in Step 3, and the traces at each step, repeat Step 1, 2, 3 for a given iteration number.
        1. choose any two traces from the given traces, and save the two choosen traces, bracketed them with <sel> and </sel>.
        2. {crossover_selection} the two traces got in Step 1 and generate a new trace that is different from all traces, and has a length lower than any of these two traces. 
        The generated trace should traverse all points exactly once. Save the selected crossover operator and bracketed it with <c> and </c>. Save the generated trace and bracketed it with <cross> and </cross>.
        3. {mutation_selection} the trace generated in Step 2 and generate a new trace that is different from all traces, and has a lower length.
        The trace should traverse all points exactly once. Save the selected mutation operator and bracketed it with <m> and </m>. Save the generated trace and bracketed it with <trace> and </trace>.
        
        Directly give me all the saved selected crossover operator from Step 2, the mutation operator from Step 3, and the traces from each Step without any explanations.
        The output format should be similiar with below, and the output should contain 16 iterations:
        Iteration 1:
        Step 1: <sel>0,1,2,3,4,5,6,7</sel>, <sel>2,6,4,0,5,7,1,3</sel>
        Step 2: <c>PMX (Partially Mapped Crossover)</c><cross>2,6,7,3,4,5,1,0</cross>
        Step 3: <m>Swap Mutation</m><trace>2,6,5,3,4,7,1,0</trace>
        Iteration 2:
        Step 1: <sel>2,6,4,0,5,7,1,3</sel>, <sel>0,1,2,3,4,5,6,7</sel>
        Step 2: <c>OX (Ordered Crossover)</c><cross>2,6,0,3,4,5,7,1</cross>
        Step 3: <m>Inversion Mutation</m><trace>2,6,5,4,3,0,7,1</trace>
        '''
        pass
    
    @staticmethod
    def getNewGenerationPrompt(population: list[tuple[list, int]], points: dict) -> str:
        prompt = f'''
            coordinates: {PromptResponseManager.structureCoordinates(points)}
            iteration number: 30
            traces and lengths: {PromptResponseManager.structureTracesAndLengths(population)}
            '''
            
        return prompt

    # endregion public methods

    @staticmethod
    def structureCoordinates(points: dict) -> str:
        # make coordinates into a string format for the llm prompt
        # coordinates: 0:(10,41),1:(16,37),2:(65,17),3:(1,79),4:(29,12),5:(90,55),6:(94,89),7:(30,63)
        coordinates = ''
        for key, value in points.items():
            coordinates += f'{key}:{value},'
        
        # remove the extra comma at the end "[:-1]"
        return coordinates[:-1]
    
    @staticmethod
    def structureTracesAndLengths(population: list[tuple[list, int]]) -> str:
        # make traces and lengths into a string format for the llm prompt
        # <trace>0,1,2,3,4,5,6,7</trace>,length:430; <trace>2,6,4,0,5,7,1,3</trace>,length:520;....
        
        traces = ''
        for trace, length in population:
            traces += f'<trace>{','.join(point for point in trace)}</trace>,length:{length};'
            
        return traces
            
    @staticmethod
    def getTinderCrossoverPrompt() -> str:
        pass
    
    @staticmethod
    def getDefaultCrossoverPrompt() -> str:
        crossoverOperatorsExplanation = '''There are 2 different crossover operators you can use:
                1. PMX (Partially Mapped Crossover):
                    - Description: PMX randomly selects a segment from parent 1, copies it to the offspring, and fills in the remaining positions of the offspring by mapping elements from parent 2.
                    Below is an example.
                        - Parent 1: 1 2 3 4 5 6 7 8
                        - Parent 2: 3 7 5 1 6 8 2 4
                        - Randomly select a segment from parent 1 (e.g., positions 4 to 6): 4 5 6
                        - Copy the segment from Parent 1 to offspring solution: _ _ _ 4 5 6 _ _ 
                        - Fill in the remaining positions by mapping elements from parent 2 (note elements cannot be repeated) to the offspring: 3 7 8 4 5 6 2 1
                2. OX (Ordered Crossover):
                    - Description: OX randomly selects a segment from parent 1, copies it to the offspring, and fills in the remaining positions with the missing elements in the order in which they appear in parent 2.
                    Below is an example.
                        - Parent 1: 1 2 3 4 5 6 7 8
                        - Parent 2: 3 7 5 1 6 8 2 4
                        - Randomly select a segment from parent 1 (e.g., positions 4 to 6): 4 5 6
                        - Copy the segment from Parent 1 to the offspring: _ _ _ 4 5 6 _ _ 
                        - The missing elements in the order in which they appear in parent 2 are {3, 7, 1, 8, 2}
                        - Fill in the remaining positions of the offspring based on the above sorted elements: 3 7 1 4 5 6 8 2'''

        crossoverOperatorsInstruction = "Select one of the crossover operators based on above EC knowledge , use the selected crossover operator to crossover"
        
        return crossoverOperatorsExplanation, crossoverOperatorsInstruction
    
    @staticmethod
    def getDefaultMutationPrompt() -> str:
        mutationOperatorsExplanation = '''There are 3 different mutation operators you can use:
                1. Swap Mutation:
                    - Description: swap mutation randomly selects two positions in an individual and swaps the elements at those two positions.
                    - Example:
                        - original: 5 2 8 4 1 7 6 3
                        - Randomly select two positions, e.g., position 3 and posision 6
                        - Swap the elements 8 and 7 at position 3 and position 6: 5 2 7 4 1 8 6 3
                2. Insert Mutation:
                    - Description: insert mutation randomly selects one position in the individual and moves the element at that position to another randomly chosen position.
                    - Example:
                        - original: 5 2 8 4 1 7 6 3
                        - Randomly select one position, e.g., position 3
                        - Move the element 8 at position 3 to another randomly chosen position 6: 5 2 4 1 7 8 6 3
                3. Inversion Mutation:
                    - Description: inversion mutation randomly selects two positions in an individual and inverts the order of the elements between those positions.
                    - Example:
                        - original: 5 2 8 4 1 7 6 3
                        - Randomly select two positions, e.g., position 3 and posision 6
                        - inverts the order of the elements between position 3 and position 6: 5 2 7 1 4 8 6 3'''

        mutationOperatorsInstruction = "Select one of the Mutation operators based on above EC knowledge, use the selected crossover operator to mutate"
        
        return mutationOperatorsExplanation, mutationOperatorsInstruction
    
    @staticmethod
    def getInitialPopulationPrompt(points: dict) -> str:
        pass
    
    @staticmethod
    def parseInitialPopulationResponse(response: str, nodeCount: int) -> list[str]:
        pass
    
    @staticmethod
    def parseNewGeneration(response: str, nodeCount: int) -> list[str]:
        pass
    
    @staticmethod
    def parseThoughts(response: str) -> str:
        pass
    
    @staticmethod
    def parseCrossoverMethods(response: str) -> set[str]:
        pass
    
    @staticmethod
    def parseMutationMethods(response: str) -> set[str]:
        pass
    
    