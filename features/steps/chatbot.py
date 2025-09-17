import logging
import random

from behave import use_step_matcher, given, step, when, then
from langchain_community.utils.math import cosine_similarity
from langchain_ollama.embeddings import OllamaEmbeddings

from globebotter.rag import chatbot


use_step_matcher("re")


logger = logging.getLogger(__name__)

# Use a low temperature to improve answer reliability and to make the tests more deterministic.
LLM_TEMPERATURE = 0.0


# A step that allows the user to set a minimum expected cosine similarity for an answer to be
# accepted as "similar".
@step("the minimum good cosine similarity should be at least (?P<value>.*)")
def set_minimum_good_cosine_similarity(context, value):
    value = float(value)
    assert (
        value <= 1.0 and value >= -1.0
    ), "cosine similarity must be in the range [-1.0, +1.0]"
    context.minimum_good_similarity = value


@given("a session with the chatbot")
def start_session(context):
    context.chatbot = chatbot
    context.session = str(random.randint(1, 1000000))


@when("a user asks the chatbot(?P<query>.*)")
def ask_chatbot(context, query):
    query = query.strip(" '\"")
    if query == "":
        query = context.text.strip(" '\"")

    assert query != "", "No question asked"
    logger.info(f"Query: {query}\n\n")
    response = context.chatbot.invoke(
        {"messages": query, "llm_temperature": LLM_TEMPERATURE},
        config={"configurable": {"thread_id": context.session}},
    )
    context.response = response["messages"][-1].content
    embedder = OllamaEmbeddings(model=context.llm_model)
    context.response_embedding = embedder.embed_documents([context.response])


@then('the response should be similar to "(?P<expected>.*)"')
def check_similar(context, expected):
    embedder = OllamaEmbeddings(model=context.llm_model, temperature=LLM_TEMPERATURE)
    context.expected_embedding = embedder.embed_documents([expected])
    context.response_similarity = cosine_similarity(
        context.response_embedding, context.expected_embedding
    )[0][0]
    logger.info(f"Expected: {expected}, got: {context.response}")
    logger.info(f"Good similarity = {context.response_similarity}")
    assert (
        context.response_similarity >= context.minimum_good_similarity
    ), f"""
    '{context.response}'
    is not similar to
    '{expected}'.
    Cosine similarity={context.response_similarity} (< {context.minimum_good_similarity})
    """


@then("the response should not be similar to")
def check_not_similar(context):
    embedder = OllamaEmbeddings(model=context.llm_model)
    for row in context.table:
        c = row["Bad Response"]
        c_embedding = embedder.embed_documents([c])
        c_similarity = cosine_similarity(context.response_embedding, c_embedding)[0][0]
        logger.info(f"Bad comparison: {c}, similarity = {c_similarity}")
        # "Not similar" means that the similarity is less than the good similarity.
        assert (
            c_similarity < context.response_similarity
        ), f"'{context.response} is similar to {c}'. Similarity = {c_similarity}"
