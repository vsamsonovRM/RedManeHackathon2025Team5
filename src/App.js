import ChatInterface from './components/Chat/chatInterface';
import './App.css';
import Header from './components/header/header';
import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [setCurrMessage] = useState("");

  // Dummy initial chat function
  const sendChat = async () => {
    try {
      const res = await axios.post('/api/chat', {
        chat: 'what is your name'
      });
      console.log(res.data.response);
      setCurrMessage(res.data.response);
    } catch (err) {
      console.error('Error sending chat:', err);
    }
  };

  useEffect(() => {
    sendChat();
  }, []);

  return (
    <div className="App">
      <Header />
      {/* Show the dummy initial chat message */}
      {/* {currMessage && (
        <div style={{textAlign: 'center', margin: '1em', color: '#1976d2', fontWeight: 500}}>
          Initial bot reply: {currMessage}
        </div>
      )} */}
      <ChatInterface />
    </div>
  );
}

export default App;
