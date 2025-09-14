from langchain_ollama import ChatOllama

LLM_MODEL = "qwen3:4b-q4_K_M"

_chat_models = {}


def get_llm(temperature):
    if _chat_models.get(temperature) is None:
        _chat_models[temperature] = ChatOllama(model=LLM_MODEL, temperature=temperature)
    return _chat_models[temperature]


def cleanup_response(response: str):
    response = response.strip()
    if response.startswith("<think>"):
        response_index = response.index("</think>") + len("</think>")
        response = response[response_index:].strip()
    return response
