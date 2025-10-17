"""
FastAPI backend for RAG system.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging
import tempfile
from pathlib import Path

from utils import settings
from utils.document_processor import process_pdfs, process_uploaded_files
from utils.vector_store import VectorStore
from utils.rag import RAGPipeline
from utils.standards import get_available_standards, get_standard_info, get_controls_for_standard
from standards.iso_27001_controls import get_high_priority_controls, get_control_by_id

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ISO RAG API",
    description="RAG system for ISO 27001/27002 documents",
    version="1.0.0"
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
            top_k=5,  # Get more context for better answers
            use_tavily=True,  # Search web for implementation examples
            use_agents=True  # Multi-agent workflow for better quality
        )
    return rag_pipeline


# ============================================================================
# Request/Response Models
# ============================================================================

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 3


class Source(BaseModel):
    content: str
    metadata: dict
    score: Optional[float] = None


class QueryResponse(BaseModel):
    answer: str
    sources: List[Source]


class IngestResponse(BaseModel):
    message: str
    total_chunks: int


class CollectionInfo(BaseModel):
    name: str
    vectors_count: Optional[int] = None
    points_count: int
    status: str


class DocumentItem(BaseModel):
    id: str
    content: str
    metadata: dict


class DocumentsResponse(BaseModel):
    total: int
    documents: List[DocumentItem]


class CompanyProfile(BaseModel):
    company_name: str
    company_size: str
    industry: str
    tech_stack: List[str]
    deadline_months: Optional[int] = 6


class Control(BaseModel):
    id: str
    title: str
    theme: str
    priority: str
    estimated_hours: int
    owner: str
    deliverables: List[str]
    description: str
    status: Optional[str] = "pending"  # pending, in_progress, completed


class ControlsResponse(BaseModel):
    total: int
    completed: int
    in_progress: int
    pending: int
    controls: List[Control]


# ============================================================================
# Endpoints
# ============================================================================

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "ISO Implementation Assistant API",
        "version": "2.0.0",
        "supported_standards": ["ISO_27001", "ISO_31000", "ISO_19011", "ISO_9001"]
    }


@app.get("/standards")
async def get_standards():
    """
    Get all supported standards (current and coming soon).
    """
    try:
        standards = get_available_standards()
        return {"standards": standards}
    except Exception as e:
        logger.error(f"Error getting standards: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/controls", response_model=ControlsResponse)
async def get_controls(standard: str = "ISO_27001"):
    """
    Get all controls for a specific standard.
    Defaults to ISO 27001 for backwards compatibility.
    """
    try:
        controls = get_controls_for_standard(standard)
        
        if not controls:
            raise HTTPException(
                status_code=404, 
                detail=f"Standard '{standard}' not found or not yet implemented"
            )
        
        # For now, all controls are pending
        # In future, load from database
        controls_with_status = [Control(**c, status="pending") for c in controls]
        
        return ControlsResponse(
            total=len(controls_with_status),
            completed=0,
            in_progress=0,
            pending=len(controls_with_status),
            controls=controls_with_status
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting controls: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/controls/priority/high")
async def get_priority_controls():
    """
    Get high-priority controls (recommended to do first).
    """
    try:
        controls = get_high_priority_controls()
        return {"controls": controls}
    except Exception as e:
        logger.error(f"Error getting priority controls: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/controls/{control_id}")
async def get_control_detail(control_id: str):
    """
    Get detailed information about a specific control.
    """
    try:
        control = get_control_by_id(control_id)
        if not control:
            raise HTTPException(status_code=404, detail="Control not found")
        return control
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting control {control_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


class ImplementRequest(BaseModel):
    company_size: Optional[str] = "50-100"
    industry: Optional[str] = "Software/SaaS"
    tech_stack: Optional[List[str]] = ["Cloud", "SaaS"]
    deadline_months: Optional[int] = 6


@app.post("/controls/{control_id}/implement")
async def generate_implementation_guide(control_id: str, request: ImplementRequest):
    """
    Generate implementation guide for a specific control.
    Uses agentic RAG to create customized guidance.
    """
    try:
        control = get_control_by_id(control_id)
        if not control:
            raise HTTPException(status_code=404, detail="Control not found")
        
        # Build customized question with company context
        question = f"""How do I implement ISO 27001 Control {control_id} ({control['title']})?

