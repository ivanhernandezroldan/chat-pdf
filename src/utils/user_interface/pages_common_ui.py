import streamlit as st


def common_ui() -> None:
    """Sets the page title and icon."""
    version = "1.0"
    app_name = "ChatPDF"

    st.set_page_config(
        page_title=f"{app_name} {version}",
        page_icon="./assets/logo_the_cliff.png",
        layout="centered",
    )
