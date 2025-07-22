from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
import openai
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("AZURE_INFERENCE_CREDENTIAL")

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_url = os.getenv("OPENAI_URL")
openai_model = os.getenv("OPENAI_MODEL_NAME")
es_password = os.getenv("ES_PASSWORD")
es_fingerprint = os.getenv("ES_FINGERPRINT")
es_http = os.getenv("ES_HTTP")


def generate_user_payload(prompt):
    
    payload = {
            "messages": [
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
            ],
            "temperature": 0,
            "top_p": 1,
            "frequency_penalty": 0
    }
    return payload

class LLMInfrastructure:
    def __init__(self):
        self.client  = ChatCompletionsClient(
            endpoint=openai_url,
            credential=AzureKeyCredential(api_key)
        )

    def respond(self):
        messages = []
        messages.append({"role": "system", "content": "you are a chatbot"})
        messages.append({"role": "user", "content": "introduce yourself"})

    
    def get_response(self, prompt):
        curr_payload = generate_user_payload(prompt)
        client_output = self.client.complete(curr_payload)
        output = client_output.choices[0].message.content
        print(output)
        return output
        
        
llm_infrastructure = LLMInfrastructure()
llm_infrastructure.get_response("What is your name")