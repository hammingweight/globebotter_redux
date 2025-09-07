import os

from langchain_community.document_loaders import PyPDFLoader
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
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
documents = text_splitter.split_documents(documents)

for index, doc in enumerate(documents):
    print(f"Document #{index}\n{doc}\n===")

# 2. Convert to vectors:
embedder = OllamaEmbeddings(model="mistral:7b-instruct-q4_K_M")

# 3. Create and populate vector DB
db_dir = os.getenv("GB_DB", ".")
_ = Chroma.from_documents(
    documents=documents, embedding=embedder, persist_directory=db_dir
)
