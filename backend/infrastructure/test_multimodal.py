from dotenv import load_dotenv
import os
from langchain.embeddings import OpenAIEmbeddings
import openai
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from openai import AzureOpenAI
import base64

load_dotenv()


openai_model = "gpt-4o-2"
es_password = os.getenv("ES_PASSWORD")

endpoint = "https://rm-shared-open-ai.openai.azure.com"
key = "6e4d8096797d4ef6a19a834f92e97103"
api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-07-01-preview')
deployment = "6e4d8096797d4ef6a19a834f92e97103"

client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_version=api_version,
                api_key=key
            )


image_path = "./redmanebackground.jpg"
with open(image_path, "rb") as img_file:
    base64_image = base64.b64encode(img_file.read()).decode("utf-8")
    
image_path2 = "./pdf_pic.png"
with open(image_path2, "rb") as img_file:
    base64_image2 = base64.b64encode(img_file.read()).decode("utf-8")
    
messages = []
messages.append({"role": "system", "content": "you are a chatbot"})
messages.append({"role": "user", "content": [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image2}"
                }
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            },
             {"type": "text", "text": "Use the following images to generate a new one while keeping readability and the structured content of the original"},
             
        ] })


response = client.chat.completions.create(
        model=openai_model,
        messages=messages
    )

from PIL import Image
from io import BytesIO
import base64

def save_base64_image(base64_str, output_path):
    image_data = base64.b64decode(base64_str)
    with open(output_path, "wb") as f:
        f.write(image_data)

# # Example usage
# base64_str = "your_base64_encoded_image_here"
# save_base64_image(base64_str, "./output.jpg")
image_url = response
print(image_url)