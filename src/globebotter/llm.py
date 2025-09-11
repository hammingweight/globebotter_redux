from langchain_ollama import ChatOllama

from .settings import LLM_MODEL


chat_model = ChatOllama(model=LLM_MODEL, num_thread=4, temperature=0.1)
