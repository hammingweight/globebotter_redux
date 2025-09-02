from typing import Annotated, List
from typing_extensions import TypedDict

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import add_messages, END, START, StateGraph

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
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("placeholder"), "{history}",
        ("human", "{question}"),
    ]
)

class State(TypedDict):
    question: str
    context: List[Document]
    answer: str
    messages: Annotated[list, add_messages]


def retrieve(state: State):
    retrieved_docs = retriever.invoke(state["messages"][-1].content)
    print(retrieved_docs)
    return {"context": retrieved_docs}

def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke(
        {"question": state["messages"][-1].content, "history": state["messages"][:-1], "context": docs_content}
    )
    response = chat_model.invoke(messages)
    return {"answer": response.content, "messages": [AIMessage(response.content)]}

graph_builder = StateGraph(State).add_sequence(
    [retrieve, generate]
)
graph_builder.add_edge(START, "retrieve")
graph_builder.add_edge("generate", END)
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

input_messages = [HumanMessage("Suggest three sites that I should visit if I spend one day in Rome.")]
response = graph.invoke({"messages": input_messages}, config=config)
print(response["answer"])
print("==================================================================\n")

input_messages = [HumanMessage("Can you suggest a fourth site?")]
response = graph.invoke({"messages": input_messages}, config=config)
print(response["answer"])
print("==================================================================\n")

input_messages = [HumanMessage("I visited that fourth suggestion before. Can you suggest something else?")]
response = graph.invoke({"messages": input_messages}, config=config)
print(response["answer"])
print("==================================================================\n")

input_messages = [HumanMessage("Why not the Taj Mahal as a fourth site?")]
response = graph.invoke({"messages": input_messages}, config=config)
print(response["answer"])
print("==================================================================\n")

input_messages = [HumanMessage("Can you suggest a restaurant for lunch?")]
response = graph.invoke({"messages": input_messages}, config=config)
print(response["answer"])



