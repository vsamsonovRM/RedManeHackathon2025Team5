import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
import axios from 'axios';

function App() {
const [currMessage, setCurrMessage] = useState();
async function getHealthStatus() {
  try {
    const response = await axios.get('/health');
    const healthStatus = response.data; // or response.data.status if you only need the value
    console.log('Health status:', healthStatus);
    return healthStatus;
  } catch (error) {
    console.error('Error fetching health status:', error);
    return null;
  }
}

const sendChat = async () => {
  try {
    const res = await axios.post('/api/chat', {
      chat: 'what is your name'
    });
    console.log(res.data.response);
    setCurrMessage(res.data.response)
  } catch (err) {
    console.error('Error sending chat:', err);
  }
};

getHealthStatus().then((status) => {
  const HEALTH_CONSTANT = status;
  console.log('Stored Health Constant:', HEALTH_CONSTANT);
});

  // Usage example
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
       
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        <button onClick={sendChat}>Hello</button>
        <text>{currMessage}</text>
      </header>
    </div>
  );
}

export default App;
