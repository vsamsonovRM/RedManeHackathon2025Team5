from dotenv import load_dotenv
import os

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_url = os.getenv("OPENAI_URL")
openai_model = os.getenv("OPENAI_MODEL_NAME")
es_password = os.getenv("ES_PASSWORD")
es_fingerprint = os.getenv("ES_FINGERPRINT")
es_http = os.getenv("ES_HTTP")


class LLMInfrastructure:
    def __init__(self):
        print()