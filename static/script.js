console.log("CloudOps AI script loaded");
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM Loaded");
    document
        .getElementById("analyzeBtn")
        .addEventListener("click", () => {
            console.log("Analyze button clicked");
            analyzeLog();
            });
});

async function analyzeLog() {

    const log = document.getElementById("logInput").value;

    const button = document.getElementById("analyzeBtn");

    const loading = document.getElementById("loading");

    const report = document.getElementById("reportContainer");

    const error = document.getElementById("errorMessage");

    button.disabled = true;

    loading.classList.remove("hidden");

    report.classList.add("hidden");

    error.classList.add("hidden");

    try {

        const response = await fetch("/analyze", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                log: log
            })

        });

        const data = await response.json();

        loading.classList.add("hidden");

        button.disabled = false;

        if (data.status.toLowerCase() === "error") {

            showError(data.message);

            return;

        }

        renderReport(data);

    }

    catch (err) {

        loading.classList.add("hidden");

        button.disabled = false;

        showError(err);

    }

}

function renderReport(data) {

    document.getElementById("confidence").textContent =
    data.confidence || "AI Generated";

    document.getElementById("reportContainer")
        .classList.remove("hidden");

    document.getElementById("source").textContent =
        data.Source || data.source || "-";

    const severityBadge =
        document.getElementById("severity");

    const severity =
        data.severity || "Unknown";

    severityBadge.textContent = severity;

    severityBadge.className = "badge";

    switch (severity.toLowerCase()) {

        case "high":
            severityBadge.classList.add("high");
            break;

        case "medium":
            severityBadge.classList.add("medium");
            break;

        case "low":
            severityBadge.classList.add("low");
            break;

        default:
            severityBadge.classList.add("unknown");

    }

    document.getElementById("rootCause").textContent =
        data.root_cause || "Not Available";

    document.getElementById("explanation").textContent =
        data.explanation ||
        data.Analysis ||
        "No explanation available.";

    const recommendationList =
        document.getElementById("recommendations");

    recommendationList.innerHTML = "";

    if (data.recommendations) {

        data.recommendations.forEach(item => {

            addRecommendation(item);

        });

    }

    document.getElementById("commands").textContent =
    data.commands
        ? data.commands.join("\n")
        : "";
}

function addRecommendation(text) {

    const li = document.createElement("li");

    li.textContent = text;

    document
        .getElementById("recommendations")
        .appendChild(li);

}

function showError(message) {

    const error =
        document.getElementById("errorMessage");

    error.classList.remove("hidden");

    error.innerHTML = `
        <strong>Analysis Failed</strong><br><br>
        ${message}
    `;

}