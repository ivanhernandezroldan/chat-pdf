import streamlit as st
from streamlit.runtime.state.session_state_proxy import SessionStateProxy
from st_pages import Page, show_pages

from src.utils.user_interface.pages_common_ui import common_ui


def basic_ui() -> None:
    common_ui()

    st.title("Chat with your PDF files")
    show_pages(
        [
            Page("./main.py", "Home (New chat)", "🏠"),
            Page("./src/pages/chat_page.py", "Chat", ":books:"),
        ]
    )


def chat_ui(session_state: SessionStateProxy) -> None:
    # Set initial message
    if "messages" not in session_state.keys():
        session_state["messages"] = [
            {"role": "assistant", "content": "Hello! How can I help you?"},
        ]

    # Display conversation (user and assistant) messages as they are being stored in 'session_state["messages"]' register.
    if "messages" in session_state.keys():
        for message in session_state["messages"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])
