import streamlit as st

from globebotter.llm import chat_model

st.write(f"Hello, world!\n{type(chat_model)}")

