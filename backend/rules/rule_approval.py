"""

Rule approval workflow.

Handles human review of AI-generated Kubernetes rule candidates.

Approved rules are marked as approved.

Rejected rules are marked as rejected.

"""

from backend.rules.candidate_rule_store import CandidateRuleStore
from datetime import datetime,timezone
from backend.rules.rule_promoter import RulePromoter
class RuleApproval:

    """

    Handles human approval and rejection of AI-generated rules.

    """

    def __init__(self):

        self.store = CandidateRuleStore()
        self.promoter = RulePromoter()

    def list_candidates(self):

        """

        Return all candidate rules.

        """

        return self.store._load()

    def approve(self, pattern: str):

        """

        Approve a candidate rule by pattern.

        """

        candidates = self.store._load()

        for candidate in candidates:

            if candidate.get("pattern") == pattern:

                if candidate.get("status") == "approved":

                    return {

                        "status": "already_approved",

                        "message": (

                            "This rule candidate is already approved."

                        ),

                        "pattern": pattern,

                    }

                candidate["status"] = "approved"
                candidate["approved_at"] = datetime.now(timezone.utc).isoformat()

                self.store._save(candidates)

                return {

                    "status": "success",

                    "message": (

                        "Rule candidate approved successfully."

                    ),

                    "pattern": pattern,

                }

        return {

            "status": "not_found",

            "message": (

                "No rule candidate found with this pattern."

            ),

            "pattern": pattern,

        }

    def reject(self, pattern: str):

        """

        Reject a candidate rule by pattern.

        """

        candidates = self.store._load()

        for candidate in candidates:

            if candidate.get("pattern") == pattern:

                if candidate.get("status") == "rejected":

                    return {

                        "status": "already_rejected",

                        "message": (

                            "This rule candidate is already rejected."

                        ),

                        "pattern": pattern,

                    }

                candidate["status"] = "rejected"

                self.store._save(candidates)

                return {

                    "status": "success",

                    "message": (

                        "Rule candidate rejected successfully."

                    ),

                    "pattern": pattern,

                }

        return {

            "status": "not_found",

            "message": (

                "No rule candidate found with this pattern."

            ),

            "pattern": pattern,

        }

    def promote(self, pattern: str):
       """
       Promote an approved rule candidate into
       the production Kubernetes rule engine.
       """
       candidates = self.store._load()

       candidate = None

       for item in candidates:
           if item.get("pattern") == pattern:
               candidate = item
               break

       if candidate is None:
           return {
               "status": "error",
               "message": "Rule candidate not found.",
               "pattern": pattern,
           }
       if candidate.get("status") != "approved":
           return {
               "status": "error",
               "message": (
                   "Only approved rule candidates "
                   "can be promoted."
               ),
               "pattern": pattern,
           }
       return self.promoter.promote(candidate)
       