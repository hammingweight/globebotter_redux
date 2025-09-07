import os
from typing import List

from langchain.retrievers import EnsembleRetriever
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_ollama.embeddings import OllamaEmbeddings

embedder = OllamaEmbeddings(model="mistral:7b-instruct-q4_K_M")
db_dir = os.getenv("VECTOR_DB_PATH", "db")
vector_db = Chroma(persist_directory=db_dir, embedding_function=embedder)

doc_strings = vector_db.get()['documents']
documents = []
for doc in doc_strings:
    documents.append(Document(doc))


class VectorDbRetriever(BaseRetriever):

    def _get_relevant_documents(self, query, *, run_manager) -> List[Document]:
        print(query)
        #return vector_db.similarity_search(query=query, k=self.k)
        return vector_db.max_marginal_relevance_search(query=query, k=5, fetch_k=20)


_VECTOR_DB_RETRIEVER = VectorDbRetriever()
_BM25_RETRIEVER = BM25Retriever.from_documents(documents)
_BM25_RETRIEVER.k = 5
HYBRID_RETRIEVER = EnsembleRetriever(retrievers=[_VECTOR_DB_RETRIEVER, _BM25_RETRIEVER])