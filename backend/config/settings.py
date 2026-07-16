"""
Application settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    Gemini_API_KEY = os.getenv("Gemini_API_KEY","")