import React, { useState, useRef, useEffect } from "react";
import "./chatInterface.css";
import { checkBackendHealth } from "../../services/health";
import { sendChatMessage } from "../../services/chat";
import GeneratePDF from "../GeneratePDF";
import { selectTopDatalist } from "../../services/selectTopDatalist"; 
import axios from "axios";
import InitialDatalistRadioGroup from "./InitialDatalistRadioGroup";
import Top10DatalistRadioGroup from "./Top10DatalistRadioGroup";
import { downloadDynamicPdf } from "../GeneratePDF";

const initialOptions = [{
    label: "Persons",
    id:"726"
}];

const ChatInterface = () => {
  const [selectedOption, setSelectedOption] = useState("");
  const [updateState, setUpdateState] = useState(false);
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Choose a datalist from below:"
    }
  ]);
  const [input, setInput] = useState("");
  const messagesEndRef = useRef(null);
  const [status, setStatus] = useState(null);
  const [topDatalists, setTopDatalists] = useState([]);
  const [selectedTopDatalist, setSelectedTopDatalist] = useState("");
  const [topDatalistDisabled, setTopDatalistDisabled] = useState(false);

  const [enablePrompt, setEnablePrompt] = useState(false);

  useEffect(() => {
    let mounted = true;
    checkBackendHealth().then((res) => {
      if (mounted) setStatus(res.status);
    });
    return () => { mounted = false; };
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleRadioChange = async (e) => {
    const value = e.target.value;
    if (!updateState) {
      setSelectedOption(value);
      setUpdateState(true);
      try {
        const res = await axios.post('/api/datalist', { selected: value });
        setMessages(prev => [
          ...prev,
          { sender: "bot", text: res.data.response }
        ]);
        // If backend returns array of objects, keep the entire object
       
          setTopDatalists(res.data.top10);
       
      } catch (err) {
        setMessages(prev => [
          ...prev,
          { sender: "bot", text: "Error fetching datalist info." }
        ]);
      }
    }
  };

  const handleTopDatalistChange = async (e) => {
    const value = e.target.value;
    
    setEnablePrompt(true);
    if (!topDatalistDisabled) {
      setSelectedTopDatalist(value);
      setTopDatalistDisabled(true);
      setMessages(prev => [
        ...prev,
        { sender: "bot", text: `You selected top datalist: ${value}` }
      ]);
      // Find the full object for the selected value
      const selectedObj = topDatalists[e.target.id]
      console.log('topDatalists',selectedObj)
      // Call backend service for selected top datalist
      try {
        const res = await selectTopDatalist(selectedObj);
        console.log('RES',res);
        setMessages(prev => [
          ...prev,
          { sender: "bot", text: "Record selection acknowledged." }
        ]);
        downloadDynamicPdf(res.data.response.mapped_selected);

      } catch (err) {
        setMessages(prev => [
          ...prev,
          { sender: "bot", text: "Error sending selected record to backend." }
        ]);
      }
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    const botReply = await sendChatMessage(input);
    setMessages((prev) => [
      ...prev,
      { sender: "bot", text: (
        <span>
          {botReply ? botReply : "Sorry, no response."} <GeneratePDF />
        </span>
      ) }
    ]);
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-message ${msg.sender === "user" ? "user" : "bot"}`}
          >
            {typeof msg.text === "string"
              ? <span>{msg.text}</span>
              : msg.text}
            {/* Show radio group only for the first bot message and if not selected */}
            {idx === 0 && msg.sender === "bot" && (
              <InitialDatalistRadioGroup
                options={initialOptions}
                selectedOption={selectedOption}
                updateState={updateState}
                onSelect={handleRadioChange}
              />
            )}
            {/* Show top 10 datalists radio group after first selection */}
            {idx === messages.length - 1 && topDatalists.length > 0 && msg.sender === "bot" && !topDatalistDisabled && (
              <div style={{ marginTop: 16 }}>
                <div style={{ fontWeight: 'bold', marginBottom: 4 }}>Search for records:</div>
                <Top10DatalistRadioGroup
                  options={topDatalists.map(obj => obj.recordName)}
                  selectedOption={selectedTopDatalist}
                  updateState={topDatalistDisabled}
                  onSelect={handleTopDatalistChange}
                />
              </div>
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-status-bar">
        Backend status: <span className={`status-badge ${status === 'OK' ? 'ok' : status === 'ERROR' ? 'error' : 'checking'}`}>{status || 'Checking...'}</span>
      </div>
      {enablePrompt && (
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
        )}
    </div>
  );
};

export default ChatInterface;
