from langchain.llms import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
#api_key = os.getenv('OPENAI_API_KEY')

#llm = OpenAI(openai_api_key = 'OPENAI_API_KEY', temperature = 0.9)
llm = OpenAI(temperature = 0.9)
print("Ans: \n", llm.predict("What are 3 things to do in Portland Oregon"))


