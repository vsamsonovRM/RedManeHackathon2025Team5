import logo from './logo.svg';
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
      </header>
    </div>
  );
}

export default App;
