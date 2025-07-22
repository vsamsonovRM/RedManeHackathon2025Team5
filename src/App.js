import ChatInterface from './components/Chat/chatInterface';
import './App.css';
import { useState } from 'react';
import axios from 'axios';

function App() {

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

getHealthStatus().then((status) => {
  const HEALTH_CONSTANT = status;
  console.log('Stored Health Constant:', HEALTH_CONSTANT);
});

  // Usage example
  return (
    <div className="App">
      <header>
        mGenerate
      </header>
      <ChatInterface />
    </div>
  );
}

export default App;
