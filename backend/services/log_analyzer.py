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
"""

from backend.rules.kubernetes_rules import KUBERNETES_RULES
class LogAnalyzer:
    """
    Coordinates infrastructure log analysis.
    """

    def __init__(self):
        """
        Initialize the analyzer.
        """
        self.analysis_result = {}

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

    def analyze(self, log_text: str) -> dict:
        """
        Analyze Kubernetes logs using rule matching.
        """

        if not self.validate_log(log_text):
            return {
                "status": "error",
                "message": "Invalid log."
            }

        cleaned_log = self.prepare_log(log_text)

        for keyword, rule in KUBERNETES_RULES.items():

            if keyword in cleaned_log:

                return {
                    "status": "success",
                    "technology": "Kubernetes",
                    "matched_rule": keyword,
                    "root_cause": rule["root_cause"],
                    "severity": rule["severity"],
                    "confidence": rule["confidence"]
                }

        return {
            "status": "success",
            "technology": "Kubernetes",
            "matched_rule": None,
            "root_cause": "Unknown issue.",
            "severity": "Unknown",
            "confidence": 0
        }