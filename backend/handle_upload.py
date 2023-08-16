from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
from .config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_API_ENV

def get_docsearch(documents, upload_id):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
    index_name = f"texttutor-{upload_id}"

    pinecone.create_index(
        name=index_name,
        metric='cosine',
        dimension=1536
    )
    #needs list of strings
    ## docsearch = Pinecone.from_existing_index(index_name, embeddings)
    print('start embed')
    docsearch = Pinecone.from_documents(documents, embeddings, index_name=index_name)
    return docsearch

    
