# Text Tutor
Text Tutor is an AI-powered chatbot that can answer and understand questions in the context of a given textbook.
<img width="1440" alt="Screen Shot 2023-09-22 at 3 09 47 AM" src="https://github.com/chateaumai/text-tutor/assets/136946607/39d1fd39-d9ac-4a1b-a75e-69d07d63fe67">

The uploaded textbook's textual information is separated into chunks, which are then turned into vector embeddings. These embeddings map semantic meaning in the form of a multi-dimensional array.

These embeddings are then stored in Pinecone and Weaviate (vector databases). When a question is asked, the vector embeddings stored in the DB that are close in meaning with the question are returned, giving the large language model the context to aid answering.

<img width="1440" alt="Screen Shot 2023-09-22 at 4 45 48 AM" src="https://github.com/chateaumai/text-tutor/assets/136946607/22c360c8-d9b3-4835-aff0-24b812ae29b6">

In this example you can see that the llm understood what rv was in the context of statistics due to the textbook content. If you were to ask chatgpt the same question it would think you are talking about the rv car.

LangChain was used for the LLM instance, as well as chunking the textbook and connecting to the vector databases.

## Semantic Search or Hybrid Search?
The specific textbook used to test was Probability & Statistics for Engineers. 

Semantic search is perfect for queries that require at most a few paragraphs to answer. 
(What is a random variable?) (How do I find 10% trimmed mean?)

But it would struggle when more comprehensive knowledge was needed.
(What are the contents of chapter 4?)
This is when hybrid search performs better than semantic search. Hybrid search is a combination of semantic search and traditional keyword search to find the correct embeddings.

This program used both semantic search as well as hybrid search. Function calling was implemented to determine which type of search to call (based on the question itself).
