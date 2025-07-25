document.addEventListener("DOMContentLoaded", function () {
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const chatBox = document.getElementById("chat-box");

    // Function to add message
    function addMessage(message, sender) {
        const msg = document.createElement("div");
        msg.classList.add("message", sender === "user" ? "user-message" : "bot-message");
        msg.textContent = message;
        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    // Function to send message to FastAPI
    async function sendMessage(message) {
        addMessage(message, "user");

        try {
            const response = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ question: message })
            });

            const data = await response.json();
            addMessage(data.answer || "No response from bot.", "bot");
        } catch (error) {
            console.error("Error:", error);
            addMessage("⚠️ Server not reachable. Please check your backend.", "bot");
        }
    }

    // Handle form submission
    chatForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const msg = userInput.value.trim();
        if (msg) {
            sendMessage(msg);
            userInput.value = "";
        }
    });
});
