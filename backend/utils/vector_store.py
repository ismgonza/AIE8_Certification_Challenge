"""
Vector store operations using Qdrant.
"""
import logging
from typing import List, Optional
from pathlib import Path

from langchain.schema import Document
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from utils import settings

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


class VectorStore:
    """
    Handles all Qdrant vector store operations.
    """
    
    def __init__(self):
        """Initialize Qdrant client and embeddings."""
        logger.info("Initializing Vector Store...")
        
        # Initialize embeddings
        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Initialize Qdrant client based on mode
        if settings.QDRANT_MODE == "memory":
            logger.info("Using in-memory Qdrant")
            self.client = QdrantClient(":memory:")
        else:
            logger.info(f"Connecting to Qdrant at {settings.QDRANT_HOST}:{settings.QDRANT_PORT}")
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )
        
        self.collection_name = settings.QDRANT_COLLECTION
        
        # Initialize vector store
        self.vector_store = None
        
        logger.info("✅ Vector Store initialized")
    
    
    def create_collection(self):
        """Create Qdrant collection if it doesn't exist."""
        try:
            # Check if collection exists
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]
            
            if self.collection_name in collection_names:
                logger.info(f"Collection '{self.collection_name}' already exists")
                return
            
            # Get embedding dimension (OpenAI text-embedding-3-small = 1536 dimensions)
            embedding_dim = len(self.embeddings.embed_query("test"))
            
            # Create collection
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=embedding_dim,
                    distance=Distance.COSINE
                )
            )
            
            logger.info(f"✅ Created collection '{self.collection_name}' with dimension {embedding_dim}")
        
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise
    
    
    def add_documents(self, documents: List[Document]) -> None:
        """
        Add documents to vector store.
        
        Args:
            documents: List of Document objects to add
        """
        if not documents:
            logger.warning("No documents to add")
            return
        
        try:
            logger.info(f"Adding {len(documents)} documents to vector store...")
            
            # Create collection if needed
            self.create_collection()
            
            # Initialize vector store with existing collection
            self.vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=self.collection_name,
                embedding=self.embeddings
            )
            
            # Add documents
            self.vector_store.add_documents(documents)
            
            logger.info(f"✅ Added {len(documents)} documents to '{self.collection_name}'")
        
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise
    
    
    def search(self, query: str, top_k: int = 3) -> List[Document]:
        """
        Search for similar documents using vector similarity.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of similar Document objects
        """
        try:
            if not self.vector_store:
                # Initialize vector store
                self.vector_store = QdrantVectorStore(
                    client=self.client,
                    collection_name=self.collection_name,
                    embedding=self.embeddings
                )
            
            logger.info(f"🔍 Vector search for: '{query}' (top_k={top_k})")
            
            # Vector similarity search using OpenAI embeddings
            results = self.vector_store.similarity_search(query, k=top_k)
            
            logger.info(f"Found {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"Error searching: {e}")
            raise
    
    
    def search_with_score(self, query: str, top_k: int = 3) -> List[tuple]:
        """
        Search with relevance scores.
        
        Args:
            query: Search query
            top_k: Number of results to return
            
        Returns:
            List of (Document, score) tuples
        """
        try:
            if not self.vector_store:
                self.vector_store = QdrantVectorStore(
                    client=self.client,
                    collection_name=self.collection_name,
                    embedding=self.embeddings
                )
            
            logger.info(f"Searching with scores for: '{query}' (top_k={top_k})")
            
            # Search with scores
            results = self.vector_store.similarity_search_with_score(query, k=top_k)
            
            logger.info(f"Found {len(results)} results")
            return results
        
        except Exception as e:
            logger.error(f"Error searching with scores: {e}")
            raise
    
    
    def as_retriever(self, **kwargs):
        """
        Return the underlying vector store as a retriever.
        Allows our VectorStore to be used with LangChain's retriever interface.
        
        Args:
            **kwargs: Arguments to pass to as_retriever (e.g., search_kwargs={"k": 5})
            
        Returns:
            LangChain retriever instance
        """
        if not self.vector_store:
            # Initialize vector store
            self.vector_store = QdrantVectorStore(
                client=self.client,
                collection_name=self.collection_name,
                embedding=self.embeddings
            )
        
        return self.vector_store.as_retriever(**kwargs)
    
    
    def delete_collection(self) -> None:
        """Delete the entire collection."""
        try:
            self.client.delete_collection(self.collection_name)
            self.vector_store = None
            logger.info(f"✅ Deleted collection '{self.collection_name}'")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise
    
    
    def get_collection_info(self) -> dict:
        """Get information about the collection."""
        try:
            info = self.client.get_collection(self.collection_name)
            return {
                "name": self.collection_name,
                "vectors_count": info.vectors_count,
                "points_count": info.points_count,
                "status": info.status
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {e}")
            return {}


# ============================================================================
# Convenience functions
# ============================================================================

def get_vector_store() -> VectorStore:
    """Get a VectorStore instance (singleton pattern)."""
    return VectorStore()


# ============================================================================
# Example usage
# ============================================================================

if __name__ == "__main__":
    from utils.document_processor import process_pdfs
    
    # Initialize vector store
    vs = VectorStore()
    
    # Process and add documents
    print("\n📄 Processing PDFs...")
    chunks = process_pdfs()
    
    print(f"\n💾 Adding {len(chunks)} chunks to vector store...")
    vs.add_documents(chunks)
    
    # Get collection info
    print("\n📊 Collection Info:")
    info = vs.get_collection_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Test search
    print("\n🔍 Testing search...")
    query = "What are the CIS Controls?"
    results = vs.search(query, top_k=3)
    
    print(f"\nQuery: {query}")
    print(f"Found {len(results)} results:\n")
    for i, doc in enumerate(results, 1):
        print(f"{i}. {doc.page_content[:200]}...")
        print(f"   Source: {doc.metadata.get('source', 'N/A')}")
        print()