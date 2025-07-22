from flask import Flask, jsonify, request
from flask_cors import CORS
from infrastructure.llm_infrastructure import LLMInfrastructure

app = Flask(__name__)
LLM_INFRASTRUCTURE = LLMInfrastructure()
# AzureEndpoint: https://rm-shared-open-ai.openai.azure.com Model: GPT-4.1-mini Deployment: gpt-4.1-mini Version: 2025-04-14 Key: 6e4d8096797d4ef6a19a834f92e97103
CORS(app)
# Home route
@app.route('/')
def home():
    return "Welcome to the Flask app!"

# Example API route
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify({
        "you_sent": data
    })

# Health check route
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "OK"}), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('chat')  # Get "chat" from POST body
    response = LLM_INFRASTRUCTURE.get_response(user_input)
    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(debug=True)
