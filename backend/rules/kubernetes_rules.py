"""
Kubernetes rule definitions.

This module contains known Kubernetes log patterns
and their corresponding analysis results.
"""

KUBERNETES_RULES = {
    "CrashLoopBackOff": {
        "root_cause": "Container is repeatedly crashing.",
        "severity": "High",
        "confidence": 95
    },

    "ImagePullBackOff": {
        "root_cause": "Container image could not be pulled.",
        "severity": "High",
        "confidence": 95
    },

    "OOMKilled": {
        "root_cause": "Container was terminated due to insufficient memory.",
        "severity": "Critical",
        "confidence": 98
    }
}