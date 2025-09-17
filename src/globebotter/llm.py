from langchain_ollama import ChatOllama

# Qwen3, 4 billion parameters, 4-bit quantization
LLM_MODEL = "qwen3:4b-q4_K_M"

_chat_models = {}


def get_llm(temperature, model=None):
    if model is None:
        model = LLM_MODEL
    if _chat_models.get((temperature, model)) is None:
        _chat_models[(temperature, model)] = ChatOllama(
            model=model, temperature=temperature
        )
    return _chat_models[(temperature, model)]


def cleanup_response(response: str):
    response = response.strip()
    if response.startswith("<think>"):
        response_index = response.index("</think>") + len("</think>")
        response = response[response_index:].strip()
    return response
