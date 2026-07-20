"""
AI Service

Acts as a single entry point for all AI providers
"""

from backend.services.gemini_service import GeminiService

class AIService:
    """
    AI provider manager
    """
    def __init__(self):
        self.provider = GeminiService()
    
    def analyze(self, log: str):
        """
        Analyze a log using configured AI provider.
        """
        return self.provider.analyze(log)