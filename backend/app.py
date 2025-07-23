from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from infrastructure.llm_infrastructure import LLMInfrastructure

from infrastructure.search_infrastructure import SearchInfrastructure

from fpdf import FPDF
from io import BytesIO
from field_config import FIELD_CONFIG
import pdf_config as cfg
import re
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


SEARCH_KB = None  # Initialize a global variable for the search knowledge base

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('chat')
    # Use SEARCH_KB as the knowledge base if available
    knowledge_base = globals().get('SEARCH_KB') or data.get('knowledgeBase')

    # Convert knowledge base to a string or summary for the prompt
    kb_context = summarize_knowledge_base(knowledge_base)  # You need to implement this

    # Combine context and user message
    prompt = f"Knowledge base: {kb_context}\nUser: {user_message}"

    response = LLM_INFRASTRUCTURE.get_response(prompt)
    return jsonify({"response": response}), 200


@app.route('/api/selected-record', methods=['POST'])
def selected_record():
    data = request.get_json()
    selected_record = data.get('selectedRecord')
    if not selected_record:
        return jsonify({'error': 'No record selected'}), 400
    
    mapped_selected = summarize_selected(selected_record)


    # set context for the LLM here: 
    # Mocked response for the selected record
    response = {
        'recordName': selected_record,
        'details': f'Details for {selected_record}',
        'mapped_selected': mapped_selected  
    }
    
    return jsonify({"response": response}), 200


@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json()
    user_input = data.get('search_term')  # Get "chat" from POST body
    data_list_id = data.get('data_list_id')
    response = SEARCH_INFRASTRUCTURE.search_record(user_input, data_list_id)
    
    
    return jsonify({"response": response}), 200


@app.route('/api/generate_pdf_content', methods=['POST'])
def generate_pdf_content():
    data = request.get_json()
    mapped_json = data  # Get "chat" from POST body
    response = LLM_INFRASTRUCTURE.generate_pdf_structure(mapped_json)
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

        max_fields_per_row = cfg.HEADER_COLUMNS
        box_height = 20
        y_current = self.get_y()
        
        # Process fields in chunks of max 5
        for row_start_idx in range(0, len(fields), max_fields_per_row):
            # Get fields for this row (max 5)
            row_fields = fields[row_start_idx:row_start_idx + max_fields_per_row]
            fields_in_row = len(row_fields)
            
            # Calculate box width based on actual fields in this row
            box_width = (self.w - 2 * cfg.DEFAULT_MARGIN) / fields_in_row
            x_start = cfg.DEFAULT_MARGIN

            for field in row_fields:
                label = field.get("label", "")
                value = field.get("value", "")

                self.set_xy(x_start, y_current)
                self.rect(x_start, y_current, box_width, box_height)
                self.set_xy(x_start + 2, y_current + 2)

                self.set_font(cfg.FONT_FAMILY, 'B', cfg.FONT_SIZE_LABEL)
                self.cell(box_width - 4, 5, label)

                self.set_xy(x_start + 2, y_current + 10)
                self.set_font(cfg.FONT_FAMILY, '', cfg.FONT_SIZE_FIELD)
                self.cell(box_width - 4, 5, value)

                x_start += box_width
            
            # Move to next row
            y_current += box_height

        # Set final Y position with line spacing
        self.set_y(y_current + cfg.LINE_SPACING)

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



@app.route('/api/generate-pdf', methods=['POST'])
def generate_pdf():
    try:
        data = request.get_json()
        print('request', request)
        print('data', data)
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

