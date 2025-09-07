import random

from behave import use_step_matcher
from langchain_community.utils.math import cosine_similarity
from langchain_ollama.embeddings import OllamaEmbeddings

from globebotter.rag import chatbot

use_step_matcher("re")

@given(u'a session with the chatbot')
def start_session(context):
    context.chatbot = chatbot
    context.session = str(random.randint(1, 1000000))


@when(u'a user asks the chatbot "(?P<query>.*)"')
def ask_chatbot(context, query):
    response = context.chatbot.invoke({"messages": query}, config = {"configurable": {"thread_id": context.session}})
    embedder = OllamaEmbeddings(model="mistral:7b-instruct-q4_K_M")
    context.response = response["messages"][-1].content
    context.response_embedding = embedder.embed_documents([context.response])

@then(u'the response should be similar to "(?P<comparison>.*)"')
def check_similar(context, comparison):
    embedder = OllamaEmbeddings(model="mistral:7b-instruct-q4_K_M")
    context.expected_embedding = embedder.embed_documents([comparison])
    context.response_similarity = cosine_similarity(context.response_embedding, context.expected_embedding)[0][0]
    print(context.response_similarity)


@then(u'the response should not be similar to')
def check_not_similar(context):
    print(dir(context.table))
