from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
from .config import OPENAI_API_KEY

def get_prompt():
    template = '''You are a tutor with expertise in the subject matter presented in the context below.
    Your goal is to provide clear, structured, and concise answers to the user's queries. 
    Whenever explaining concepts, follow a step-by-step format. 
    Use headers to demarcate different sections of your answer. 
    Format the output in a way that is easy to understand and read.
    Incorporate examples to elucidate your points. 
    If you can't address a query based on the provided context, reply with "I don't know".

    #IF RELEVANT TO THE QUESTION AND CONTEXT, TRY TO FOLLOW THIS GUIDE TO OUTPUT WITH WELL DEFINED HEADERS AND LINEBREAKS (for ease of reading)#
    - Start by providing a brief **Definition** or overview of the topic.
    - Follow it with **Key Properties or Characteristics**, presenting each in a separate sub-header with a clear explanation.
    - If relevant, Illustrate with a practical **Example**, making sure to break down the example for easy understanding.
    - If relevant, discuss how the topic can be **Visualized** or represented.
    - Ensure the response is clear, structured, and concise.
    - Use headers and sub-headers to demarcate different sections of your answer. This is crucial.
    - Incorporate examples wherever necessary to elucidate your points.
    - If a question cannot be addressed based on the provided context, reply with "I don't know".


    {context}

    Question: {question}'''

    PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )
    return PROMPT

def run_llm(query: str, docs: object):
    #llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)
    chat = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY, verbose=True)
    PROMPT = get_prompt()
    chain = load_qa_chain(chat, chain_type="stuff", prompt=PROMPT)
    result = chain.run({"input_documents": docs, "question": query})
    return result

def answer(query: str, docsearch: Pinecone) -> str:
    docs = docsearch.similarity_search(query)
    print(f'k: {len(docs)}')
    for doc in docs:
        print(doc)
        print('_______________________')
    return run_llm(query, docs)

def answer_hybrid(query: str, retriever: WeaviateHybridSearchRetriever) -> str:
    docs = retriever.get_relevant_documents(query)
    for doc in docs:
        print(doc)
        print('_______________________')
    return run_llm(query, docs)
    

