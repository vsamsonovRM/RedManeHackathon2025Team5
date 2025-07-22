from flask import Flask, jsonify, request
from flask_cors import CORS
from infrastructure.llm_infrastructure import LLMInfrastructure

app = Flask(__name__)
LLM_INFRASTRUCTURE = LLMInfrastructure()

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
