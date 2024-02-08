import os

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from streamlit.runtime.state.session_state_proxy import SessionStateProxy


def get_llm() -> ChatOpenAI:
    llm = ChatOpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"), temperature=0)
    return llm


def get_chat_memory() -> ConversationBufferMemory:
    memory = ConversationBufferMemory(return_messages=True, memory_key="chat_history")
    return memory


def get_retrieval_chain(session_state: SessionStateProxy, llm: ChatOpenAI, memory: ConversationBufferMemory) -> ConversationalRetrievalChain:
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        # Retriever args will depend on the general purpose of the app.
        retriever=session_state["vector_db"].as_retriever(
            search_kargs={"fecth_k": 20, "k": 10}, search_type="mmr"
        ),
        chain_type="refine",
    )
    return qa_chain


def rag_func(session_state: SessionStateProxy, user_prompt: str | None) -> str:
    """Create a response to the user question using retrieval augmented genetation (RAG).

    Args:
        session_state (SessionState): Provides access to the vector database, where the pdf vectors are stored.
        user_prompt (str | None): User's question.

    Returns:
        str: Assistant's response to the user prompt.
    """

    if "vector_db" not in session_state.keys():
        return "Please go to 'Home' page and upload your PDF file first."

    llm = get_llm()
    memory = get_chat_memory()
    qa_chain = get_retrieval_chain(session_state, llm, memory)
    response = qa_chain({"question": user_prompt})

    return response.get("answer")