@app.route('/api/datalist', methods=['POST'])
def datalist():
    data = request.get_json()
    selected = data.get('selected')
    if not selected:
        return jsonify({'error': 'No datalist selected'}), 400
    # Mocked top_10 as list of dicts with recordName, etc.
    top_10 = [
        {'dynamicFieldMappings': '', 'recordName': 's_P1332642429: Jane Doe [2 ACTIVE PSA]', 'datalistPath': '726~', 'recordPath': '215499', 'FIELD_7143': '1332642429', 'FIELD_20642': 'p1332642429', 'FIELD_SEARCHABLE_20642': 'p1332642429', 'FIELD_18471': 'draft', 'FIELD_7146': 'jane', 'FIELD_SEARCHABLE_7146': 'jane', 'FIELD_7145': 'doe', 'FIELD_SEARCHABLE_7145': 'doe', 'FIELD_12459': 'jane  doe', 'FIELD_20581': 'person', 'FIELD_20584': 'person', 'FIELD_28371': '[2 active psa]', 'DYNAMICFIELD_20410': '288546', 'FIELD_37926': 'alcorn', 'FIELD_SEARCHABLE_37926': 'alcorn', 'FIELD_20618': 'female', 'FIELD_SEARCHABLE_20618': 'female', 'FIELD_7148': 'female', 'DYNAMICFIELD_11977': '249128', 'DYNAMICFIELD_SEARCHABLE_11977': '249128', 'DYNAMICFIELD_20274': '245281', 'FIELD_20840': 'yes', 'FIELD_7149': '2020-11-01', 'FIELD_SEARCHABLE_7149': '2020-11-01', 'FIELD_48270': 'known', 'FIELD_SEARCHABLE_48270': 'known', 'FIELD_50387': 'jane doe', 'FIELD_SEARCHABLE_50387': 'jane doe'},
        {'dynamicFieldMappings': '', 'recordName': 's_P638684781: Khloe Kane', 'datalistPath': '726~', 'recordPath': '219544', 'FIELD_7143': '638684781', 'FIELD_20642': 'p638684781', 'FIELD_SEARCHABLE_20642': 'p638684781', 'FIELD_18471': 'active', 'FIELD_7146': 'khloe', 'FIELD_SEARCHABLE_7146': 'khloe', 'FIELD_7145': 'kane', 'FIELD_SEARCHABLE_7145': 'kane', 'FIELD_12459': 'khloe  kane', 'FIELD_20840': 'yes', 'FIELD_7149': '1989-01-10', 'FIELD_SEARCHABLE_7149': '1989-01-10', 'FIELD_20618': 'female', 'FIELD_SEARCHABLE_20618': 'female', 'FIELD_7148': 'female', 'DYNAMICFIELD_11977': '249128', 'DYNAMICFIELD_SEARCHABLE_11977': '249128', 'DYNAMICFIELD_20274': '245281', 'FIELD_37734': '2024-01-01', 'FIELD_20581': 'person', 'FIELD_20584': 'person', 'FIELD_37926': 'hinds', 'FIELD_SEARCHABLE_37926': 'hinds', 'FIELD_40134': '260048', 'DYNAMICFIELD_37733': '193076', 'FIELD_40135': '260048', 'FIELD_44855': 'person', 'FIELD_48270': 'known', 'FIELD_SEARCHABLE_48270': 'known'},
        {'dynamicFieldMappings': '', 'recordName': 's_P-1154697195: Janel Synan', 'datalistPath': '726~', 'recordPath': '237826', 'FIELD_7143': '1154697195', 'FIELD_20642': 'p1154697195', 'FIELD_SEARCHABLE_20642': 'p1154697195', 'FIELD_18471': 'active', 'FIELD_7146': 'janel', 'FIELD_SEARCHABLE_7146': 'janel', 'FIELD_7147': '2404111251102', 'FIELD_SEARCHABLE_7147': '2404111251102', 'FIELD_7145': 'synan', 'FIELD_SEARCHABLE_7145': 'synan', 'FIELD_12459': 'janel 2404111251102 synan', 'FIELD_20840': 'yes', 'FIELD_7149': '1985-01-01', 'FIELD_SEARCHABLE_7149': '1985-01-01', 'FIELD_36822': 'yes', 'FIELD_37906': '2023-10-31', 'FIELD_20618': 'female', 'FIELD_SEARCHABLE_20618': 'female', 'FIELD_7148': 'female', 'DYNAMICFIELD_11977': '194867', 'DYNAMICFIELD_SEARCHABLE_11977': '194867', 'DYNAMICFIELD_20274': '245281', 'FIELD_28331': '336610470', 'FIELD_SEARCHABLE_28331': '336610470', 'FIELD_37734': '2023-10-31', 'FIELD_40135': '237905', 'FIELD_20584': 'person', 'FIELD_20581': 'person', 'FIELD_40134': '237905', 'FIELD_37926': 'hinds', 'FIELD_SEARCHABLE_37926': 'hinds', 'FIELD_40307': 'janel.synan@fakeemail.com', 'DYNAMICFIELD_37733': '193076', 'FIELD_48270': 'known', 'FIELD_SEARCHABLE_48270': 'known'}
    ]

    #we may call map_elastic_search_date_by_field_id(top_10[0]) here

    return jsonify({
        'response': f'You selected datalist: {selected}. Here are some records for the selected datalist.',
        'top10': top_10
    }), 200

def map_elastic_search_data_by_field_id(input_object):
    """
    Takes an object with FIELD_[number] keys and replaces them with the corresponding 
    labels from the field configuration, ignoring keys with "FIELD_SEARCHABLE" or "DYNAMICFIELD".

    Args:
        input_object (dict): Dictionary containing keys like 'FIELD_7143', 'FIELD_20642', etc.

    Returns:
        dict: New dictionary with field keys replaced by their corresponding labels
    """

    # Create a mapping dictionary from field ID to label
    field_id_to_label = {}
    for field in FIELD_CONFIG:
        field_id_to_label[field['FieldID']] = field['Label']

    # Create a new dictionary to store the mapped results
    mapped_object = {}

    # Pattern to match FIELD_[number] keys
    field_pattern = re.compile(r'^FIELD_(\d+)$')

    for key, value in input_object.items():
        # Skip keys with "FIELD_SEARCHABLE" or "DYNAMICFIELD"
        if "FIELD_SEARCHABLE" in key or "DYNAMICFIELD" in key:
            continue

        # Check if the key matches the FIELD_[number] pattern
        match = field_pattern.match(key)
        
        if match:
            # Extract the field ID number
            field_id = int(match.group(1))
            
            # Look up the corresponding label
            if field_id in field_id_to_label:
                # Use the label as the new key
                new_key = field_id_to_label[field_id]
                mapped_object[new_key] = value
            else:
                # If field ID not found in config, keep original key
                mapped_object[key] = value
        else:
            # If key doesn't match pattern, keep it as is
            mapped_object[key] = value

    SEARCH_KB = summarize_knowledge_base(mapped_object)
    globals()['SEARCH_KB'] = SEARCH_KB

    return mapped_object 

def summarize_selected(selected):
    mapped_selected = map_elastic_search_data_by_field_id(selected)
    #todo this will call victor's LLM prompt passing in selected
    return mapped_selected 

def summarize_knowledge_base(knowledge_base):
    """
    Summarize the knowledge base JSON into a readable string for the LLM prompt.
    This version returns a pretty-printed JSON string for maximum fidelity.
    """
    import json
    if not knowledge_base:
        return "No knowledge base provided."
    return json.dumps(knowledge_base, indent=2)





if __name__ == '__main__':
    app.run(debug=True)
