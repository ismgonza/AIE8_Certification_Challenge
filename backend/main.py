"""
FastAPI backend for Security Maturity Assistant.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging

from utils import settings
from utils.document_processor import process_pdfs
from utils.vector_store import VectorStore
from utils.rag import RAGPipeline

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Security Maturity Assistant API",
    description="AI-powered security assessment and guidance for SMBs",
    version="2.0.0"
)

# Add CORS middleware (for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize singletons
vector_store = None
rag_pipeline = None


def get_vector_store() -> VectorStore:
    """Get or create vector store instance."""
    global vector_store
    if vector_store is None:
        vector_store = VectorStore()
    return vector_store


def get_rag_pipeline() -> RAGPipeline:
    """Get or create RAG pipeline instance."""
    global rag_pipeline
    if rag_pipeline is None:
        vs = get_vector_store()
        rag_pipeline = RAGPipeline(
            vector_store=vs,
            top_k=settings.TOP_K,  # Get more context for better answers
            use_tavily=True,  # Search web for implementation examples
            use_agents=True,  # Multi-agent workflow for better quality
            use_reranking=settings.USE_RERANKING,  # Cohere reranking (from .env)
            reranker_model=settings.RERANKER_MODEL  # Reranker model choice (from .env)
        )
    return rag_pipeline


# ============================================================================
# Request/Response Models
# ============================================================================

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5


class Source(BaseModel):
    content: str
    metadata: dict
    score: Optional[float] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]


class AssessmentRequest(BaseModel):
    company_name: str
    company_size: str  # "1-10", "11-50", "51-200", "201-500", "500+"
    industry: str
    tech_stack: List[str]  # ["Windows", "Microsoft 365", "Cloud", etc.]
    security_measures: Optional[str] = "None"
    budget: Optional[str] = None
    main_concern: Optional[str] = None


class SecurityGap(BaseModel):
    priority: str  # "critical", "high", "medium"
    title: str
    description: str
    risk: str
    cost: str
    time: str
    cis_control: Optional[str] = None


class AssessmentResponse(BaseModel):
    company_name: str
    maturity_score: float  # 0-10
    maturity_level: str  # "Level 1: Survival Mode", etc.
    risk_summary: str
    top_gaps: List[SecurityGap]


class DocumentItem(BaseModel):
    id: str
    content: str
    metadata: dict


class DocumentsResponse(BaseModel):
    total: int
    documents: List[DocumentItem]


class CollectionInfo(BaseModel):
    name: str
    vectors_count: Optional[int] = None
    points_count: int
    status: str


# ============================================================================
# Startup Event - Auto-ingest PDFs
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Auto-ingest PDFs from data folder on startup (only if needed)."""
    try:
        logger.info("🚀 Starting Security Maturity Assistant...")
        
        # Log LangSmith tracing status
        if settings.LANGCHAIN_API_KEY:
            logger.info("✅ LangSmith tracing enabled - view traces at https://smith.langchain.com")
        else:
            logger.info("⚠️ LangSmith tracing disabled (no API key)")
        
        vs = get_vector_store()
        
        # Check if collection exists and has documents
        try:
            collection_info = vs.get_collection_info()
            vectors_count = collection_info.get("vectors_count", 0) or collection_info.get("points_count", 0)
            
            logger.info(f"📊 Collection status: {vectors_count} documents in Qdrant")
            
            if vectors_count > 0:
                logger.info(f"✅ Vector store ready with {vectors_count:,} documents")
                logger.info("⚡ Skipping PDF ingestion (documents already loaded)")
                logger.info("✨ Security Maturity Assistant ready!")
                return  # Early exit - no need to ingest
            else:
                logger.info("📚 Collection exists but is empty")
                
        except Exception as e:
            logger.info(f"📚 Collection doesn't exist yet: {e}")
        
        # Only reach here if collection is empty or doesn't exist
        logger.info("📚 Ingesting PDFs from data folder (this will take 1-2 minutes)...")
        logger.info("💡 This only happens once - subsequent startups will be instant!")
        
        chunks = process_pdfs()
        
        if len(chunks) == 0:
            logger.warning("⚠️ No PDF chunks found! Make sure PDFs are in backend/data/ folder")
        else:
            logger.info(f"📄 Processing {len(chunks)} chunks...")
            vs.add_documents(chunks)
            logger.info(f"✅ Ingested {len(chunks):,} chunks into Qdrant")
        
        logger.info("✨ Security Maturity Assistant ready!")
        
    except Exception as e:
        logger.error(f"❌ Error during startup: {e}")
        import traceback
        logger.error(traceback.format_exc())
        logger.warning("⚠️ Server will start, but RAG may not work until documents are ingested")
        # Don't crash the server, but log the error


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Security Maturity Assistant API",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.post("/assess")
async def assess_security(request: AssessmentRequest) -> AssessmentResponse:
    """
    Assess company's security maturity and provide recommendations.
    """
    try:
        rag = get_rag_pipeline()
        
        # Build assessment query
        query = f"""Assess the security maturity of this company and provide TOP 5 CRITICAL security gaps:

Company Profile:
- Name: {request.company_name}
- Size: {request.company_size} employees
- Industry: {request.industry}
- Tech Stack: {', '.join(request.tech_stack)}
- Current Security: {request.security_measures or 'Minimal/None'}
- Budget: {request.budget or 'Limited'}
- Main Concern: {request.main_concern or 'General security'}

Based on CIS Controls IG1 (small business appropriate) and relevant benchmarks:

1. Calculate a security maturity score (0-10) based on their current state
2. Identify their maturity level (Survival, Baseline, Professional, Advanced)
3. List TOP 5 CRITICAL security gaps they should fix
4. For each gap provide:
   - Why it's critical for THEIR situation
   - Specific risk if ignored
   - Estimated cost
   - Time to implement
   - Reference CIS Control

Focus on PRACTICAL, AFFORDABLE recommendations appropriate for {request.company_size} company."""

        result = rag.query(query, return_sources=True)
        
        # Extract score and level from AI response
        import re
        answer = result["answer"]
        
        # Try to extract score (look for patterns like "8/10", "Score: 8", etc.)
        score_match = re.search(r'(?:score|maturity)[:\s]*(\d+(?:\.\d+)?)\s*/\s*10', answer, re.IGNORECASE)
        maturity_score = float(score_match.group(1)) if score_match else 3.5
        
        # Try to extract level (Survival, Baseline, Professional, Advanced)
        level_match = re.search(r'(Level \d+:|Maturity Level:)\s*([^\n]+)', answer, re.IGNORECASE)
        if level_match:
            maturity_level = level_match.group(2).strip()
        else:
            # Fallback based on score
            if maturity_score < 3:
                maturity_level = "Level 1: Survival Mode"
            elif maturity_score < 5:
                maturity_level = "Level 2: Baseline Security"
            elif maturity_score < 7:
                maturity_level = "Level 3: Professional"
            else:
                maturity_level = "Level 4: Advanced"
        
        return {
            "company_name": request.company_name,
            "maturity_score": maturity_score,
            "maturity_level": maturity_level,
            "risk_summary": answer[:500],  # First 500 chars
            "top_gaps": [
                {
                    "priority": "critical",
                    "title": "Full assessment in answer field",
                    "description": answer,
                    "risk": "See full analysis",
                    "cost": "Varies",
                    "time": "Varies",
                    "cis_control": "Multiple"
                }
            ]
        }
        
    except Exception as e:
        logger.error(f"Error in assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query_documents(request: QueryRequest) -> QueryResponse:
    """
    Query the RAG system.
    """
    try:
        rag = get_rag_pipeline()
        result = rag.query(request.query, return_sources=True)
        
        return {
            "answer": result["answer"],
            "sources": result.get("sources", [])
        }
    except Exception as e:
        logger.error(f"Error querying: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents(limit: int = 10, offset: int = 0) -> DocumentsResponse:
    """
    List documents in vector store (for debugging).
    """
    try:
        vs = get_vector_store()
        docs = vs.list_documents(limit=limit, offset=offset)
        
        return {
            "total": len(docs),
            "documents": [
                {
                    "id": doc.get("id", "unknown"),
                    "content": doc.get("content", "")[:200] + "...",
                    "metadata": doc.get("metadata", {})
                }
                for doc in docs
            ]
        }
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Detailed health check."""
    vs = get_vector_store()
    collection_info = vs.get_collection_info()
    
    vectors_count = collection_info.get("vectors_count", 0) or collection_info.get("points_count", 0)
    
    return {
        "status": "healthy",
        "version": "2.0.0",
        "vector_store": {
            "collection": collection_info.get("name", "unknown"),
            "documents": vectors_count,
            "status": collection_info.get("status", "unknown"),
            "message": "✅ Ready" if vectors_count > 0 else "⚠️ No documents loaded"
        },
        "settings": {
            "data_path": str(settings.DATA_PATH),
            "llm_model": settings.LLM_MODEL,
            "embedding_model": settings.EMBEDDING_MODEL
        }
    }


@app.post("/admin/reingest")
async def force_reingest():
    """
    Manually trigger re-ingestion of PDFs.
    Use this only if you've added new PDFs or want to refresh the database.
    """
    try:
        logger.info("🔄 Manual re-ingestion triggered")
        
        vs = get_vector_store()
        
        # Get current count
        collection_info = vs.get_collection_info()
        old_count = collection_info.get("vectors_count", 0) or collection_info.get("points_count", 0)
        
        logger.info(f"Current: {old_count} documents")
        logger.info("📚 Processing PDFs...")
        
        chunks = process_pdfs()
        
        if len(chunks) == 0:
            return {"error": "No PDF chunks found in data folder"}
        
        logger.info(f"📄 Adding {len(chunks)} new chunks...")
        vs.add_documents(chunks)
        
        # Get new count
        collection_info = vs.get_collection_info()
        new_count = collection_info.get("vectors_count", 0) or collection_info.get("points_count", 0)
        
        return {
            "message": "Re-ingestion complete",
            "old_count": old_count,
            "new_chunks": len(chunks),
            "new_count": new_count,
            "added": new_count - old_count
        }
        
    except Exception as e:
        logger.error(f"Error during re-ingestion: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/admin/clear")
async def clear_vector_store():
    """
    Clear entire vector store (delete all documents).
    ⚠️ WARNING: This deletes ALL documents! Use with caution.
    """
    try:
        logger.warning("⚠️ CLEARING ENTIRE VECTOR STORE")
        
        vs = get_vector_store()
        
        # Get count before deletion
        collection_info = vs.get_collection_info()
        count_before = collection_info.get("vectors_count", 0) or collection_info.get("points_count", 0)
        
        # Delete the collection
        vs.client.delete_collection(vs.collection_name)
        logger.info(f"🗑️ Deleted collection: {vs.collection_name}")
        
        # Recreate empty collection
        vs.client.create_collection(
            collection_name=vs.collection_name,
            vectors_config={
                "size": 1536,  # OpenAI embedding dimension
                "distance": "Cosine"
            }
        )
        logger.info(f"✅ Recreated empty collection: {vs.collection_name}")
        
        return {
            "message": "Vector store cleared successfully",
            "documents_deleted": count_before,
            "collection": vs.collection_name,
            "warning": "Collection is now empty. Run /admin/reingest to reload documents."
        }
        
    except Exception as e:
        logger.error(f"Error clearing vector store: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/admin/documents/{source_name}")
async def delete_documents_by_source(source_name: str):
    """
    Delete all documents from a specific source file.
    
    Example: DELETE /admin/documents/CIS_Controls_Guide_v8.1.2_0325_v2.pdf
    """
    try:
        logger.info(f"🗑️ Deleting documents from source: {source_name}")
        
        vs = get_vector_store()
        
        # Get current count
        collection_info = vs.get_collection_info()
        count_before = collection_info.get("vectors_count", 0) or collection_info.get("points_count", 0)
        
        # Delete by metadata filter
        from qdrant_client.models import Filter, FieldCondition, MatchValue
        
        # Try to delete with full path or just filename
        deleted_count = 0
        for source_pattern in [source_name, f"*/{source_name}"]:
            result = vs.client.delete(
                collection_name=vs.collection_name,
                points_selector=Filter(
                    must=[
                        FieldCondition(
                            key="source",
                            match=MatchValue(value=source_pattern)
                        )
                    ]
                )
            )
            if result:
                deleted_count += 1
        
        # Get count after deletion
        collection_info = vs.get_collection_info()
        count_after = collection_info.get("vectors_count", 0) or collection_info.get("points_count", 0)
        
        actual_deleted = count_before - count_after
        
        return {
            "message": f"Documents from '{source_name}' deleted" if actual_deleted > 0 else "No matching documents found",
            "source": source_name,
            "documents_before": count_before,
            "documents_after": count_after,
            "deleted": actual_deleted
        }
        
    except Exception as e:
        logger.error(f"Error deleting documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
