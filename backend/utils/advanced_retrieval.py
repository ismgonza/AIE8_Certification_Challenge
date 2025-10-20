"""
Advanced retrieval methods for ensemble.

Provides:
1. BM25 retriever (keyword-based)
2. Cohere rerank retriever (precision filtering)
3. Ensemble retriever (combines multiple strategies)
"""
from typing import Optional
import logging

from langchain.retrievers import BM25Retriever, EnsembleRetriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

from utils import settings

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# ============================================================================
# BM25 Retriever (Keyword-based)
# ============================================================================

# Cache BM25 retriever since document processing is expensive
_bm25_retriever_cache = None

def get_bm25_retriever(top_k: int = 10) -> BM25Retriever:
    """
    Create BM25 (keyword-based) retriever.
    
    Why: Security docs have exact terms (CIS Control X.X, AWS IAM, etc.)
         BM25 ensures these exact matches are found.
    
    Args:
        top_k: Number of documents to retrieve
    
    Returns:
        BM25Retriever instance
    """
    global _bm25_retriever_cache
    
    if _bm25_retriever_cache is None:
        logger.info("🔨 Building BM25 index from documents...")
        from utils.document_processor import process_pdfs
        
        chunks = process_pdfs()
        _bm25_retriever_cache = BM25Retriever.from_documents(chunks, k=top_k)
        logger.info(f"✅ BM25 retriever ready with {len(chunks)} documents")
    else:
        # Update k if different
        _bm25_retriever_cache.k = top_k
    
    return _bm25_retriever_cache


# ============================================================================
# Cohere Rerank Retriever (Precision)
# ============================================================================

def get_cohere_rerank_retriever(
    base_retriever,
    top_k: int = 10,
    model: str = "rerank-v3.5"
) -> ContextualCompressionRetriever:
    """
    Create Cohere rerank retriever.
    
    Why: Improves precision by reranking base retriever results.
         Uses cross-encoder for better relevance scoring.
    
    Args:
        base_retriever: Base retriever to rerank from
        top_k: Number of documents to return after reranking
        model: Cohere rerank model
    
    Returns:
        ContextualCompressionRetriever with Cohere reranker
    """
    if not settings.COHERE_API_KEY:
        logger.warning("No Cohere API key found, skipping reranking")
        return base_retriever
    
    try:
        logger.info(f"🔄 Creating Cohere reranker with model: {model}")
        
        compressor = CohereRerank(
            model=model,
            top_n=top_k,
            cohere_api_key=settings.COHERE_API_KEY
        )
        
        return ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
    
    except Exception as e:
        logger.error(f"Failed to create Cohere reranker: {e}")
        return base_retriever


# ============================================================================
# Ensemble Retriever (Combines Multiple Strategies)
# ============================================================================

def get_ensemble_retriever(
    vector_store,
    top_k: int = 3,
    use_cohere: bool = True,
    retriever_k_multiplier: int = 3
) -> EnsembleRetriever:
    """
    Create ensemble retriever combining multiple strategies.
    
    Strategy:
    - Vector search (semantic understanding)
    - BM25 (keyword matching for exact terms)
    - Cohere rerank (precision improvement on vector results)
    
    Uses reciprocal rank fusion to combine results.
    
    Args:
        vector_store: VectorStore instance
        top_k: Final number of documents to return
        use_cohere: Whether to include Cohere reranker
        retriever_k_multiplier: Multiplier for initial retrieval (default 3x)
    
    Returns:
        EnsembleRetriever instance
    """
    logger.info(f"🏗️  Building ensemble retriever (final top_k={top_k})")
    
    # Calculate initial retrieval amount (get more candidates for fusion)
    initial_k = top_k * retriever_k_multiplier
    
    # 1. Vector retriever (semantic understanding)
    logger.info(f"  📊 Vector retriever: retrieving {initial_k} candidates")
    vector_retriever = vector_store.as_retriever(search_kwargs={"k": initial_k})
    
    # 2. BM25 retriever (keyword matching)
    logger.info(f"  🔤 BM25 retriever: retrieving {initial_k} candidates")
    bm25_retriever = get_bm25_retriever(top_k=initial_k)
    
    # Start with these two
    retrievers = [vector_retriever, bm25_retriever]
    weights = [0.5, 0.5]  # Equal weight by default
    
    # 3. Cohere rerank retriever (optional, for precision)
    if use_cohere and settings.COHERE_API_KEY:
        # Rerank from initial_k down to a smaller number for precision
        cohere_top_k = max(top_k, int(initial_k * 0.5))  # At least top_k, max 50% of initial
        logger.info(f"  ✨ Cohere reranker: reranking {initial_k} → {cohere_top_k}")
        cohere_retriever = get_cohere_rerank_retriever(
            base_retriever=vector_retriever,
            top_k=cohere_top_k,  # Return fewer docs after reranking
            model="rerank-v3.5"
        )
        retrievers.append(cohere_retriever)
        weights = [0.4, 0.3, 0.3]  # Vector slightly higher, rest equal
        logger.info("  🎯 Using 3-way ensemble: Vector (40%) + BM25 (30%) + Cohere (30%)")
    else:
        logger.info("  🎯 Using 2-way ensemble: Vector (50%) + BM25 (50%)")
    
    # Create ensemble with reciprocal rank fusion
    ensemble = EnsembleRetriever(
        retrievers=retrievers,
        weights=weights,
        c=60  # Rank fusion constant (balance between high/low ranked items)
    )
    
    logger.info(f"✅ Ensemble retriever ready (will return {top_k} final documents)")
    
    return ensemble


# ============================================================================
# Helper function for standalone reranking (backwards compatibility)
# ============================================================================

def rerank_documents(
    query: str, 
    documents: list, 
    top_k: int = 5,
    model: str = "cohere"
) -> list:
    """
    Legacy rerank function for backwards compatibility.
    
    Note: Ensemble retriever is now the recommended approach.
    This function is kept for any existing code that uses it.
    """
    logger.warning("rerank_documents() is deprecated. Use get_ensemble_retriever() instead.")
    
    if not documents:
        return documents
    
    if len(documents) <= top_k:
        logger.info(f"⚡ Skipping reranking ({len(documents)} docs <= top_k={top_k})")
        return documents
    
    try:
        logger.info(f"🔄 Reranking {len(documents)} documents with Cohere")
        
        import cohere
        
        api_key = settings.COHERE_API_KEY or settings.OPENAI_API_KEY
        if not api_key:
            logger.warning("No Cohere API key found, skipping reranking")
            return documents[:top_k]
        
        co = cohere.Client(api_key)
        
        # Prepare documents
        docs_text = [doc.page_content for doc in documents]
        
        # Rerank
        results = co.rerank(
            query=query,
            documents=docs_text,
            top_n=top_k,
            model="rerank-english-v3.0"
        )
        
        # Get reranked documents
        reranked_docs = []
        for result in results.results:
            original_doc = documents[result.index]
            reranked_docs.append(original_doc)
        
        logger.info(f"✅ Reranked to top {len(reranked_docs)} documents (Cohere)")
        return reranked_docs
    
    except ImportError:
        logger.error("Cohere not installed. Install: pip install cohere")
        return documents[:top_k]
    except Exception as e:
        logger.error(f"Cohere reranking failed: {e}")
        return documents[:top_k]