Company Context:
- Size: {request.company_size}
- Industry: {request.industry}
- Tech Stack: {', '.join(request.tech_stack)}
- Deadline: {request.deadline_months} months"""
        
        # Use RAG pipeline to generate guide
        rag = get_rag_pipeline()
        result = rag.query(question, return_sources=True)
        
        return {
            "control_id": control_id,
            "control_title": control["title"],
            "implementation_guide": result["answer"],
            "sources": result.get("sources", [])
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating implementation guide: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Detailed health check."""
    vs = get_vector_store()
    collection_info = vs.get_collection_info()
    
    return {
        "status": "healthy",
        "settings": {
            "data_path": str(settings.DATA_PATH),
            "chunk_size": settings.CHUNK_SIZE,
            "chunk_overlap": settings.CHUNK_OVERLAP,
            "llm_model": settings.LLM_MODEL,
            "embedding_model": settings.EMBEDDING_MODEL,
            "qdrant_mode": settings.QDRANT_MODE,
            "collection_name": settings.QDRANT_COLLECTION,
        },
        "vector_store": collection_info
    }


@app.post("/upload", response_model=IngestResponse)
async def upload_documents(
    files: List[UploadFile] = File(...),
    clear_existing: bool = False
):
    """
    Upload PDF files and ingest them into vector store.
    
    Args:
        files: List of PDF files to upload
        clear_existing: If True, clear vector store before ingesting
    """
    try:
        logger.info(f"Received {len(files)} files for upload")
        
        # Validate files are PDFs
        for file in files:
            if not file.filename.endswith('.pdf'):
                raise HTTPException(
                    status_code=400, 
                    detail=f"File {file.filename} is not a PDF"
                )
        
        # Clear existing if requested
        vs = get_vector_store()
        if clear_existing:
            logger.info("Clearing existing documents...")
            try:
                vs.delete_collection()
            except:
                pass
        
        # Read uploaded files
        file_data = []
        for file in files:
            content = await file.read()
            file_data.append((file.filename, content))
        
        # Process files in temp directory
        with tempfile.TemporaryDirectory() as temp_dir:
            chunks = process_uploaded_files(file_data, Path(temp_dir))
            vs.add_documents(chunks)
        
        logger.info(f"✅ Successfully ingested {len(chunks)} chunks from {len(files)} files")
        
        return IngestResponse(
            message=f"Successfully uploaded and ingested {len(files)} PDF(s)",
            total_chunks=len(chunks)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during upload: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """
    Query the RAG system.
    """
    try:
        logger.info(f"Received query: {request.query}")
        
        # Get RAG pipeline
        rag = get_rag_pipeline()
        
        # Process query
        result = rag.query(request.query, return_sources=True)
        
        # Format response
        sources = [
            Source(
                content=src["content"],
                metadata=src["metadata"]
            )
            for src in result["sources"]
        ]
        
        return QueryResponse(
            answer=result["answer"],
            sources=sources
        )
    except Exception as e:
        logger.error(f"Error during query: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/collection/info", response_model=CollectionInfo)
async def get_collection_info():
    """
    Get information about the vector store collection.
    """
    try:
        vs = get_vector_store()
        info = vs.get_collection_info()
        
        if not info:
            raise HTTPException(status_code=404, detail="Collection not found")
        
        return CollectionInfo(**info)
    except Exception as e:
        logger.error(f"Error getting collection info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents", response_model=DocumentsResponse)
async def get_documents(limit: int = 10, offset: int = 0):
    """
    Browse documents in the vector store.
    """
    try:
        vs = get_vector_store()
        
        # Get documents from Qdrant
        from qdrant_client.models import Filter
        
        result = vs.client.scroll(
            collection_name=vs.collection_name,
            limit=limit,
            offset=offset,
            with_payload=True,
            with_vectors=False
        )
        
        points, _ = result
        
        # Get total count
        collection_info = vs.client.get_collection(vs.collection_name)
        total = collection_info.points_count or 0
        
        # Format documents
        documents = [
            DocumentItem(
                id=str(point.id),
                content=point.payload.get("page_content", ""),
                metadata=point.payload.get("metadata", {})
            )
            for point in points
        ]
        
        return DocumentsResponse(total=total, documents=documents)
    except Exception as e:
        logger.error(f"Error getting documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/clear")
async def clear_vector_store():
    """
    Clear all documents from vector store.
    """
    try:
        logger.info("Clearing vector store...")
        vs = get_vector_store()
        vs.delete_collection()
        
        logger.info("✅ Vector store cleared")
        
        return {"message": "Vector store cleared successfully"}
    except Exception as e:
        logger.error(f"Error clearing vector store: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("🚀 Starting ISO RAG API...")
    logger.info(f"Data path: {settings.DATA_PATH}")
    logger.info(f"Qdrant mode: {settings.QDRANT_MODE}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("👋 Shutting down ISO RAG API...")


# ============================================================================
# Run with: uvicorn main:app --reload
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)