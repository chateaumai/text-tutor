from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_API_ENV

def get_query_result(texts, query):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
    index_name = "texttutor"
    docsearch = Pinecone.from_existing_index(index_name, embeddings)
    docs = docsearch.similarity_search(query)

    llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.run(input_documents=docs, question=query)
    return result
