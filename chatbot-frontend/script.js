document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    sendButton.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") sendMessage();
    });

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage(message, "user-message");
        userInput.value = "";
        
        fetch('https://ai-agents-academy.onrender.com/', {
            method: 'POST',
            body: JSON.stringify({ message: userInput }),
            headers: { 'Content-Type': 'application/json' }
          })

        .then(response => response.json())
        .then(data => appendMessage(data.response, "bot-message"))
        .catch(error => console.error("Error:", error));
    }

    function appendMessage(text, className) {
        const messageDiv = document.createElement("div");
        messageDiv.classList.add(className);
        messageDiv.textContent = text;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;  // Auto-scroll to latest message
    }
});