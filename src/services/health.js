// Utility to call the Flask backend health API using axios
import axios from 'axios';

export async function checkBackendHealth() {
  try {
    const response = await axios.get('http://localhost:5000/health');
    return response.data;
  } catch (error) {
    return { status: 'ERROR', error: error.message };
  }
}
