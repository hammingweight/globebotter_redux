from typing import Annotated

from langchain_core.prompts import ChatPromptTemplate

from .llm import chat_model
from .retriever import DocumentRetriever


system_prompt = (
    "You are a helpful assistant that helps a user to plan an optimized"
    "travel itinerary given document snippets about a travel destination."
    "If none of the snippets is relevant, mention that there are no relevant"
    "travel documents, and then answer the question to the best of your ability."
    "\n\nHere are the destination documents: "
    "{context}"
)

retriever = DocumentRetriever()
prompts = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{question}"),
    ]
)

print(chat_model)
