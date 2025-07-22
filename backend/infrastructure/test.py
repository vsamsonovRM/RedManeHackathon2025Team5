import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.azure import AzureProvider
from openai import AsyncAzureOpenAI, AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Setup Azure OpenAI Client and Model
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-05-01-preview"
)

model = OpenAIModel(
    provider=AzureProvider(openai_client=client),
    model_name="gpt-4",  # or your deployed Azure model name
)

# === Agents ===
proposer_agent = Agent(model=model, instructions="You are a JSON generator. Improve your JSON based on feedback. Only output raw JSON.")
validator_agent = Agent(model=model, instructions="You are a JSON validator. Review the JSON and respond with feedback. If it's valid, say: 'Valid JSON.'")

def json_refinement_loop():
    schema_description = """
Create a JSON object representing a user with the following fields:
- name: string
- age: integer
- interests: list of strings
Return only the JSON object.
"""
    current_json = proposer_agent.run(schema_description)
    print("Initial Proposal:\n", current_json)

    MAX_TURNS = 5
    for turn in range(MAX_TURNS):
        print(f"\n--- Turn {turn + 1} ---")
        feedback = validator_agent.run(current_json)
        
        print("Validator Feedback:\n", feedback)

        if "valid" in feedback.lower():
            print("\n✅ Final JSON Accepted:\n", current_json)
            return current_json

        current_json = proposer_agent(feedback)

    print("\n⚠️ Max turns reached. Final JSON may still need review.")
    return current_json

if __name__ == "__main__":
    json_refinement_loop()