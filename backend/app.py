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


class CustomPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=False)
        self.set_margins(10, 10, 10)

    def draw_default_header(self, image_path=None, title="Default Title", description="Optional subtitle or description"):
        # Constants
        img_width = 20  # mm (~300px @127 DPI)
        img_height = 20
        margin = 10
        spacing = 4
        right_margin = self.r_margin
        page_width = self.w

        # Y position start
        y_start = self.get_y()

        # Image on the left
        if image_path:
            self.image(image_path, x=margin, y=y_start, w=img_width, h=img_height)

        # Text block dimensions
        text_block_x_end = page_width - right_margin
        text_block_width = page_width - img_width - 3 * margin

        # Position for text aligned to right
        x_text_start = text_block_x_end - text_block_width

        # Title
        self.set_xy(x_text_start, y_start)
        self.set_font("Arial", 'B', 16)
        self.multi_cell(text_block_width, 10, title, align='R')

        # Description (smaller, under title)
        self.set_font("Arial", '', 12)
        self.set_x(x_text_start)
        self.multi_cell(text_block_width, 6, description, align='R')

        # Move below the image or text, whichever is taller
        self.set_y(max(y_start + img_height, self.get_y()) + spacing)
    def draw_header_fields(self, fields):
        self.set_font("Arial", size=10)
        self.set_line_width(0.5)

        # Calculate box width based on number of fields
        margin = 10
        box_width = (self.w - 2 * margin) / len(fields)
        box_height = 20
        y_start = self.get_y()
        x_start = margin

        for field in fields:
            label = field.get("label", "")
            value = field.get("value", "")
            
            self.set_xy(x_start, y_start)
            self.rect(x_start, y_start, box_width, box_height)
            self.set_xy(x_start + 2, y_start + 2)
            self.set_font("Arial", 'B', 9)
            self.cell(box_width - 4, 5, label)
            self.set_xy(x_start + 2, y_start + 10)
            self.set_font("Arial", '', 10)
            self.cell(box_width - 4, 5, value)

            x_start += box_width

        # Move Y below header row
        self.set_y(y_start + box_height + 5)

    def add_boxed_content(self, header, body):
        padding = 3
        max_width = self.w - self.l_margin - self.r_margin
        x_start = self.l_margin
        y_start = self.get_y()

        # Estimate height
        self.set_font("Arial", 'B', 14)
        header_height = self.font_size + 4

        self.set_font("Arial", '', 12)
        body_lines = self.multi_cell(max_width - 2 * padding, 8, body, split_only=True)
        body_height = len(body_lines) * 8

        total_height = header_height + body_height + 3 * padding

        # Auto page break
        if y_start + total_height > self.page_break_trigger:
            self.add_page()
            y_start = self.get_y()

        # Draw box
        self.set_line_width(0.5)
        self.rect(x_start, y_start, max_width, total_height)

        # Header
        self.set_xy(x_start + padding, y_start + padding)
        self.set_font("Arial", 'B', 14)
        self.cell(max_width - 2 * padding, 10, txt=header, ln=True)

        # Body
        self.set_font("Arial", '', 12)
        self.multi_cell(max_width - 2 * padding, 8, txt=body)

        # Move to next box start (overlap border)
        self.set_y(y_start + total_height)

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()

        header_fields = data.get("headerFields", [])
        content_sections = data.get("content", [])
        default_header = data.get("defaultHeader", {})

        pdf = CustomPDF()
        pdf.add_page()

        if default_header:
            pdf.draw_default_header(default_header.get("image", ""), default_header.get("title", ""), default_header.get("description", ""))

        if header_fields:
            pdf.draw_header_fields(header_fields)

        for section in content_sections:
            pdf.add_boxed_content(section.get("header", ""), section.get("body", ""))

        buffer = BytesIO()
        buffer.write(pdf.output(dest='S').encode('latin1'))
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="generated-form.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
