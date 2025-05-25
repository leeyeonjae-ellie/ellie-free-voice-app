const sendBtn = document.getElementById("send-btn");
const micBtn = document.getElementById("mic-btn");
const userInput = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");

sendBtn.onclick = async () => {
  const message = userInput.value.trim();
  if (!message) return;
  appendMessage("You", message);
  userInput.value = "";
  const res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  const data = await res.json();
  if (data.response) {
    appendMessage("Ellie", data.response);
    if (data.audio) {
      const audio = new Audio(data.audio);
      audio.play();
    }
  } else {
    appendMessage("Ellie", "Sorry, something went wrong.");
  }
};

micBtn.onclick = () => {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = "en-US";
  recognition.start();
  recognition.onresult = (e) => {
    userInput.value = e.results[0][0].transcript;
    sendBtn.click();
  };
};

function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.className = "message";
  msg.innerHTML = `<strong>${sender}:</strong> ${text}`;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}
