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
from utils.prompts import SECURITY_ADVISOR_PROMPT

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
        use_agents: bool = True,
        use_reranking: bool = False,
        reranker_model: str = "cohere",
        use_ensemble: bool = False
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
            use_reranking: Enable Cohere reranking [Task 6] (deprecated, use ensemble)
            reranker_model: Reranker model (default: "cohere")
            use_ensemble: Enable ensemble retrieval (Vector + BM25 + Cohere) [Task 6]
        """
        self.vector_store = vector_store or VectorStore()
        self.top_k = top_k
        self.use_tavily = use_tavily and bool(settings.TAVILY_API_KEY)
        self.use_agents = use_agents
        
        # Advanced retrieval flags (Task 6)
        self.use_reranking = use_reranking
        self.reranker_model = reranker_model
        self.use_ensemble = use_ensemble
        self.ensemble_retriever = None
        
        # Log enabled features
        if self.use_tavily:
            logger.info("✅ Tavily search enabled")
        
        if self.use_agents:
            logger.info("✅ Multi-agent mode enabled")
        
        # Log advanced retrieval features
        if self.use_ensemble:
            logger.info("🚀 Advanced Retrieval: Ensemble (Vector + BM25 + Cohere)")
            from utils.advanced_retrieval import get_ensemble_retriever
            self.ensemble_retriever = get_ensemble_retriever(
                self.vector_store,
                top_k=self.top_k,
                use_cohere=bool(settings.COHERE_API_KEY)
            )
        elif self.use_reranking:
            logger.info(f"🚀 Advanced Retrieval: Reranking ({self.reranker_model}) [Legacy]")
        
        # Initialize LLM
        self.llm = ChatOpenAI(
            model=model or settings.LLM_MODEL,
            temperature=temperature,
            openai_api_key=settings.OPENAI_API_KEY
        )
        
        # Set prompt template
        self.prompt = SECURITY_ADVISOR_PROMPT
        
        logger.info(f"✅ RAG Pipeline initialized (model={self.llm.model_name}, top_k={self.top_k})")
    
    
    def retrieve(self, query: str) -> List[Document]:
        """
        Retrieve relevant documents with optional advanced techniques.
        
        Args:
            query: Search query
            
        Returns:
            List of relevant Documents
        """
        logger.info(f"Retrieving top {self.top_k} chunks for query: '{query}'")
        
        # Use ensemble retrieval if enabled (Vector + BM25 + Cohere)
        if self.use_ensemble and self.ensemble_retriever:
            logger.info("Using ensemble retrieval (Vector + BM25 + Cohere)")
            results = self.ensemble_retriever.get_relevant_documents(query)
            # Ensemble returns all results, trim to top_k
            results = results[:self.top_k]
            logger.info(f"✅ Retrieved {len(results)} documents via ensemble")
            return results
        
        # Fallback: Legacy reranking or simple vector search
        # Get more docs if we're going to rerank (better recall)
        initial_top_k = self.top_k * 3 if self.use_reranking else self.top_k
        
        results = self.vector_store.search(query, top_k=initial_top_k)
        
        # Step 2: Reranking (if enabled - legacy approach)
        if self.use_reranking and len(results) > self.top_k:
            from utils.advanced_retrieval import rerank_documents
            results = rerank_documents(
                query, 
                results, 
                top_k=self.top_k,
                model=self.reranker_model
            )
        
        logger.info(f"✅ Retrieved {len(results)} final documents")
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
        # Format context from security documentation
        context = "**Security Documentation (CIS, NIST, OWASP, CSA):**\n\n"
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
            return run_agentic_rag(
                question,
                use_reranking=self.use_reranking,
                reranker_model=self.reranker_model,
                use_ensemble=self.use_ensemble
            )
        
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
    result = rag.query("What are the CIS Controls?")
    
    print(f"\n{'='*60}")
    print(f"Question: What are the CIS Controls?")
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\nSources: {len(result['sources'])} chunks")
    print(f"{'='*60}\n")

