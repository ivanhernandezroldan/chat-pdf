import streamlit as st

from src.utils.user_interface.chat_page_ui import basic_ui, chat_ui
from src.utils.chat_functionality.chat_state import chatting


def main() -> None:
    """Allow user to chat with the uploaded PDF file."""
    session_state = st.session_state

    basic_ui()
    chat_ui(session_state)

    chatting(session_state)


if __name__ == "__main__":
    main()
