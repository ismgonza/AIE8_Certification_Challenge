"""
Simple RAG pipeline for question answering.
"""
from typing import List, Dict, Optional
import logging

from langchain_openai import ChatOpenAI
from langchain.schema import Document

from utils import settings
from utils.vector_store import VectorStore
from utils.tools import search_tavily
from utils.prompts import IMPLEMENTATION_CONSULTANT_PROMPT

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Simple RAG: Retrieve context, generate answer.
    """
    
    def __init__(
        self,
        vector_store: VectorStore = None,
        model: str = None,
        temperature: float = 0.0,
        top_k: int = 3,
        use_tavily: bool = True,
        use_agents: bool = True
    ):
        """
        Initialize RAG pipeline.
        
        Args:
            vector_store: VectorStore instance (creates new if None)
            model: LLM model name (defaults to settings.LLM_MODEL)
            temperature: LLM temperature (0 = deterministic)
            top_k: Number of chunks to retrieve
            use_tavily: Enable Tavily search for real-world examples
            use_agents: Use multi-agent LangGraph workflow (recommended)
        """
        self.vector_store = vector_store or VectorStore()
        self.top_k = top_k
        self.use_tavily = use_tavily and settings.TAVILY_API_KEY
        self.use_agents = use_agents
        
        if self.use_tavily:
            logger.info("✅ Tavily search enabled")
        
        if self.use_agents:
            logger.info("✅ Multi-agent mode enabled")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model or settings.LLM_MODEL,
            temperature=temperature,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Set prompt template
        self.prompt = IMPLEMENTATION_CONSULTANT_PROMPT
        
        logger.info(f"✅ RAG Pipeline initialized (model={self.llm.model_name}, top_k={self.top_k})")
    
    
    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents.
        
        Args:
            query: Search query
            
        Returns:
            List of relevant Documents
        """
        logger.info(f"Retrieving top {self.top_k} chunks for query: '{query}'")
        results = self.vector_store.search(query, top_k=self.top_k)
        return results
    
    
    
    def generate(self, query: str, context_docs: List[Document], tavily_results: Optional[str] = None) -> str:
        """
        Generate answer from context.
        
        Args:
            query: User question
            context_docs: Retrieved documents
            tavily_results: Optional Tavily search results
            
        Returns:
            Generated answer
        """
        # Format context from ISO documents
        context = "**ISO 27001/27002 Documentation:**\n\n"
        context += "\n\n".join([doc.page_content for doc in context_docs])
        
        # Add Tavily results if available
        if tavily_results:
            context += "\n\n" + tavily_results
        
        # Generate answer
        logger.info("Generating answer...")
        messages = self.prompt.format_messages(context=context, question=query)
        response = self.llm.invoke(messages)
        
        return response.content
    
    
    def query(self, question: str, return_sources: bool = True) -> Dict:
        """
        Full RAG pipeline: retrieve + generate.
        
        Args:
            question: User question
            return_sources: Include source documents in response
            
        Returns:
            Dict with 'answer' and optionally 'sources'
        """
        logger.info(f"Processing query: '{question}'")
        
        # Use agentic workflow if enabled
        if self.use_agents:
            from utils.agents import run_agentic_rag
            return run_agentic_rag(question)
        
        # Otherwise use simple RAG (fallback)
        logger.info("Using simple RAG pipeline")
        
        # Retrieve from vector store
        docs = self.retrieve(question)
        
        # Search Tavily for additional context
        tavily_results = None
        if self.use_tavily:
            tavily_results = search_tavily(question)
        
        # Generate answer
        answer = self.generate(question, docs, tavily_results)
        
        result = {"answer": answer}
        
        if return_sources:
            result["sources"] = [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata
                }
                for doc in docs
            ]
        
        logger.info("✅ Query completed")
        return result


# ============================================================================
# Convenience function
# ============================================================================

def get_rag_pipeline(**kwargs) -> RAGPipeline:
    """Get a RAG pipeline instance with custom settings."""
    return RAGPipeline(**kwargs)


# ============================================================================
# Example usage
# ============================================================================

if __name__ == "__main__":
    # Initialize
    rag = RAGPipeline(top_k=3)
    
    # Query
    result = rag.query("What is ISO 27001?")
    
    print(f"\n{'='*60}")
    print(f"Question: What is ISO 27001?")
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nSources: {len(result['sources'])} chunks")
    print(f"{'='*60}\n")

