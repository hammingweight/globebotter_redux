import random
import sys

from behave import use_step_matcher, given, when, then
from langchain_community.utils.math import cosine_similarity
from langchain_ollama.embeddings import OllamaEmbeddings

from globebotter.rag import chatbot
from globebotter.settings import LLM_MODEL

use_step_matcher("re")


@given("a session with the chatbot")
def start_session(context):
    context.chatbot = chatbot
    context.session = str(random.randint(1, 1000000))


@when('a user asks the chatbot(?P<query>.*)')
def ask_chatbot(context, query):
    query = query.strip(" '\"")
    if query == "":
        query = context.text.strip(" '\"")

    assert query != "", "No question asked"
    print(f"Query: {query}\n\n")
    response = context.chatbot.invoke(
        {"messages": query}, config={"configurable": {"thread_id": context.session}}
    )
    context.response = response["messages"][-1].content
    embedder = OllamaEmbeddings(model=LLM_MODEL)
    context.response_embedding = embedder.embed_documents([context.response])


@then('the response should be similar to "(?P<expected>.*)"')
def check_similar(context, expected):
    embedder = OllamaEmbeddings(model=LLM_MODEL)
    context.expected_embedding = embedder.embed_documents([expected])
    context.response_similarity = cosine_similarity(
        context.response_embedding, context.expected_embedding
    )[0][0]
    print(f"Expected: {expected}, got: {context.response}")
    print(f"Good similarity = {context.response_similarity}")


@then("the response should not be similar to")
def check_not_similar(context):
    embedder = OllamaEmbeddings(model=LLM_MODEL)
    for row in context.table:
        c = row["Bad Response"]
        c_embedding = embedder.embed_documents([c])
        c_similarity = cosine_similarity(context.response_embedding, c_embedding)[0][0]
        print(f"Bad comparison: {c}, similarity = {c_similarity}")
        assert (
            c_similarity < context.response_similarity
        ), f"'{context.response} is similar to {c}'. Similarity = {c_similarity}"
