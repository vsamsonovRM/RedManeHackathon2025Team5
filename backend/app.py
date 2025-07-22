from flask import Flask, jsonify, request
from flask_cors import CORS
from infrastructure.llm_infrastructure import LLMInfrastructure
from infrastructure.search_infrastructure import SearchInfrastructure

app = Flask(__name__)
LLM_INFRASTRUCTURE = LLMInfrastructure()
SEARCH_INFRASTRUCTURE = SearchInfrastructure()

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


@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    user_input = data.get('search_term')  # Get "chat" from POST body
    data_list_id = data.get('data_list_id')
    response = SEARCH_INFRASTRUCTURE.search_record(user_input, data_list_id)
    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(debug=True)
