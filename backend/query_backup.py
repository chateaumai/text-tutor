'''from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_API_ENV

def get_query_result(texts, query, user_id):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
    index_name = f"texttutor_{user_id}"

    if index_name not in pinecone.list_indexes():
        pinecone.create_index(
            name=index_name,
            metric='cosine',
            dimension=1536
        )
        docsearch = Pinecone.from_texts(texts, embeddings, index_name=index_name)
        print("created")
    else:
        docsearch = Pinecone.from_existing_index(index_name, embeddings)
        print("from existing")

    # seperate the upload and creation of index with actually querying

    #index name can be serializer? 
    #if name not in pinecone, 
    #create it, and go from text
    #else, from existing index
    docs = docsearch.similarity_search(query)
    llm = OpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY)
    chain = load_qa_chain(llm, chain_type="stuff")
    result = chain.run(input_documents=docs, question=query)
    return result'''
