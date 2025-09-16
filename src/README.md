# The Source Code
There are three Python files:

[rag.py](./globebotter/rag.py): This is the main entry point. The code constructs a `LangGraph` graph that:
 * Checks that a user's question is related to Italy
 * Retrieves document snippets related from the vector database that are related to the question
 * Generates a reply based on the document snippets and the LLM's parametric knowledge.

 [llm.py](./globebotter/llm.py): This provides a method to get an LLM at a specified temperature. For BDD testing,
 a low temperature is advisable.

 [retriever.py](./globebotter/retriever.py): This code creates a hybrid retriever using similarity and keyword (BM25)
 search to fetch relevant code snippets from the Chroma database.