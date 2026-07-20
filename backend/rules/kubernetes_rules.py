"""
Kubernetes rule definitions.

This module contains known Kubernetes log patterns
and their corresponding analysis results.
"""

KUBERNETES_RULES = {

    "CrashLoopBackOff": {

        "root_cause":
            "The container is repeatedly crashing after startup.",

        "severity":
            "High",

        "confidence":
            "95%",

        "explanation":
            (
                "Kubernetes restarts the container whenever it exits "
                "unexpectedly. After several consecutive failures, the "
                "pod enters the CrashLoopBackOff state to prevent "
                "continuous restart attempts."
            ),

        "recommendations": [

            "Inspect the application logs for runtime errors.",

            "Verify ConfigMaps and Secrets are correctly mounted.",

            "Check environment variables required by the application.",

            "Verify CPU and memory resource limits.",

            "Confirm the container image starts successfully."

        ],

        "commands": [

            "kubectl logs <pod-name>",

            "kubectl describe pod <pod-name>",

            "kubectl get events --sort-by=.lastTimestamp",

            "kubectl get pods -A"

        ]

    },

    "ImagePullBackOff": {

        "root_cause":
            "Kubernetes cannot pull the requested container image.",

        "severity":
            "High",

        "confidence":
            "98%",

        "explanation":
            (
                "The kubelet attempted to download the container image "
                "from the configured registry but failed. This can happen "
                "because the image name is incorrect, authentication is "
                "missing, or the registry is unavailable."
            ),

        "recommendations": [

            "Verify the image name and tag.",

            "Check imagePullSecrets configuration.",

            "Confirm registry connectivity.",

            "Verify registry credentials.",

            "Ensure the image exists."

        ],

        "commands": [

            "kubectl describe pod <pod-name>",

            "kubectl get secret",

            "kubectl get events",

            "kubectl describe serviceaccount default"

        ]

    }

}