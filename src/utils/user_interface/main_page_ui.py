import streamlit as st
from streamlit.runtime.state.session_state import SessionState
from st_pages import Page, show_pages, hide_pages

from src.utils.user_interface.pages_common_ui import common_ui
from src.utils.file_managment.load_n_split import process_file


def basic_ui() -> None:
    common_ui()
    st.title("Upload your PDF files :outbox_tray:")
    show_pages(
        [
            Page("./main.py", "Home", "🏠"),
            Page("./src/pages/chat_page.py", "Chat", ":books:"),
        ]
    )
    hide_pages(["Chat"])


def file_uploader(session_state: SessionState) -> None:
    """Create a file uploader widget.

    Args:
        session_state (SessionState): container used, for each user session, to share variables between reruns
    """
    uploaded_file = st.file_uploader(
        label="Upload your file :inbox_tray:",
        type="pdf",
        key="pdf_files",
        label_visibility="hidden",
        accept_multiple_files=True,
    )
    if uploaded_file:
        process_file(session_state)
