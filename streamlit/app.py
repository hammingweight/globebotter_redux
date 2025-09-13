import streamlit as st
from langchain_core.messages import HumanMessage

from globebotter.rag import chatbot

st.set_page_config(page_title="GlobeBotter", page_icon="🌐")
st.header("🌐 Welcome to GlobeBotter!")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def process_message(message):
    response = chatbot.invoke({"messages": HumanMessage(message)})
    return response["messages"][-1].content


if user_message := st.chat_input("How can I help you?"):
    with st.chat_message("user"):
        st.markdown(user_message)
    st.session_state.chat_history.append({"role": "User", "content": user_message})
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_message(user_message)
        st.markdown(response)
    st.session_state.chat_history.append({"role": "Assistant", "content": response})
