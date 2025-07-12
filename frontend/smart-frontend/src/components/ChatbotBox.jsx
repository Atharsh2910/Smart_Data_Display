import React, { useState } from 'react';
import axios from 'axios';
import './ChatbotBox.css';

function ChatbotBox() {
  const [input, setInput] = useState('');
  const [chat, setChat] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: 'user', text: input };
    setChat([...chat, userMessage]);

    try {
      const response = await axios.post('/chatbot', { message: input });
      const botMessage = { sender: 'bot', text: response.data.response };
      setChat(prev => [...prev, botMessage]);
    } catch (error) {
      setChat(prev => [...prev, { sender: 'bot', text: 'Error contacting chatbot.' }]);
    }

    setInput('');
  };

  return (
    <div className="chatbot-box">
      <div className="chat-history">
        {chat.map((msg, idx) => (
          <div key={idx} className={`chat-msg ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={input}
          placeholder="Ask something..."
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default ChatbotBox;
