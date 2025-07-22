import axios from 'axios';

export async function sendChatMessage(message, knowledgeBase) {
  try {
    const response = await axios.post('/api/chat', {
      chat: message,
      knowledgeBase: knowledgeBase
    });
    return response.data.response;
  } catch (error) {
    console.error('Error sending chat:', error);
    return null;
  }
}
