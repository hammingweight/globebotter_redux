import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_experimental.text_splitter import SemanticChunker

from globebotter.settings import LLM_MODEL


if not os.path.exists("italy_guide.pdf"):
    raise Exception(
        "The file 'italy_guide.pdf' cannot be found in the current directory"
    )

loader = PyPDFLoader("./italy_guide.pdf")
documents = loader.load()
embedder = OllamaEmbeddings(model=LLM_MODEL)
text_splitter = SemanticChunker(embeddings=embedder, add_start_index=True)
documents = text_splitter.split_documents(documents)

cleaned_docs = []
for index, doc in enumerate(documents):
    cleaned_doc = doc.page_content.replace("Coliseum", "Colosseum")
    cleaned_doc = cleaned_doc.replace("Cappuchin", "Capuchin")
    cleaned_doc = Document(cleaned_doc)
    cleaned_docs.append(cleaned_doc)
    print(f"Document #{index}\n{cleaned_doc}\n===")

db_dir = os.getenv("GB_DB", ".")
_ = Chroma.from_documents(
    documents=cleaned_docs, embedding=embedder, persist_directory=db_dir
)
