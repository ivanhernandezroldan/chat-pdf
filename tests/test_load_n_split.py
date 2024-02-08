from langchain_core.documents.base import Document

from src.utils.file_managment.load_n_split import add_metadata_to_chunks

def test_add_metadata_to_chunks():
    doc1 = Document(page_content = "content1", metadata = {})
    doc2 = Document(page_content = "content2", metadata = {})
    metadata = {"test1": "test1", "test2": "test2"}
    chunks = [doc1, doc2]
    
    assert add_metadata_to_chunks(chunks, metadata) == [
        Document(page_content='Metadata: {\'test1\': \'test1\', \'test2\': \'test2\'} content1 \n\n Metadata: {\'test1\': \'test1\', \'test2\': \'test2\'}', metadata={}),
        Document(page_content='Metadata: {\'test1\': \'test1\', \'test2\': \'test2\'} content2 \n\n Metadata: {\'test1\': \'test1\', \'test2\': \'test2\'}', metadata={})
        ]