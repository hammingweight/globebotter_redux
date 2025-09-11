from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import add_messages, END, START, StateGraph

from .llm import chat_model, cleanup_response
from .retriever import HYBRID_RETRIEVER


class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    messages: Annotated[list, add_messages]


def retrieve(state: State):
    retrieved_docs = HYBRID_RETRIEVER.invoke(state["messages"][-1].content)
    return {"context": retrieved_docs}


def generate(state: State):
    system_prompt = (
        "You are a helpful assistant that helps a user visiting Italy. You should "
        "answer questions about travel destinations including towns, tourist sights, "
        "regional food, hotels, etc. You will be supplied with document snippets to "
        "help you answer the question. "
        "Some of the snippets may not apply to the user's question."
        "If none of the snippets is relevant, answer the question to the best of "
        "your ability."
        "\n\nHere are the document snippets: "
        "{context}\n\n"
        # Use the advice on p.78 of "Building LLM Powered Applications":
        # Repeat instructions at the end.
        "Remember if none of the snippets is relevant, ignore the snippets "
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
    response = chat_model.invoke(messages).content
    response = cleanup_response(response)
    return {"answer": response, "messages": [AIMessage(response)]}


graph_builder = StateGraph(State)
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate", END)

memory = MemorySaver()
chatbot = graph_builder.compile(checkpointer=memory)
