import React, { useState } from "react";
import axios from "axios";
import "./ChatbotBox.css";

const ChatbotBox = () => {
  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const newChat = [...chat, { from: "user", text: message }];
    setChat(newChat);
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:5000/chatbot", { message });
      setChat([...newChat, { from: "bot", text: res.data.response }]);
    } catch (err) {
      console.error("❌ Chatbot Error:", err);
      setChat([...newChat, { from: "bot", text: "⚠️ Failed to connect to chatbot." }]);
    }

    setMessage("");
    setLoading(false);
  };

  return (
    <div className="chatbot-container">
      <h3>Ask ProductBot</h3>
      <div className="chat-window">
        {chat.map((c, i) => (
          <div key={i} className={c.from}>
            {c.text}
          </div>
        ))}
        {loading && <div className="bot">Typing...</div>}
      </div>
      <div className="chat-input">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask about products..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatbotBox;
