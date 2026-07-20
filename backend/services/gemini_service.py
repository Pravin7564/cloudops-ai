"""
Gemini AI servic
Handles Communication with the Gemini API
"""

import json
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
        #Step1 try gemini
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            return response.text

        except Exception as e:
            return f"AI Service Error: {str(e)}"
        
        #Step 2 - Get response text

        text = response.text.strip()

        #Step 3 - Convert json text into python dictionary
        try:
            return json.loads(text)
        
        except json.JSONDecodeError:
            return {
                "root cause":
                    "Unable to parse AI response.",
                
                "severity":
                    "Unknown",

                "confidence":
                    "0%",
                
                "explanation":
                    text,
                
                "recommandations":
                    [],
                
                "commands":
                    []
            }
