import streamlit as st
from streamlit.runtime.state.session_state import SessionState
from streamlit.runtime.state.session_state_proxy import SessionStateProxy

from src.utils.chat_functionality.retrieval_augmented_generation import rag_func


def chatting(session_state: SessionStateProxy) -> None:
    """Receive user prompt and assistant's response and store them in 'session_state.messages' register.

    Args:
        session_state (SessionStateProxy): Proxy to the storage for the messages produced by the user and the assistant.
    """

    user_prompt = st.chat_input("Message ChatPDF...")
    if user_prompt:
        session_state["messages"].append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

    if session_state["messages"][-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                ai_response = rag_func(session_state, user_prompt)
                st.write(ai_response)
        new_ai_message = {"role": "assistant", "content": ai_response}
        session_state["messages"].append(new_ai_message)


def reset_chat(session_state: SessionState) -> None:
    if "messages" in session_state.keys():
        del session_state["messages"]


def start_chat(session_state: SessionState) -> None:
    # Clean previous chat messages before starting new conversation
    reset_chat(session_state)

    # Start new conversation related to the uploaded file
    st.switch_page("./src/pages/chat_page.py")
