from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

class DocumentRetriever(BaseRetriever):
    documents: List[Document] = []
    k: int = 5

    def _get_relevant_documents(self, query, *, run_manager) -> List[Document]:
        return []