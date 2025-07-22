import React, { useState, useRef, useEffect } from "react";
import "./chatInterface.css";
import { checkBackendHealth } from "../../services/health";
import GeneratePDF from "../GeneratePDF";



const ChatInterface = () => {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hello! How can I help you today?" }
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);

  const [status, setStatus] = useState(null);
  
    useEffect(() => {
      let mounted = true;
      checkBackendHealth().then((res) => {
        if (mounted) setStatus(res.status);
      });
      return () => { mounted = false; };
    }, []);

    const [responseStatus,setResponseStatus] = useState(false);
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    setResponseStatus(true);
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: input }
    ]);
    // Simulate bot response
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: (
            <span>
              You said: {input} 
              {responseStatus && <GeneratePDF />}
            </span>
          ) }
      ]);
    }, 600);
    setInput("");
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {msg.text}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-status-bar">
        Backend status: <span className={`status-badge ${status === 'OK' ? 'ok' : status === 'ERROR' ? 'error' : 'checking'}`}>{status || 'Checking...'}</span>
      </div>
      <form className="chat-input-form" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="chat-input"
        />
        <button type="submit" className="chat-send-btn">Send</button>
      </form>
    </div>
  );
};

export default ChatInterface;
