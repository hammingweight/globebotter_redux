from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import add_messages, END, START, StateGraph

from .llm import chat_model
from .retriever import DocumentRetriever


retriever = DocumentRetriever()


class State(TypedDict):
    question: str
    is_off_topic: bool
    off_topic_reason: str
    context: List[Document]
    answer: str
    messages: Annotated[list, add_messages]


def sanity_check(state: State):
    system_prompt = (
        "You are a helpful assistant that helps a user to plan an optimized "
        "travel itinerary. Check that the user's question may be on topic for "
        "travel planning. If the question is on topic reply simply with "
        "'ON TOPIC', else respond with 'OFF TOPIC:' (in upper case) followed by "
        "the reason that the question is unrelated to travel."
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{history}"),
            ("human", "{question}"),
        ]
    )

    messages = prompt.invoke(
        {
            "question": state["messages"][-1].content,
            "history": state["messages"][:-1],
        }
    )
    response = chat_model.invoke(messages)
    print(response)
    import time
    time.sleep(60)
    return {}


def retrieve(state: State):
    retrieved_docs = retriever.invoke(state["messages"][-1].content)
    # print(retrieved_docs)
    return {"context": retrieved_docs}


def generate(state: State):
    system_prompt = (
        "You are a helpful assistant that helps a user to plan an optimized "
        "travel itinerary given document snippets."
        "Some of the snippets may not apply to the user's destination."
        "If none of the snippets is relevant, mention that there are no relevant "
        "travel documents, and then answer the question to the best of your ability."
        "\n\nHere are the document snippets: "
        "{context}\n\n"
        # Use the advice on p.78 of "Building LLM Powered Applications":
        # Repeat instructions at the end.
        "Remember if none of the context is relevant, ignore the context messages "
        "and answer to the best of your ability."
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("placeholder", "{history}"),
            ("human", "{question}"),
        ]
    )

    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke(
        {
            "question": state["messages"][-1].content,
            "history": state["messages"][:-1],
            "context": docs_content,
        }
    )
    print(messages)
    response = chat_model.invoke(messages)
    return {"answer": response.content, "messages": [AIMessage(response.content)]}


graph_builder = StateGraph(State)
graph_builder.add_node("sanity_check", sanity_check)
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "sanity_check")
graph_builder.add_edge("sanity_check", "retrieve")
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate", END)

memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
