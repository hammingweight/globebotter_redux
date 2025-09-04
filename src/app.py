import uuid

from langchain_core.messages import HumanMessage
import streamlit as st

from globebotter.rag import graph

st.set_page_config(page_title="GlobeBotter", page_icon="🌐")
st.header("🌐 Welcome to GlobeBotter!")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for message in st.session_state.chat_history:
    print(f"message: {message}")
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())


def process_message(message, user_id):
    config = {"configurable": {"thread_id": user_id}}
    response = graph.invoke({"messages": HumanMessage(message)}, config=config)
    return response["messages"][-1].content


if user_message := st.chat_input("How can I help you?"):
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state.chat_history.append({"role": "User", "content": user_message})
    response = process_message(user_message, st.session_state["user_id"])
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.chat_history.append({"role": "Assistant", "content": response})
