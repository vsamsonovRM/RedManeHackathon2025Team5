from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import ElasticsearchStore
from langchain.embeddings import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
import os
import openai
from dotenv import load_dotenv
import warnings

load_dotenv()
llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
api_key = os.getenv("OPENAI_API_KEY")
es_password = os.getenv("ES_PASSWORD")
es_fingerprint = os.getenv("ES_FINGERPRINT")
es_http = os.getenv("ES_HTTP")

openai.api_key = os.getenv("OPEN_AI_API_KEY")

class mCase_GPT:
    def __init__(self):
        self.chain = create_chain()

    def query(self, query):
        result = self.chain({"query": query})
        output = result['result']
        print(f"\n{output}\n")
        return result['result'], result


def create_chain():
    warnings.filterwarnings("ignore")
    llm = OpenAI(openai_api_key=api_key)
    embeddings = OpenAIEmbeddings(openai_api_key=api_key)
    openai.api_key = api_key
    
def query(self, query):
        result = self.llm(query)
        print(result)
    
    

gpt = mCase_GPT()
gpt.query("hello")
# import openai
# from openai import AzureOpenAI

# # Set your Azure OpenAI credentials
# openai.api_type = "azure"
# openai.api_base = "https://victo-m9k0iyi6-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4.1-nano"
# openai.api_version = "2025-04-14"
# openai.api_key = "6e4d8096797d4ef6a19a834f92e97103"

# # Your deployment name
# deployment_name = "gpt-4.1-mini"

# client = AzureOpenAI(
#     api_key="6e4d8096797d4ef6a19a834f92e97103",
#     api_version="2025-04-14",
#     azure_endpoint="https://rm-shared-open-ai.openai.azure.com",
# )

# # Call the model
# response = client.chat.completions.create(
#     model="gpt-4.1-mini",  # This is the *deployment name* in Azure
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "What is the capital of France?"}
#     ],
# )
# # Print the response
# print("response")
# print(response['choices'][0]['message']['content'])
