from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
import openai
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from openai import AzureOpenAI
import re

load_dotenv()

openai_model = "gpt-4.1"
es_password = os.getenv("ES_PASSWORD")
endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
key = os.getenv('AZURE_OPENAI_KEY')
api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-07-01-preview')
deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')

EXAMPLE = '''
{
  "recordName": "P1332642429: Jane Doe [2 ACTIVE PSA]",
  "Person ID": "p1332642429",
  "Person Status": "draft",
  "First Name": "jane",
  "Last Name": "doe",
  "Legal Name": "jane  doe",
  "Background Check Requester": "person",
  "Datalist Type": "person",
  "Active PSA Alerts Count": "[2 active psa]",
  "County": "alcorn",
  "Sex at Birth": "female",
  "Gender Identity": "female",
  "Date of Birth Available?": "yes",
  "Date of Birth": "2020-11-01",
  "Known / Unknown Person": "known",
  "Alias / Other Names": "jane doe"
}
 
'''

INPUT_PDF_EXAMPLE = """{
            "Last Name": "Doe",
            "First Name": "John",
            "Date of Birth": "01/01/1990",
            "Gender Identity": "Male",
            "Title": "Lorem ipsum dolor sit amet.",
            "Title 2": "Lorem ipsum again.",
            "Image": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
            "Form Title": "Screening Form",
            "Description": "Optional subtitle or description"
            }"""
            
OUTPUT_PDF_EXAMPLE = """
  "headerFields": [
    { "label": "Last Name", "value": "Doe" },
    { "label": "First Name", "value": "John" },
    { "label": "Date of Birth", "value": "01/01/1990" },
    { "label": "Gender Identity", "value": "Male" }
  ],
  "content": [
    { "header": "Title", "body": "Lorem ipsum dolor sit amet." },
    { "header": "Title 2", "body": "Lorem ipsum again." }
  ],
  "defaultHeader": {
    "image": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
    "title": "Screening Form",
    "description": "Optional subtitle or description"
  }
}
"""

PROMPT_PDF_OUTPUT_STRUCTURE = """
{
  "headerFields": [
    { "label": ..., "value": ... },
    ...
  ],
  "content": [
    { "header": ..., "body": ... },
    ...
  ],
  "defaultHeader": {
    "image": "https://www.google.com/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png",
    "title": "Screening Form",
    "description": "Optional subtitle or description"
  }
}"""

def generate_proposer_messages(prompt):
    messages =  [
                {
                "role": "system",
                "content": f'''You are a JSON generator. Improve your JSON based on feedback. Only output raw JSON with brackets <OUTPUT> ... <OUTPUT>'''
                ""
                },
                {
                "role": "user",
                "content": f'''{prompt}'''
                ""
                }
            ]
    return messages

def generate_proposer_messages(prompt):
    messages =  [
                {
                "role": "system",
                "content": f'''You are a JSON validator. Review the JSON and respond with feedback. If it's valid, say: 'Valid JSON.'''
                ""
                },
                {
                "role": "user",
                "content": f'''{prompt}'''
                ""
                }
            ]
    return messages


def generate_pdf_helper(content):
        messages = [
                    {
                        "role": "system",
                        "content": f'''
                You are an intelligent formatter that transforms flattened form data into a structured JSON object following a predefined schema.

                **Objective**: Convert the flat key-value input into a structured JSON object that matches the following schema:

                {PROMPT_PDF_OUTPUT_STRUCTURE}

                ---
                🔁 **Behavior**:
                - Group personal information into `headerFields` as `{{ "label": ..., "value": ... }}` pairs.
                - Group other textual fields into `content` as `{{ "header": ..., "body": ... }}` pairs.
                - Map branding or metadata elements to `defaultHeader`, specifically: `image`, `title`, and `description`.
                ---

                📘 **Example Transformation**:
                Only present your output using <OUTPUT> <OUTPUT> brackets, go straight to the point.

                **User Input**:
                <INPUT> {INPUT_PDF_EXAMPLE} <INPUT>

                **Expected Output (MUST BE JSON)**:
                <OUTPUT> {OUTPUT_PDF_EXAMPLE} <OUTPUT>
                '''
                    },
                    {
                        "role": "user",
                        "content": f"<INPUT> {content} <INPUT>"
                    }
                ]

        return messages


def generate_user_payload(prompt):
    messages =  [
                {
                "role": "system",
                "content": f'''You are an assistant'''
                ""
                },
                {
                "role": "user",
                "content": f'''{prompt}'''
                ""
                }
            ]
    return messages


class LLMInfrastructure:
    def __init__(self):
        self.client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_version=api_version,
                api_key=key
            )

    def respond(self):
        messages = []
        messages.append({"role": "system", "content": "you are a chatbot"})
        messages.append({"role": "user", "content": "introduce yourself"})

    
    def get_response(self, prompt):
        curr_messages = generate_user_payload(prompt)
        client_output = self.client.chat.completions.create(
        model=openai_model,
        messages=curr_messages
    )
        output = client_output.choices[0].message.content
        return output


    def generate_pdf_structure(self, content):
        curr_messages = generate_pdf_helper(content)
        client_output = self.client.chat.completions.create(
        model=openai_model,
        messages=curr_messages
    )
        output = client_output.choices[0].message.content
        match = re.search(r"<OUTPUT>\s*(\{.*?\})\s*<OUTPUT>", output, re.DOTALL)
        if match:
            return match.group(1).strip()
        return output
    
    # def json_validation(self, content):
    #     proposer_messages = generate_proposer_messages(content)
    #     curr_json = None
    #     for i in range(3):
    #         print(f"Attempt: {i+1}")
    #         curr_json = self.client.chat.completions.create(
    #             model=openai_model,
    #             messages=curr_messages
    #         )

    #     curr_messages = generate_user_payload(prompt)
    #     client_output = self.client.chat.completions.create(
    #     model=openai_model,
    #     messages=curr_messages
    # )
    #     output = client_output.choices[0].message.content
    #     print(output)
    #     return output
        
        
llm_infrastructure = LLMInfrastructure()
print(llm_infrastructure.generate_pdf_structure(EXAMPLE))