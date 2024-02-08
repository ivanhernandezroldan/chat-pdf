import streamlit as st

from src.utils.user_interface.main_page_ui import basic_ui
from src.utils.user_interface.main_page_ui import file_uploader


def main() -> None:
    """Allow user to upload a PDF file."""
    session_state = st.session_state

    basic_ui()

    file_uploader(session_state)


if __name__ == "__main__":
    main()
