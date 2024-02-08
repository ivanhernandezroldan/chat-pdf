import os
import tempfile
import random

import streamlit as st
from streamlit.runtime.state.session_state import SessionState
from streamlit.runtime.uploaded_file_manager import UploadedFile
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores.chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents.base import Document
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from src.utils.chat_functionality.chat_state import start_chat


PERSIST_DIR = "./vector_db"


def add_metadata_to_chunks(chunks: list[Document], metadata: dict) -> list[Document]:
    """Add metadata to each chunk of the PDF.

    Args:
        chunks (list[Document]): List of the PDF chunks.
        metadata (dict): Metadata of the PDF.
    """
    """
    Chunk size and contents are key to maximizing RAG effectiveness.
    Something that works very well for me as a starting point is adding some metadata to each chunk (at the beggining and at the end).
    But there are other interesting aproaches that could be covered in the future like:
        - https://community.openai.com/t/the-length-of-the-embedding-contents/111471/7
        - https://community.openai.com/t/embedding-text-length-vs-accuracy/96564/5
    """
    for i in range(len(chunks)):
        chunks[i].page_content = (
            "Metadata: "
            + str(metadata) 
            + " "
            + chunks[i].page_content
            + " \n\n Metadata: "
            + str(metadata)
        )

    return chunks

def load_n_split_pdf(session_state: SessionState, files_paths: list[str], metadatas: list[dict]) -> None:
    """Load stored file as PDF, split it into chunks and vectorize them (with its metadata).

    Args:
        session_state (SessionState): Storage for the vector database to create.
        file_path (str): File's path.
        metadata (dict): Metadata of the file.
    """

    chunks = []

    for file_path, metadata in zip(files_paths, metadatas):
        # Create loader
        loader = PyPDFLoader(file_path)

        # Split document (By default with RecursiveCharacterTextSplitter) into chunks
        new_chunks = loader.load_and_split()

        # Add metadata to each chunk returned by 'load_and_split()'
        new_chunks_with_metadata = add_metadata_to_chunks(new_chunks, metadata)

        # Add all chunks of the current PDF file to the rest of chunks of the other PDF files
        chunks.extend(new_chunks_with_metadata)

    with st.spinner("Document is being vectorized...."):
        # Embeddings model (param 'openai_api_key' is automatically inferred from the first env var OPENAI_API_KEY value if not provided)
        load_dotenv(override=True)
        embeddings_model = OpenAIEmbeddings(
            openai_api_key=os.environ.get("OPENAI_API_KEY")
        )

        # Create vector database
        vector_db = Chroma.from_documents(
            collection_name="langchain" + str(random.randint(1, 10000)),
            documents=chunks,
            embedding=embeddings_model,
            persist_directory=PERSIST_DIR,
        )

        # Make persistent
        vector_db.persist()
        session_state["vector_db"] = vector_db


def store_files_in_dir(uploaded_files: list[UploadedFile]) -> list[str]:
    """Store the uploaded file in a temporary directory.

    Args:
        uploaded_file (UploadedFile): The PDF file to upload.

    Returns:
        str: The path to the temporary directory.
    """

    temp_dir = tempfile.mkdtemp()
    uploaded_files_paths = []

    for uploaded_file in uploaded_files:
        uploaded_file_path = os.path.join(temp_dir, uploaded_file.name)
        uploaded_files_paths.append(uploaded_file_path)
        with open(uploaded_file_path, "wb") as f:
            f.write(uploaded_file.getvalue())

    return uploaded_files_paths


def extract_metadatas(uploaded_files: list[UploadedFile]) -> list[dict]:
    metadatas = []
    for uploaded_file in uploaded_files:
        reader = PdfReader(uploaded_file)
        metadata = dict(reader.metadata)
        metadata["PdfNumberOfPages"] = str(len(reader.pages))
        metadatas.append(metadata)
    return metadatas


def process_file(session_state: SessionState) -> None:
    """Process the uploaded file.

    Args:
        session_state (SessionState): Container to share variables like 'vector_db' between reruns, for each user session.
    """
    metadatas = extract_metadatas(session_state["pdf_files"])
    uploaded_files_paths = store_files_in_dir(session_state["pdf_files"])
    load_n_split_pdf(session_state, uploaded_files_paths, metadatas)

    # If I call to 'start_chat()' in 'main.py', the page is changed before the file is uploaded.
    # That's why I have to call 'start_chat()' at the end of this function, waiting for the file uploader to end.
    start_chat(session_state)
