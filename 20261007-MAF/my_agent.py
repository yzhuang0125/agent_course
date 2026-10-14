import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
import my_agent_def
from agent_framework import InMemoryHistoryProvider

# Microsoft Foundry - Azure OpenAI
from agent_framework.openai import OpenAIChatClient
agent = OpenAIChatClient(
    base_url=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
).as_agent(
    instructions=my_agent_def.instructions, 
    name=my_agent_def.name,
    context_providers = [InMemoryHistoryProvider("memory", load_messages=True)],
)