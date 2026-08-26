document.addEventListener("DOMContentLoaded", () => {
    const generateBtn = document.getElementById("generateBtn");
    const refineBtn = document.getElementById("refineBtn");
    const clearBtn = document.getElementById("clearBtn");
    
    const articleInput = document.getElementById("articleInput");
    const refinementInput = document.getElementById("refinementInput");

    const placeholderState = document.getElementById("placeholderState");
    const loadingState = document.getElementById("loadingState");
    const resultsContainer = document.getElementById("resultsContainer");

    // Tab Navigation Logic
    const tabBtns = document.querySelectorAll(".tab-btn");
    tabBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
            document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
            
            btn.classList.add("active");
            document.getElementById(btn.getAttribute("data-target")).classList.add("active");
        });
    });

    // Generate Posts API Call
    generateBtn.addEventListener("click", async () => {
        const text = articleInput.value.trim();
        if (!text) {
            alert("Please paste some content first!");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text_input: text })
            });

            if (!response.ok) throw new Error("Failed to generate posts.");

            const data = await response.json();
            renderResults(data);
        } catch (error) {
            alert("Error: " + error.message);
            setLoading(false);
        }
    });

    // Refinement API Call
    refineBtn.addEventListener("click", async () => {
        const text = refinementInput.value.trim();
        if (!text) return;

        setLoading(true);

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ text_input: text })
            });

            if (!response.ok) throw new Error("Failed to update posts.");

            const data = await response.json();
            renderResults(data);
            refinementInput.value = "";
        } catch (error) {
            alert("Error: " + error.message);
            setLoading(false);
        }
    });

    // Clear Session
    clearBtn.addEventListener("click", async () => {
        await fetch("/api/clear", { method: "POST" });
        articleInput.value = "";
        refinementInput.value = "";
        resultsContainer.classList.add("hidden");
        placeholderState.classList.remove("hidden");
        alert("Session cleared successfully!");
    });

    function setLoading(isLoading) {
        if (isLoading) {
            placeholderState.classList.add("hidden");
            resultsContainer.classList.add("hidden");
            loadingState.classList.remove("hidden");
        } else {
            loadingState.classList.add("hidden");
            resultsContainer.classList.remove("hidden");
        }
    }

    function renderResults(data) {
        setLoading(false);
        
        // LinkedIn
        document.getElementById("linkedinText").textContent = data.linkedin || "";

        // Twitter Thread
        const twitterContainer = document.getElementById("twitterContainer");
        twitterContainer.innerHTML = "";
        if (Array.isArray(data.twitter)) {
            data.twitter.forEach((tweet, index) => {
                const div = document.createElement("div");
                div.className = "tweet-card";
                div.innerHTML = `<div class="tweet-num">Tweet ${index + 1}/${data.twitter.length}</div><div>${tweet}</div>`;
                twitterContainer.appendChild(div);
            });
        }

        // Instagram
        document.getElementById("instagramText").textContent = data.instagram || "";
    }
});

// Clipboard Utility Functions
function copyContent(elementId) {
    const text = document.getElementById(elementId).textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert("Copied to clipboard!");
    });
}

function copyTwitterThread() {
    const tweets = document.querySelectorAll(".tweet-card");
    let fullThread = "";
    tweets.forEach((t, i) => {
        fullThread += `--- Tweet ${i+1} ---\n` + t.innerText.split("\n").slice(1).join("\n") + "\n\n";
    });
    navigator.clipboard.writeText(fullThread.trim()).then(() => {
        alert("Twitter thread copied to clipboard!");
    });
}