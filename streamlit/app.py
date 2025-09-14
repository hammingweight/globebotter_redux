import uuid

# Hack 1 to suppress a warning (we don't actually need this import)
# import torch

import streamlit as st
from langchain_core.messages import HumanMessage

from globebotter.rag import chatbot

# Hack 2 to stop streamlit from emitting a meaningless warning.
# torch.classes.__path__ = []

st.set_page_config(page_title="GlobeBotter Redux", page_icon="🌐")
st.header("🌐 Welcome to GlobeBotter Redux!")
st.markdown(
    "<center><h4>An AI Chatbot for Italian Travel</h4></center>", unsafe_allow_html=True
)
message = """
__This chatbot was inspired by Valentina Alto's fun
[GlobeBotter](https://github.com/PacktPublishing/Building-LLM-Powered-Applications/blob/main/Chapter%206%20-%20Building%20conversational%20apps.ipynb)
LLM application.__

Valentina Alto's chatbot is a LangChain chatbot that incorporates RAG and tools (Google search).
In particular, questions about Italy retrieve information from an Italian tourism guide stored in
a FAISS vector database. The LLM used is an OpenAI model. *GlobeBotter* was written before the
release of LangGraph.

*GlobeBotter Redux* uses LangGraph to build a RAG chatbot. It runs on a local LLM (Qwen3-4B) and
uses ChromaDB. This application is more limited than *GlobeBotter* since it doesn't incorporate
Google search.

The main goal of *GlobeBotter Redux* is to see whether it's practical to
write BDD tests to evaluate an LLM application's ability to retrieve information from RAG sources.
"""
st.markdown(message)

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
