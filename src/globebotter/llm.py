from langchain_ollama import ChatOllama

from .settings import LLM_MODEL


chat_model = ChatOllama(model=LLM_MODEL, temperature=0.1)


def cleanup_response(response: str):
    response = response.strip()
    if response.startswith("<think>"):
        response_index = response.index("</think>") + len("</think>")
        response = response[response_index:].strip()
    return response
