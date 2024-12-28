class PromptResponseManager:
    """
    A static class to manage prompt templates and generation
    """
    

    @staticmethod
    def getSystemPrompt() -> str:
        pass

    @staticmethod
    def getTinderCrossoverPrompt() -> str:
        pass
    
    @staticmethod
    def getDefaultCrossoverPrompt() -> str:
        pass
    
    @staticmethod
    def getDefaultMutationPrompt() -> str:
        pass
    
    
    @staticmethod
    def getInitialPopulationPrompt(points: dict) -> str:
        pass
    
    @staticmethod
    def parseInitialPopulationResponse(response: str) -> list[str]:
        pass
    
    @staticmethod
    def parseNewGeneration(response: str) -> list[str]:
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
    
    