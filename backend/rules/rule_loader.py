"""

Rule loader.

Combines built-in Kubernetes rules with

human-approved AI-promoted rules.

"""

import json

from pathlib import Path

from backend.rules.kubernetes_rules import KUBERNETES_RULES


class RuleLoader:

    """

    Loads trusted Kubernetes rules for analysis.

    """

    def __init__(self):

        self.promoted_rules_file = (

            Path(__file__).parent / "promoted_rules.json"

        )

    def load_rules(self):

        """

        Return combined built-in and promoted rules.

        """

        rules = dict(KUBERNETES_RULES)

        promoted_rules = self._load_promoted_rules()

        for rule in promoted_rules:

            if rule.get("status") != "promoted":

                continue

            pattern = rule.get("pattern")

            if not pattern:

                continue

            rules[pattern] = {

                "root_cause": rule["root_cause"],

                "severity": rule["severity"],

                "confidence": rule["confidence"],

                "explanation": rule["explanation"],

                "recommendations": rule["recommendations"],

                "commands": rule["commands"],

            }

        return rules

    def _load_promoted_rules(self):

        """

        Load promoted rules from persistent storage.

        """

        if not self.promoted_rules_file.exists():

            return []

        with open(

            self.promoted_rules_file,

            "r",

            encoding="utf-8"

        ) as file:

            return json.load(file)
 