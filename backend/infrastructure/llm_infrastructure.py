from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
import openai
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

openai_model = "gpt-4.1-mini"
es_password = os.getenv("ES_PASSWORD")
es_fingerprint = os.getenv("ES_FINGERPRINT")
es_http = os.getenv("ES_HTTP")

endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
key = os.getenv('AZURE_OPENAI_KEY')
api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-07-01-preview')
deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')

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
        print(output)
        return output
        
        
llm_infrastructure = LLMInfrastructure()
llm_infrastructure.get_response("What is your name")