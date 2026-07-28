"""
Module: log_analyzer

Purpose:
    Coordinate the analysis of infrastructure logs.

Responsibilities:
    - Validate log input.
    - Prepare log data for AI analysis.
    - Coordinate the analysis workflow.
    - Return structured analysis results.

This module DOES NOT:
    - Read files.
    - Call AI providers directly.
    - Print reports.
    - Save data.

New Comments
Cloudops API - Log Analyzer

This service :
1. Validates the log
2. Checks from Kubernetes rules
3. If no rule matches , asks Gemini AI.    
"""

from backend.rules.rule_loader import RuleLoader
#from backend.services.gemini_service import GeminiService
from backend.services.ai_service import AIService
from backend.rules.candidate_rule_store import CandidateRuleStore

class LogAnalyzer:
    """
    Coordinates infrastructure log analysis.
    """

    def __init__(self):
        """
        Initialize the analyzer.
        """
        #self.gemini = GeminiService()
        self.ai_service = AIService()
        self.candidate_store = CandidateRuleStore()
        self.rule_loader = RuleLoader()

    def validate_log(self, log_text: str) -> bool:
        """
        Validate the incoming log text.

        Returns:
            True if valid, otherwise False.
        """
        if not log_text:
            return False

        if not log_text.strip():
            return False

        return True

    def prepare_log(self, log_text: str) -> str:
        """
        Prepare the log before analysis.
        """
        return log_text.strip()

    def analyze(self, log_text: str):
        """
        Analyze Kubernetes logs using rule matching.
        """

        if not self.validate_log(log_text):
            return {
                "status": "error",
                "message": "Invalid log."
            }

        cleaned_log = self.prepare_log(log_text)

        rules = self.rule_loader.load_rules()

        normalized_log = cleaned_log.lower()

        matches = []

        for keyword, rule in rules.items():

            if keyword.lower() in normalized_log:
                matches.append(
                    {
                    "keyword": keyword,
                    "rule": rule,
                    "specificity": len(keyword),
                    }
                )
        if matches:
            matches.sort(
                key=lambda item: item["specificity"],
                reverse=True
                )

            best_match = matches[0]

            return {
                "status": "success",
                "Source": "Rule Engine",
                "technology": "Kubernetes",
                "matched_rule": best_match["keyword"],
                **best_match["rule"]
            }
        #Unknon Issue -> Ask Gemini API

        #ai_response = self.gemini.analyze(cleaned_log)
        ai_response = self.ai_service.analyze(cleaned_log)

        if ai_response.get("status") == "error":
            return{
                "status": "error",
                "source": "Gemini AI",
                "error_type": ai_response.get(
                    "error_type",
                    "ai_service_error"
                ),
                "message": ai_response.get(
                    "message",
                    "AI service failed to analyze the log."
                )
            }
        # Generate an AI rule candidate for future learning
        rule_candidate_result = (
           self.ai_service.generate_rule_candidate(
               cleaned_log
           )
       )
        candidate_status = None
        if rule_candidate_result.get("status") == "success":
           candidate = rule_candidate_result.get(
               "rule_candidate"
           )
           if candidate:
               candidate_status = (
                   self.candidate_store.save(candidate)
               )
        return {
           "status": "success",
           "Source": "Gemini AI",
           "Analysis": ai_response,
           "rule_learning": candidate_status
        }