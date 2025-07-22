import os
from typing import Optional
from openai import AsyncAzureOpenAI, AzureOpenAI
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_ai import Agent
from dotenv import load_dotenv
load_dotenv()

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


class OpenAIAgentBase:
    """Base class for OpenAI-powered agents with shared configuration and model setup."""
    
    def __init__(self):
        """Initialize the base agent with Azure OpenAI configuration."""
        self._model: Optional[OpenAIModel] = None
        self._agent: Optional[Agent] = None
    
    def _get_azure_config(self) -> tuple[str, str, str, str]:
        """
        Get Azure OpenAI configuration from environment variables.
        
        Returns:
            Tuple of (endpoint, key, api_version, deployment)
            
        Raises:
            ValueError: If required environment variables are missing
        """
        endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
        key = os.getenv('AZURE_OPENAI_KEY')
        api_version = os.getenv('AZURE_OPENAI_API_VERSION', '2024-07-01-preview')
        deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT')
        
        missing = [k for k, v in [
            ("AZURE_OPENAI_ENDPOINT", endpoint),
            ("AZURE_OPENAI_KEY", key),
            ("AZURE_OPENAI_DEPLOYMENT", deployment),
        ] if not (v and isinstance(v, str) and v.strip())]
        
        if missing:
            raise ValueError(f"Missing Azure OpenAI config: {', '.join(missing)}. Please set these in your environment or .env file.")
        
        # All are present and non-empty strings
        return str(endpoint), str(key), str(api_version), str(deployment)
    
    def _get_azure_model(self):
        """
        Get the Azure OpenAI model instance.
        
        Returns:
            Configured OpenAIModel instance
            
        Raises:
            ValueError: If Azure configuration is invalid
        """
        if self._model is None:
            endpoint, key, api_version, deployment = self._get_azure_config()
            client = AzureOpenAI(
                azure_endpoint=endpoint,
                api_version=api_version,
                api_key=key,
            )
            self._model = OpenAIModel(
                deployment,  # This is the deployment name, not the model name!
                provider=AzureProvider(openai_client=client),
            )
        curr_messages  =[
                {
                "role": "system",
                "content": f'''You are an assistant'''
                ""
                },
                {
                "role": "user",
                "content": f'''{"Hello"}'''
                ""
                }
            ]
        client.chat.completions.create(
        messages=curr_messages,
        model = deployment
        )
        return self._model
   

agent_base = OpenAIAgentBase()
model = agent_base._get_azure_model()

 