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


openai_model = "gpt4o"
es_password = os.getenv("ES_PASSWORD")

endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
key = os.getenv('AZURE_OPENAI_KEY')
api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-07-01-preview')
deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')