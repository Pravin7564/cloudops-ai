"""
Rule promotion service.
Converts approved AI-generated rule candidates
into persistent Kubernetes rule definitions.
The service does not automatically modify
production rules. It prepares the approved
rule for controlled promotion.
"""
import json
from pathlib import Path
from backend.rules.kubernetes_rules import KUBERNETES_RULES
from datetime import datetime,timezone

class RulePromoter:
   """
   Handles persistent promotion of approved
   Kubernetes rule candidates.
   """
   def __init__(self):
       self.output_file = (
           Path(__file__).parent / "promoted_rules.json"
       )
   def promote(self, candidate: dict):
       """
       Persist an approved rule candidate.
       The candidate must already have
       status = approved.
       """
       if candidate.get("status") != "approved":
           return {
               "status": "error",
               "message": (
                   "Only approved rule candidates "
                   "can be promoted."
               ),
           }
       pattern = candidate.get("pattern")
       if not pattern:
           return {
               "status": "error",
               "message": "Rule candidate has no pattern.",
           }
       if pattern in KUBERNETES_RULES:
           return {
               "status": "duplicate",
               "message": (
                   "Rule already exists in production "
                   "Kubernetes rules."
               ),
               "pattern": pattern,
           }
       promoted_rules = self._load()
       for rule in promoted_rules:
           if rule.get("pattern") == pattern:
               return {
                   "status": "duplicate",
                   "message": (
                       "Rule already exists in "
                       "promoted rules."
                   ),
                   "pattern": pattern,
               }
       promoted_rules.append({
           "pattern": pattern,
           "root_cause": candidate["root_cause"],
           "severity": candidate["severity"],
           "confidence": candidate["confidence"],
           "explanation": candidate["explanation"],
           "recommendations": candidate["recommendations"],
           "commands": candidate["commands"],
           "source": candidate.get(
               "source",
               "Gemini AI"
           ),
           "status": "promoted",
           "created_at": candidate.get(
               "created_at",
               ""
           ),
            "approved_at": candidate.get(
                "approved_at",
                ""
           ),
           "promoted_at": datetime.now(
               timezone.utc
           ).isoformat(),

       })
       self._save(promoted_rules)
       return {
           "status": "success",
           "message": (
               "Approved rule persisted "
               "successfully."
           ),
           "pattern": pattern,
       }
   def _load(self):
       """
       Load persisted promoted rules.
       """
       if not self.output_file.exists():
           return []
       with open(
           self.output_file,
           "r",
           encoding="utf-8"
       ) as file:
           return json.load(file)
   def _save(self, rules):
       """
       Save persisted promoted rules.
       """
       with open(
           self.output_file,
           "w",
           encoding="utf-8"
       ) as file:
           json.dump(
               rules,
               file,
               indent=4
           )