"""
Gemini AI servic
Handles Communication with the Gemini API and converts Gemini
responses into structured results
Google SDK migration included
"""

import json
from google import genai

from backend.config.settings import Settings

class GeminiService:
    """
    Service responsible for interacting with Gemini
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=Settings.Gemini_API_KEY
        )
       
    def analyze(self, log: str):
        """
        Analyze an infrastructure log using Gemini

        Returns: 
          dict: Structured analysis result or Structured error
        """

        prompt = f"""
You are a Senior Kubernetes Site Reliability Engineer (SRE).

Analyze the following Kubernetes log.

Return ONLY valid JSON.

Do not use markdown.

Do not wrap the response in ```.

Do not include explanations outside JSON.

Return this exact schema:

{{
    "root_cause": "",
    "severity": "",
    "confidence": "",
    "explanation": "",
    "recommendations": [
        ""
    ],
    "commands": [
        ""
    ]
}}

Guidelines:

- severity must be one of:
  High
  Medium
  Low

- confidence must be a percentage like:
  95%

- recommendations must contain 3-5 concise actions.

- commands must contain useful kubectl commands.

Log:

{log}
"""
        #Step1 call gemini
        try:
            response = self.client.models.generate_content(
                model = "gemini-3.5-flash",
                contents = prompt
            )
            text = response.text.strip()
          
        except Exception as e:
            return {
                "status": "error",
                "error_type": "ai_service_error",
                "message": str(e)
            }

        #Step 2 - Convert Gemini JSON response
        try:
            return json.loads(text)
       
        except json.JSONDecodeError:
            return {
                "status": "error",
                "error_type": "invalid_ai_response",
                "message": "Gemini returned an invalid JSON response.",
                "raw_response": text
            }
