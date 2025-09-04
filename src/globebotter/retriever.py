from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_ollama.embeddings import OllamaEmbeddings

embedder = OllamaEmbeddings(model="mistral:7b-instruct-q4_K_M")
vector_db = Chroma(persist_directory="db", embedding_function=embedder)


class DocumentRetriever(BaseRetriever):
    documents: List[Document] = []
    k: int = 5

    def _get_relevant_documents(self, query, *, run_manager) -> List[Document]:
        print(query)
        return vector_db.similarity_search(query=query, k=self.k)
