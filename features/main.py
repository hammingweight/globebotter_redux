from langchain_community.utils.math import cosine_similarity
from langchain_core.messages import HumanMessage
from langchain_ollama import OllamaEmbeddings

from globebotter.rag import graph

config = {"configurable": {"thread_id": "abc123"}}

input_messages = [
    HumanMessage(
        (
            "I'm in Rome for one day. Please suggest three sights, in numbered bullet "
            "form that I should visit. Do not include any details about the sights."
        )
    )
]

comparisons = [
    "1. The Colosseum. 2 Vatican City. 3. Trevi Fountain.",
    "1. Eiffel Tower. 2. Louvre Museum. 3. Arc de Triomphe.",
    "1. Pane e Salame. 2. Tonnarello. 3. Cantina e Cucina",
    "All mimsy were the borogoves",
]
response = graph.invoke({"messages": input_messages}, config=config)
actual = response["answer"]
# actual = "foo"
print("================================================================")
print(actual)
print("================================================================")

embedder = OllamaEmbeddings(model="mistral:7b-instruct-q4_K_M")
embedding_actual = embedder.embed_documents([actual])
embedding_comparisons = embedder.embed_documents(comparisons)

for c in comparisons:
    print(c)
    embedding_c = embedder.embed_documents([c])
    print(cosine_similarity(embedding_actual, embedding_c))
# print(cosine_similarity(embedding_actual, embedding_expected))
