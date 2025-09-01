from langchain_ollama import ChatOllama

chat_model = ChatOllama(model="mistral:7b-instruct-q4_K_M", num_thread=4)