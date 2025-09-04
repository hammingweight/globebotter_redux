from langchain_core.messages import HumanMessage

from .rag import graph

config = {"configurable": {"thread_id": "abc123"}}

input_messages = [
    HumanMessage("Suggest three sites that I should visit if I spend one day in Rome.")
]
response = graph.invoke({"messages": input_messages}, config=config)
print(response["answer"])
print("==================================================================\n")

input_messages = [HumanMessage("Can you suggest a fourth site?")]
response = graph.invoke({"messages": input_messages}, config=config)
print(response["answer"])
print("==================================================================\n")

input_messages = [
    HumanMessage(
        "I visited that fourth suggestion before. Can you suggest something else?"
    )
]
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
