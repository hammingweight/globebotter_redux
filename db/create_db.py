import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Load and chunk documents
if not os.path.exists("italy_guide.pdf"):
    raise Exception(
        "The file 'italy_guide.pdf' cannot be found in the current directory"
    )

loader = PyPDFLoader("./italy_guide.pdf")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
documents = text_splitter.split_documents(documents)

cleaned_docs = []
for index, doc in enumerate(documents):
    cleaned_doc = doc.page_content.replace("Coliseum", "Colosseum")
    cleaned_doc = cleaned_doc.replace("Cappuchin", "Capuchin")
    cleaned_doc = Document(cleaned_doc)
    cleaned_docs.append(cleaned_doc)
    print(f"Document #{index}\n{cleaned_doc}\n===")

# 2. Convert to vectors:
embedder = OllamaEmbeddings(model="mistral:7b-instruct-q4_K_M")

# 3. Create and populate vector DB
db_dir = os.getenv("GB_DB", ".")
_ = Chroma.from_documents(
    documents=cleaned_docs, embedding=embedder, persist_directory=db_dir
)
