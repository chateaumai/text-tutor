from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import weaviate
from langchain.retrievers.weaviate_hybrid_search import WeaviateHybridSearchRetriever
from langchain.vectorstores import Weaviate
from .config import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_API_ENV, WEAVIATE_URL, WEAVIATE_API_KEY

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
    #docsearch = Pinecone.from_existing_index(index_name, embeddings)
    print('start embed')
    docsearch = Pinecone.from_documents(documents, embeddings, index_name=index_name)
    return docsearch

def hybrid_search(documents):
    client = weaviate.Client(
        url=WEAVIATE_URL,
        auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY),
        additional_headers={
            "X-Openai-Api-Key": OPENAI_API_KEY,
        },
    )
    index_name = "Texttutor"

    if not client.schema.exists(index_name):
        retriever = WeaviateHybridSearchRetriever(
            client=client,
            index_name=index_name,
            text_key="text",
            attributes=[],
            create_schema_if_missing=True,
        )
        print("starting to add")
        retriever.add_documents(documents)
        print("done adding")

    else:
        print("not adding")
        retriever = WeaviateHybridSearchRetriever(
            client=client,
            index_name=index_name,
            text_key="text",
            attributes=[],
            create_schema_if_missing=False,
        )

    return retriever
    
