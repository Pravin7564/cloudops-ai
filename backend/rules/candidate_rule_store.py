"""
Candidate rule storage.
Stores AI-generated Kubernetes rule candidates
separately from approved production rules.
"""
import json
from pathlib import Path
from backend.rules.rules_schema import RuleCandidate
from datetime import datetime,timezone

class CandidateRuleStore:
   """
   Handles storage of AI-generated rule candidates.
   """
   def __init__(self):
       self.file_path = (
           Path(__file__).parent / "candidate_rules.json"
       )
       
   def save(self, candidate: dict):
       """
       Validate and save an AI-generated rule candidate.
       """
       required_fields = [
           "pattern",
           "root_cause",
           "severity",
           "confidence",
           "explanation",
           "recommendations",
           "commands",
       ]
       for field in required_fields:
           if field not in candidate:
               return {
                   "status": "error",
                   "message": (
                       f"Invalid rule candidate. "
                       f"Missing field: {field}"
                   ),
               }
       rule = RuleCandidate(
           pattern=candidate["pattern"],
           root_cause=candidate["root_cause"],
           severity=candidate["severity"],
           confidence=candidate["confidence"],
           explanation=candidate["explanation"],
           recommendations=candidate["recommendations"],
           commands=candidate["commands"],
           created_at=datetime.now(timezone.utc).isoformat(),
       )
       existing_rules = self._load()    
       existing_patterns = [
           item["pattern"]
           for item in existing_rules
       ]
       if rule.pattern in existing_patterns:
           return {
               "status": "duplicate",
               "message": (
                   "A rule candidate with this pattern "
                   "already exists."
               ),
           }
       existing_rules.append({
           "pattern": rule.pattern,
           "root_cause": rule.root_cause,
           "severity": rule.severity,
           "confidence": rule.confidence,
           "explanation": rule.explanation,
           "recommendations": rule.recommendations,
           "commands": rule.commands,
           "source": rule.source,
           "status": rule.status,
           "created_at": rule.created_at,
           "approved_at": rule.approved_at,
           "promoted_at": rule.promoted_at
       })
       self._save(existing_rules)
       return {
           "status": "success",
           "message": "Rule candidate saved successfully.",
           "pattern": rule.pattern,
       }
   
   def _load(self):
       """
       Load existing rule candidates.
       """
       if not self.file_path.exists():
           return []
       with open(self.file_path, "r") as file:
           return json.load(file)
       
   def _save(self, rules):
       """
       Save rule candidates to JSON.
       """
       with open(self.file_path, "w") as file:
           json.dump(
               rules,
               file,
               indent=4
           )