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

    },

    "OOMKilled": {

        "root_cause":

            "The container was terminated because it exceeded its memory limit.",

        "severity":

            "High",

        "confidence":

            "98%",

        "explanation":

            (

                "The Kubernetes container was terminated by the operating "

                "system after exceeding its configured memory limit. "

                "This usually indicates that the application requires more "

                "memory than the container limit allows or has a memory leak."

            ),

        "recommendations": [

            "Inspect the pod's previous container logs for memory-related errors.",

            "Check the container memory requests and limits.",

            "Monitor the application's memory consumption over time.",

            "Investigate possible memory leaks in the application.",

            "Increase the memory limit if higher memory usage is expected."

        ],

        "commands": [

            "kubectl describe pod <pod-name>",

            "kubectl logs <pod-name> --previous",

            "kubectl top pod <pod-name>",

            "kubectl get pod <pod-name> -o yaml"

        ]

    },
    "FailedMount": {

        "root_cause":

            "Kubernetes failed to mount the required volume into the pod.",

        "severity":

            "High",

        "confidence":

            "95%",

        "explanation":

            (

                "The kubelet was unable to mount a required volume for the "

                "pod. This can be caused by storage attachment problems, "

                "CSI driver failures, incorrect mount configuration, "

                "permission issues, or a volume that is already attached "

                "to another node."

            ),

        "recommendations": [

            "Inspect the pod events for the exact volume mount error.",

            "Verify that the PersistentVolumeClaim is in Bound status.",

            "Check the health and logs of the CSI driver.",

            "Check for volume attachment or multi-attach conflicts.",

            "Verify storage permissions and node connectivity."

        ],

        "commands": [

            "kubectl describe pod <pod-name> -n <namespace>",

            "kubectl get pvc -n <namespace>",

            "kubectl get pv",

            "kubectl get volumeattachment",

            "kubectl get events -n <namespace> --sort-by=.lastTimestamp"

        ]

    },

    "ErrImagePull": {

        "root_cause":

            "Kubernetes failed to pull the requested container image.",

        "severity":

            "High",

        "confidence":

            "98%",

        "explanation":

            (

                "The kubelet attempted to pull the container image but "

                "the image retrieval failed. Common causes include an "

                "incorrect image name or tag, missing registry credentials, "

                "registry connectivity problems, or an unavailable image."

            ),

        "recommendations": [

            "Verify the container image name and tag.",

            "Check whether the image exists in the configured registry.",

            "Verify imagePullSecrets configuration.",

            "Check registry authentication credentials.",

            "Verify connectivity between the Kubernetes node and registry."

        ],

        "commands": [

            "kubectl describe pod <pod-name> -n <namespace>",

            "kubectl get pod <pod-name> -o jsonpath='{.spec.containers[*].image}'",

            "kubectl get secrets -n <namespace>",

            "kubectl get events -n <namespace> --sort-by=.lastTimestamp"

        ]

    },

    "Pending": {

        "root_cause":

            "The pod cannot be scheduled onto an available Kubernetes node.",

        "severity":

            "Medium",

        "confidence":

            "92%",

        "explanation":

            (

                "The pod remains in Pending state because the Kubernetes "

                "scheduler cannot find a suitable node. Common causes "

                "include insufficient CPU or memory, node taints, "

                "node selectors, affinity rules, or unavailable resources."

            ),

        "recommendations": [

            "Inspect pod events for scheduler failure messages.",

            "Check available CPU and memory resources on cluster nodes.",

            "Verify node taints and pod tolerations.",

            "Review nodeSelector and affinity configuration.",

            "Check whether all cluster nodes are Ready."

        ],

        "commands": [

            "kubectl describe pod <pod-name> -n <namespace>",

            "kubectl get nodes",

            "kubectl describe nodes",

            "kubectl top nodes",

            "kubectl get events -n <namespace> --sort-by=.lastTimestamp"

        ]

    },

    "CreateContainerConfigError": {

        "root_cause":

            "Kubernetes could not create the container because its configuration is invalid or required configuration is missing.",

        "severity":

            "High",

        "confidence":

            "95%",

        "explanation":

            (

                "The kubelet was unable to create the container because "

                "a required configuration value could not be resolved. "

                "Common causes include missing ConfigMaps, missing Secrets, "

                "incorrect environment variable references, or invalid "

                "volume configuration."

            ),

        "recommendations": [

            "Inspect pod events for the exact configuration error.",

            "Verify that referenced ConfigMaps exist.",

            "Verify that referenced Secrets exist.",

            "Check environment variable references in the pod specification.",

            "Review volume and volumeMount configuration."

        ],

        "commands": [

            "kubectl describe pod <pod-name> -n <namespace>",

            "kubectl get configmap -n <namespace>",

            "kubectl get secret -n <namespace>",

            "kubectl get pod <pod-name> -o yaml",

            "kubectl get events -n <namespace> --sort-by=.lastTimestamp"

        ]

    }
  
}