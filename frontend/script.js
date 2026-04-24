document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    function addMessage(content, sender="user") {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${sender}-message`;
        
        const avatar = document.createElement("div");
        avatar.className = "avatar";
        avatar.textContent = sender === "user" ? "👤" : "🤖";

        const textDiv = document.createElement("div");
        textDiv.className = "content";
        textDiv.innerHTML = content.replace(/\n/g, "<br>"); // simple formatting

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(textDiv);
        chatBox.appendChild(msgDiv);
        
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function addLoader() {
        const msgDiv = document.createElement("div");
        msgDiv.className = "message system-message loader-msg";
        msgDiv.innerHTML = `
            <div class="avatar">🤖</div>
            <div class="content">
                <div class="loading">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return msgDiv;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if(!text) return;

        addMessage(text, "user");
        userInput.value = "";
        
        const loader = addLoader();

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: text })
            });
            const data = await response.json();
            
            loader.remove();
            
            if(data.error) {
                addMessage("Oops! Something went wrong: " + data.error, "system");
            } else {
                addMessage(data.response, "system");
            }
        } catch (error) {
            loader.remove();
            addMessage("Network Error. Ensure FastAPI is running.", "system");
        }
    }

    sendBtn.addEventListener("click", sendMessage);
    userInput.addEventListener("keypress", (e) => {
        if(e.key === "Enter") sendMessage();
    });
});
