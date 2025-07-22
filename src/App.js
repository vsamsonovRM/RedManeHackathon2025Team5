import ChatInterface from './components/Chat/chatInterface';
import './App.css';
import { useEffect, useState } from 'react';
import { checkBackendHealth } from './services/health';

function App() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    checkBackendHealth().then(setHealth);
  }, []);

  return (
    <div className="App">
      <header>
        mGenerate
        <div style={{ fontSize: '0.9em', marginTop: 8 }}>
          Backend health: {health ? health.status : 'Checking...'}
        </div>
      </header>
      <ChatInterface />
    </div>
  );
}

export default App;
