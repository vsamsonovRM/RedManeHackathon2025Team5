from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from infrastructure.llm_infrastructure import LLMInfrastructure
from fpdf import FPDF
from io import BytesIO
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


class BoxedPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=False)

    def add_boxed_block(self, header, body):
        padding = 3
        left_margin = self.l_margin
        max_width = self.w - self.r_margin - left_margin

        x_start = self.get_x()
        y_start = self.get_y()

        self.set_font("Arial", 'B', 16)
        header_height = self.font_size + 4

        self.set_font("Arial", '', 12)
        body_lines = self.multi_cell(max_width - 2 * padding, 8, body, split_only=True)
        body_height = len(body_lines) * 8

        total_height = header_height + body_height + 3 * padding

        if y_start + total_height > self.page_break_trigger:
            self.add_page()
            x_start = self.get_x()
            y_start = self.get_y()

        # Draw box
        self.set_line_width(0.5)
        self.rect(x_start, y_start, max_width, total_height)

        # Draw text
        self.set_xy(x_start + padding, y_start + padding)

        self.set_font("Arial", 'B', 16)
        self.cell(max_width - 2 * padding, 10, txt=header, ln=True)

        self.set_font("Arial", '', 12)
        self.multi_cell(max_width - 2 * padding, 8, txt=body)

        # Adjust Y to overlap the bottom of the current box with the top of the next
        self.set_y(y_start + total_height)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        content = request.get_json()

        if not isinstance(content, list):
            return jsonify({"error": "Expected a list of content blocks"}), 400

        pdf = BoxedPDF()
        pdf.add_page()

        for block in content:
            header = block.get("header", "")
            body = block.get("body", "")
            pdf.add_boxed_block(header, body)

        buffer = BytesIO()
        buffer.write(pdf.output(dest='S').encode('latin1'))
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="boxed-content.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
