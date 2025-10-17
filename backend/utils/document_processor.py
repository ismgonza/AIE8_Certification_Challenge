"""
Document processing utilities for loading PDFs and chunking text.
"""
from pathlib import Path
from typing import List
import logging

from langchain_community.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

from utils import settings

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def load_pdfs(directory_path: str | Path = None) -> List[Document]:
    """
    Load all PDFs from a directory.
    
    Args:
        directory_path: Path to directory with PDFs (defaults to settings.DATA_PATH)
        
    Returns:
        List of Document objects (one per page)
    """
    directory_path = Path(directory_path) if directory_path else settings.DATA_PATH
    
    if not directory_path.exists():
        raise FileNotFoundError(f"Directory not found: {directory_path}")
    
    logger.info(f"Loading PDFs from: {directory_path}")
    
    # Load all PDFs
    loader = DirectoryLoader(
        str(directory_path),
        glob="*.pdf",
        loader_cls=PyMuPDFLoader,
        show_progress=True
    )
    
    docs = loader.load()
    
    # Count PDFs
    pdf_count = len(set(doc.metadata.get("source", "") for doc in docs))
    logger.info(f"✅ Loaded {len(docs)} pages from {pdf_count} PDF files")
    
    return docs


def chunk_documents(documents: List[Document]) -> List[Document]:
    """
    Split documents into chunks.
    
    Args:
        documents: List of Document objects
        
    Returns:
        List of chunked Documents
    """
    logger.info(f"Chunking {len(documents)} documents...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(documents)
    
    # Add chunk IDs
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
    
    logger.info(f"✅ Created {len(chunks)} chunks")
    return chunks


def process_pdfs(directory_path: str | Path = None) -> List[Document]:
    """
    Load PDFs and chunk them. That's it!
    
    Args:
        directory_path: Path to directory with PDFs
        
    Returns:
        List of chunked Documents ready for embedding
    """
    # Load
    docs = load_pdfs(directory_path)
    
    # Chunk
    chunks = chunk_documents(docs)
    
    return chunks


def process_uploaded_files(files: list, temp_dir: Path) -> List[Document]:
    """
    Process uploaded PDF files.
    
    Args:
        files: List of file contents (bytes) with filenames
        temp_dir: Temporary directory to save files
        
    Returns:
        List of chunked Documents ready for embedding
    """
    logger.info(f"Processing {len(files)} uploaded files...")
    
    # Save files to temp directory
    for filename, content in files:
        file_path = temp_dir / filename
        with open(file_path, "wb") as f:
            f.write(content)
        logger.info(f"Saved {filename} to temp directory")
    
    # Process PDFs from temp directory
    chunks = process_pdfs(temp_dir)
    
    return chunks


# ============================================================================
# Example usage
# ============================================================================

if __name__ == "__main__":
    # Process PDFs
    chunks = process_pdfs()
    
    # Show stats
    print(f"\n{'='*60}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Example chunk:\n{chunks[0].page_content[:200]}...")
    print(f"{'='*60}\n")