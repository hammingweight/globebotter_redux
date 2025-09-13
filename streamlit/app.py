import uuid

# Hack 1 to suppress a warning (we don't actually need this import)
# import torch

import streamlit as st
from langchain_core.messages import HumanMessage

from globebotter.rag import chatbot

# Hack 2 to stop streamlit from emitting a meaningless warning.
# torch.classes.__path__ = []

st.set_page_config(page_title="GlobeBotter", page_icon="🌐")
st.header("🌐 Welcome to GlobeBotter!")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())


def process_message(message, user_id):
    config = {"configurable": {"thread_id": user_id}}
    response = chatbot.invoke({"messages": HumanMessage(message)}, config=config)
    return response["messages"][-1].content


if user_message := st.chat_input("How can I help you?"):
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state.chat_history.append({"role": "User", "content": user_message})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_message(user_message, st.session_state["user_id"])
        st.markdown(response)
    st.session_state.chat_history.append({"role": "Assistant", "content": response})
