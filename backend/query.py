from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
from .config import OPENAI_API_KEY

def get_prompt():
    template = '''You are a tutor that is an expert in the field related to the context provided.
    Answer the user's question in a way what is helpful and promotes as much learning as possible.
    Be detailed in answers and give examples when appropriate. Information should explained
    step by step when needed. If a question can not be answered using the information provided
    from the documentation, answer with "I don't know"

    {context}

    Question: {question}'''

    PROMPT = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )
    return PROMPT

def answer(query: str, docsearch: Pinecone) -> str:

    docs = docsearch.similarity_search(query)
    print(f'k: {len(docs)}')
    for doc in docs:
        print(doc)
        print('_______________________')

    llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)
    PROMPT = get_prompt()
    chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT)
    result = chain.run({"input_documents": docs, "question": query})
    #result = chain.run(input_documents=docs, question=query)
    return result

def answer_hybrid(query: str, retriever: WeaviateHybridSearchRetriever) -> str:
    docs = retriever.get_relevant_documents(query)
    for doc in docs:
        print(doc)
        print('_______________________')
    
    llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)
    PROMPT = get_prompt()
    chain = load_qa_chain(llm, chain_type="stuff", prompt=PROMPT)
    result = chain.run({"input_documents": docs, "question": query})

    return result