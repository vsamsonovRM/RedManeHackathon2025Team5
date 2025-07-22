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

# sAzureEndpoint: https://rm-shared-open-ai.openai.azure.com Model: GPT-4.1-mini Deployment: gpt-4.1-mini Version: 2025-04-14 Key: 6e4d8096797d4ef6a19a834f92e97103
api_key = os.getenv("AZURE_INFERENCE_CREDENTIAL")

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_api_key = "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"

openai_model = "gpt-4.1-nano"
es_password = os.getenv("ES_PASSWORD")
es_fingerprint = os.getenv("ES_FINGERPRINT")
es_http = os.getenv("ES_HTTP")

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


openai.api_key = openai_api_key
class LLMInfrastructure:
    def __init__(self):
        self.client = openai # See if we will use it

        
    def respond(self):
        messages = []
        messages.append({"role": "system", "content": "you are a chatbot"})
        messages.append({"role": "user", "content": "introduce yourself"})

    
    def get_response(self, prompt):
        curr_messages = generate_user_payload(prompt)
        client_output = openai.chat.completions.create(
        model=openai_model,
        messages=curr_messages
    )
        print(f"COmpleted \n\n\n\n")
        output = client_output.choices[0].message.content
        print(output)
        return output
        
        
llm_infrastructure = LLMInfrastructure()
llm_infrastructure.get_response("What is your name")