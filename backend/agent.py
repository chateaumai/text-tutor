from langchain import OpenAI
from langchain.agents import AgentType, initialize_agent, Tool
from .config import OPENAI_API_KEY

llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo-0613")

tools = [
    Tool(
        name = "pinecone vector search",
    )


]

agent = initialize_agent()