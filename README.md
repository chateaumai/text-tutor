# Text Tutor
Text Tutor is an AI-powered chatbot that can answer and understand questions in the context of a given textbook.

The uploaded textbook's textual information is separated into chunks, which are then turned into vector embeddings. These embeddings map semantic meaning in the form of a multi-dimensional array.

These embeddings are then stored in Pinecone and Weaviate (vector databases). When a question is asked, the vector embeddings stored in the DB that are close in meaning with the question are returned, giving the large language model the context to aid answering.

LangChain was used for the LLM instance, as well as chunking the textbook and connecting to the vector databases.
## Semantic Search or Hybrid Search?
The specific textbook used to test was Probability & Statistics for Engineers. 

Semantic search is perfect for queries that require at most a few paragraphs to answer. 
(What is a random variable?) (How do I find 10% trimmed mean?)

But it would struggle when more comprehensive knowledge was needed.
(What are the contents of chapter 4?)
This is when hybrid search performs better than semantic search. Hybrid search is a combination of semantic search and traditional keyword search to find the correct embeddings.

This program used both semantic search as well as hybrid search. Function calling was implemented to determine which type of search to call (based on the question itself).
