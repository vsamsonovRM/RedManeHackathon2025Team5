from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from infrastructure.llm_infrastructure import LLMInfrastructure
from fpdf import FPDF
from io import BytesIO
import pdf_config as cfg
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
    user_message = data.get('chat')
    knowledge_base = data.get('knowledgeBase')  # This is your sampleData.json

    # Convert knowledge base to a string or summary for the prompt
    kb_context = summarize_knowledge_base(knowledge_base)  # You need to implement this

    # Combine context and user message
    prompt = f"Knowledge base: {kb_context}\nUser: {user_message}"

    response = LLM_INFRASTRUCTURE.get_response(prompt)
    return jsonify({"response": response}), 200


class CustomPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=False)
        self.set_margins(cfg.DEFAULT_MARGIN, cfg.DEFAULT_MARGIN, cfg.DEFAULT_MARGIN)

    def set_body_font(self):
        self.set_font(cfg.FONT_FAMILY, '', cfg.FONT_SIZE_DESCRIPTION)

    def draw_default_header(self, image_path=None, title="Default Title", description="Optional subtitle or description"):
        margin = cfg.DEFAULT_MARGIN
        y_start = self.get_y()

        # Image
        if image_path:
            self.image(image_path, x=margin, y=y_start, w=cfg.IMAGE_WIDTH_MM, h=cfg.IMAGE_HEIGHT_MM)

        # Text Block
        x_text_end = self.w - margin
        text_block_width = self.w - cfg.IMAGE_WIDTH_MM - 3 * margin
        x_text_start = x_text_end - text_block_width

        self.set_xy(x_text_start, y_start)
        self.set_font(cfg.FONT_FAMILY, 'B', cfg.FONT_SIZE_TITLE)
        self.multi_cell(text_block_width, 10, title, align='R')

        self.set_font(cfg.FONT_FAMILY, '', cfg.FONT_SIZE_DESCRIPTION)
        self.set_x(x_text_start)
        self.multi_cell(text_block_width, 6, description, align='R')

        self.set_y(max(y_start + cfg.IMAGE_HEIGHT_MM, self.get_y()) + cfg.LINE_SPACING)

    def draw_header_fields(self, fields):
        self.set_font(cfg.FONT_FAMILY, size=cfg.FONT_SIZE_LABEL)
        self.set_line_width(cfg.HEADER_LINE_WIDTH)

        box_width = (self.w - 2 * cfg.DEFAULT_MARGIN) / len(fields)
        box_height = 20
        y_start = self.get_y()
        x_start = cfg.DEFAULT_MARGIN

        for field in fields:
            label = field.get("label", "")
            value = field.get("value", "")

            self.set_xy(x_start, y_start)
            self.rect(x_start, y_start, box_width, box_height)
            self.set_xy(x_start + 2, y_start + 2)

            self.set_font(cfg.FONT_FAMILY, 'B', cfg.FONT_SIZE_LABEL)
            self.cell(box_width - 4, 5, label)

            self.set_xy(x_start + 2, y_start + 10)
            self.set_font(cfg.FONT_FAMILY, '', cfg.FONT_SIZE_FIELD)
            self.cell(box_width - 4, 5, value)

            x_start += box_width

        self.set_y(y_start + box_height + cfg.LINE_SPACING)

    def add_boxed_content(self, header, body):
        padding = 3
        max_width = self.w - self.l_margin - self.r_margin
        x_start = self.l_margin
        y_start = self.get_y()

        self.set_font(cfg.FONT_FAMILY, 'B', 14)
        header_height = self.font_size + 4

        self.set_font(cfg.FONT_FAMILY, '', cfg.FONT_SIZE_DESCRIPTION)
        body_lines = self.multi_cell(max_width - 2 * padding, 8, body, split_only=True)
        body_height = len(body_lines) * 8

        total_height = header_height + body_height + 3 * padding

        if y_start + total_height > self.page_break_trigger:
            self.add_page()
            y_start = self.get_y()

        self.set_line_width(cfg.HEADER_LINE_WIDTH)
        self.rect(x_start, y_start, max_width, total_height)

        self.set_xy(x_start + padding, y_start + padding)
        self.set_font(cfg.FONT_FAMILY, 'B', 14)
        self.cell(max_width - 2 * padding, 10, txt=header, ln=True)

        self.set_font(cfg.FONT_FAMILY, '', cfg.FONT_SIZE_DESCRIPTION)
        self.multi_cell(max_width - 2 * padding, 8, txt=body)

        self.set_y(y_start + total_height - cfg.HEADER_LINE_WIDTH)



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

def summarize_knowledge_base(knowledge_base):
    """
    Summarize the knowledge base JSON into a readable string for the LLM prompt.
    This example summarizes roles and permissions for each entry.
    """
    if not knowledge_base:
        return "No knowledge base provided."
    summary_lines = []
    for entry in knowledge_base:
        name = entry.get("Name", [{}])[0].get("Value", "Unknown")
        summary_lines.append(f"Entity: {name}")
        roles = entry.get("ListRoles", [])
        for role in roles:
            role_name = role.get("RoleName", "Unknown Role")
            perms = []
            for perm in ["CanEdit", "CanAdd", "CanDelete", "CanBulkEdit", "CanMove", "CanMerge", "IsListAdmin"]:
                if role.get(perm):
                    perms.append(perm)
            perms_str = ", ".join(perms) if perms else "No special permissions"
            summary_lines.append(f"  - {role_name}: {perms_str}")
    return "\n".join(summary_lines)

if __name__ == '__main__':
    app.run(debug=True)
