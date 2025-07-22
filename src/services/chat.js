import axios from 'axios';

export async function sendChatMessage(message) {
  try {
    const response = await axios.post('/api/chat', {
      chat: message
    });
    return response.data.response;
  } catch (error) {
    console.error('Error sending chat:', error);
    return null;
  }
}
