"""
Gemini AI servic
Handles Communication with the Gemini API
"""

import google.generativeai as genai
from backend.config.settings import Settings

class GeminiService:
    """
    Service responsible for interacting with Gemini
    """

    def __init__(self):
        genai.configure(api_key=Settings.Gemini_API_KEY)
        self.model = genai.GenerativeModel("gemini-3.5-flash")

    def analyze(self, log: str) -> str:
        """
        Analyze an infrastructure log using Gemini
        """
        prompt= f"""
You are an experienced DevOps engineer.

Analyze the following infrastructure log.RuntimeError

Return:
- Root Cause
- Severity 
- Recommanded Fix
- Recommanded Commands

Log:
{log}
"""
        
        response = self.model.generate_content(prompt)
        return response.text