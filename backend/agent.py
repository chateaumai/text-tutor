import openai
import json
from .query import answer, answer_hybrid
from .config import OPENAI_API_KEY
from langchain.vectorstores import Pinecone
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
#prompt
#load_qa

#Between pinecone semantic and weaviate's hybrid
functions = [
    {
        "name": "answer",
        "description": "Use this function if the question is asking something that doesn't require comprehensive knowledge\
                        , if the answer can be found out from a few paragraphs of the text max\
                        (example: what is a random variable?)\
                        (example: how can i calculate the 25% trimmed mean?)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The question the user is asking"
                },
                "docsearch": {
                    "type": "object",
                    "description": "The Pinecone docsearch object"
                }
            },
            "required": ["query", "docsearch"]
        }
    },
    {
        "name": "answer_hybrid",
        "description": "Use this function if the question being asked requires more comprehensive knowledge to answer\
                        (example: summarize chapter 4.1)\
                        (example: how does the character harry evolve over the course of the book?)",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The question the user is asking"
                },
                "retriever": {
                    "type": "object",
                    "description": "The Weaviate retriever object"
                }
            },
            "required": ["query", "retriever"]
        }
    }
]

#choosing which one
def decide_retriever(question: str, pinecone_retriever: Pinecone, weaviate_retriever: WeaviateHybridSearchRetriever):

    messages = [
        {"role": "system", "content": "Examine the following query and based on it, call the appropriate function.\
         You should always call the most relavent function no matter what, even if the user's query might not seem directly relevant"},
        {"role": "user", "content": question},
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
    )

    response_message = response["choices"][0]["message"]
    
    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]

        if function_name == "answer":
            print("pinecone")
            return answer(question, pinecone_retriever)
        elif function_name == "answer_hybrid":
            print("weaviate")
            return answer_hybrid(question, weaviate_retriever)
