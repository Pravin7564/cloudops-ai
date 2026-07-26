alert("Script version 2");
console.log("CloudOps AI script loaded version 2");
document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM Loaded");
    document
        .getElementById("clearFileBtn")
        .addEventListener("click", clearFile);

    document
        .getElementById("logFile")
        .addEventListener("change", loadFile);
        
    document
        .getElementById("analyzeBtn")
        .addEventListener("click", () => {
            console.log("Analyze button clicked");
            analyzeLog();
            });
});


function loadFile(event){

    console.log("loadfile() called")
    const file = event.target.files[0];

    if(!file){
        return;
    }

    let size = file.size;

    let displaySize;

    if(size < 1024) {
        displaySize = size + "Bytes";
    }

    else if(size < 1024 * 1024){
        displaySize = (size / 1024).toFixed(1) + "KB";
    }

    else{

        displaySize = (size / (1024 * 1024)).toFixed(2) + "MB";
    }

    document.getElementById("selectedFile").innerHTML =
    "📄 <b> " + file.name + "</b><br>" +
    displaySize + "<br>" +
    "✅ Ready for analysis";

    const reader = new FileReader();

    reader.onload = function(e){

        document.getElementById("logInput").value = 
        e.target.result;
    };
    reader.readAsText(file);
}

function clearFile(){

    document.getElementById("logFile").value = "";

    document.getElementById("logInput").value = "";

    document.getElementById("selectedFile").textContent = 
    "No file selected";
}

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

        let data;

        try{
            data = await response.json();
        } catch(parseError){
            throw new Error(
                "The server returned an invalid response."
            );
        }

        loading.classList.add("hidden");

        button.disabled = false;

        if(!response.ok){
            showError(
                data.message || "The server failed to analyze the log."
            );
            return;
        }

        if(
            data.status && 
            data.status.toLowerCase() == "error"
        ){
            showError(
                data.message || "AI service failed to analyze the log."
            );
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
    //Gemini response contain analysis inside data.analysis.
    // Rule engine responses contain analysis directly in data.
    
    const analysis = data.Analysis || data;

    document.getElementById("confidence").textContent =
    analysis.confidence || "AI Generated";

    document.getElementById("reportContainer")
        .classList.remove("hidden");

    document.getElementById("source").textContent =
        data.Source || data.source || "-";

    const severityBadge =
        document.getElementById("severity");

    const severity =
        analysis.severity || "Unknown";

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
        analysis.root_cause || "Not Available";

    document.getElementById("explanation").textContent =
        analysis.explanation ||
        "No explanation available.";

    const recommendationList =
        document.getElementById("recommendations");

    recommendationList.innerHTML = "";

    if (Array.isArray(analysis.recommendations)){

        analysis.recommendations.forEach(item => {

            addRecommendation(item);

        });
    
    }

    document.getElementById("commands").textContent =
    Array.isArray(analysis.commands)
        ? analysis.commands.join("\n")
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