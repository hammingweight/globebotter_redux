from typing import Annotated, List, Literal
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import add_messages, END, START, StateGraph

from .llm import cleanup_response, get_llm
from .retriever import HYBRID_RETRIEVER


class State(TypedDict):
    llm_temperature: float
    question: str
    is_question_relevant: bool
    context: List[Document]
    answer: str
    messages: Annotated[list, add_messages]


# A step that rejects questions that are unrelated to Italy travel.
def check_relevancy(state: State):
    system_prompt = (
        "You are an assistant that checks that a user is asking for help about Italy."
        " You should check that questions are about travel destinations including "
        "towns, tourist sights, regional food, hotels, etc. "
        "If a question is about Italy, simply reply 'RELEVANT' without any further detail."
        "If a question is not about Italy, reply 'IRRELEVANT:' followed by your reasoning "
        "and a statement that you cannot assist with the question."
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
    llm = get_llm(state.get("llm_temperature", 0.3))
    response = llm.invoke(messages).content
    response = cleanup_response(response)
    if "IRRELEVANT:" in response:
        reason_index = response.index("IRRELEVANT:") + len("IRRELEVANT:")
        reason = response[reason_index:].strip()
        return {"is_question_relevant": False, "messages": [AIMessage(reason)]}
    return {"is_question_relevant": True}


# If the question is irrelevant, just go to the final state.
def is_relevant_condition(state: State) -> Literal["retrieve", END]:
    if state["is_question_relevant"]:
        return "retrieve"
    return END


# Get relevant document steps
def retrieve(state: State):
    retrieved_docs = HYBRID_RETRIEVER.invoke(state["messages"][-1].content)
    return {"context": retrieved_docs}


# Generate a reply based on the "RAG" document snippets.
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
    llm = get_llm(state.get("llm_temperature", 0.3))
    response = llm.invoke(messages).content
    response = cleanup_response(response)
    return {"answer": response, "messages": [AIMessage(response)]}


graph_builder = StateGraph(State)
graph_builder.add_node("check_relevancy", check_relevancy)
graph_builder.add_node("retrieve", retrieve)
graph_builder.add_node("generate", generate)

graph_builder.add_edge(START, "check_relevancy")
graph_builder.add_conditional_edges("check_relevancy", is_relevant_condition)
graph_builder.add_edge("retrieve", "generate")
graph_builder.add_edge("generate", END)

memory = MemorySaver()
chatbot = graph_builder.compile(checkpointer=memory)
