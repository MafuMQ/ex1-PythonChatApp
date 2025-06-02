// --- User info ---
let userName = "User" + Math.floor(Math.random() * 1000);
let iconStyle = Math.random() > 0.5 ? "girl" : "boy";
let iconURL = `https://avatar.iran.liara.run/public/${iconStyle}?username=${userName}`;
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('username').textContent = userName;
    document.getElementById('avatar').src = iconURL;
});

let lastTimestamp = 0;

async function fetchMessages() {
    try {
        const res = await fetch(`/api/get_messages?since=${lastTimestamp}`);
        const msgs = await res.json();
        if (msgs.length > 0) {
            msgs.forEach(msg => {
                appendMessage(msg);
                if (msg.timestamp > lastTimestamp) lastTimestamp = msg.timestamp;
            });
        }
    } catch (e) {
        // Optionally handle error
    }
}

function appendMessage(data) {
    const chat = document.getElementById('chat');
    const msgDiv = document.createElement('div');
    msgDiv.className = 'message';
    msgDiv.innerHTML = `<img src="${data.iconURL}" width="24" height="24" style="vertical-align:middle;border-radius:50%;"> <span class="username">${data.userName}:</span> ${data.message}`;
    chat.appendChild(msgDiv);
    chat.scrollTop = chat.scrollHeight;
}

setInterval(fetchMessages, 1000);

document.addEventListener('DOMContentLoaded', () => {
    // --- Send message ---
    document.getElementById('message-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        const input = document.getElementById('message-input');
        const message = input.value.trim();
        if (message) {
            await fetch('/api/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userName: userName,
                    iconURL: iconURL,
                    message: message
                })
            });
            input.value = '';
        }
    });

    // --- Change username ---
    document.getElementById('username-form').addEventListener('submit', function(e) {
        e.preventDefault();
        const newUserName = document.getElementById('new-username').value.trim();
        if (newUserName) {
            userName = newUserName;
            iconURL = `https://avatar.iran.liara.run/public/${iconStyle}?username=${userName}`;
            document.getElementById('username').textContent = userName;
            document.getElementById('avatar').src = iconURL;
            document.getElementById('new-username').value = '';
            // Optionally, send a system message about the name change
            fetch('/api/send_message', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    userName: "System",
                    iconURL: "",
                    message: `User changed their name to ${userName}`
                })
            });
        }
    });
});