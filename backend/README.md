# ISO RAG System

A Retrieval-Augmented Generation (RAG) system for ISO 27001/27002 documents, built with FastAPI, LangChain, and Qdrant.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## ✨ Features

- **PDF Document Processing**: Automatically load and chunk ISO standard PDFs
- **Vector Search**: Semantic search using OpenAI embeddings and Qdrant
- **RESTful API**: FastAPI endpoints for document ingestion and querying
- **Flexible Storage**: Support for both in-memory and Docker-based Qdrant
- **Interactive Docs**: Auto-generated Swagger UI and ReDoc

---

## 🔧 Prerequisites

- **Python**: 3.10 or higher
- **OpenAI API Key**: For embeddings and LLM
- **Docker** (optional): For persistent Qdrant vector store
- **PDFs**: ISO 27001/27002 documents (or any PDFs you want to query)

---

## 📦 Installation

### 1. Clone/Navigate to the Backend Directory

```bash
cd backend
```

### 2. Install Python Dependencies

```bash
pip install -e .
```

This will install:
- FastAPI & Uvicorn
- LangChain & LangChain OpenAI
- Qdrant Client
- PyMuPDF (for PDF processing)
- Python-dotenv

### 3. Set Up Qdrant (Choose One Option)

#### Option A: In-Memory (Quick Start - No Persistence)

No setup needed! Data will be stored in memory and lost on restart.

#### Option B: Docker (Recommended - Persistent Storage)

```bash
# Start Qdrant container
docker-compose up -d

# Verify it's running
docker ps

# Access Qdrant dashboard
open http://localhost:6333/dashboard
```

---

## ⚙️ Configuration

### 1. Create Environment File

Copy the example environment file:

```bash
cp .env.example .env
```

### 2. Edit `.env` File

**Minimum Required Configuration:**

```env
# Required: Your OpenAI API Key
OPENAI_API_KEY=sk-proj-your-actual-key-here

# Choose storage mode: "memory" or "docker"
QDRANT_MODE=docker
```

**Full Configuration Options:**

```env
# =============================================================================
# API Keys
# =============================================================================
OPENAI_API_KEY=sk-proj-your-key-here
TAVILY_API_KEY=tvly-dev-your-key-here  # Optional

# =============================================================================
# Model Configuration
# =============================================================================
EMBEDDING_MODEL=text-embedding-3-small  # OpenAI embedding model
LLM_MODEL=gpt-4o-mini                   # OpenAI chat model

# =============================================================================
# Qdrant Configuration
# =============================================================================
QDRANT_MODE=docker                      # Options: "memory" or "docker"
QDRANT_HOST=localhost                   # Qdrant host (for docker mode)
QDRANT_PORT=6333                        # Qdrant port
QDRANT_COLLECTION=iso_documents         # Collection name

# =============================================================================
# Document Processing
# =============================================================================
CHUNK_SIZE=1500                         # Characters per chunk (recommended for ISO docs)
CHUNK_OVERLAP=300                       # Overlap between chunks

# =============================================================================
# Paths
# =============================================================================
DATA_PATH=data/                         # Directory containing PDF files

# =============================================================================
# Retrieval Settings
# =============================================================================
TOP_K=3                                 # Default number of results to retrieve

# =============================================================================
# Logging
# =============================================================================
LOG_LEVEL=INFO                          # Options: DEBUG, INFO, WARNING, ERROR
```

### 3. Add Your PDF Documents

Place your PDF files in the `data/` directory:

```bash
backend/
└── data/
    ├── isoiec_27001_2022.pdf
    └── isoiec_27002_2022.pdf
```

---

## 🚀 Running the Application

### Start the API Server

**Development Mode (with auto-reload):**

```bash
uvicorn main:app --reload
```

**Production Mode:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Custom Port:**

```bash
uvicorn main:app --port 8080
```

The API will be available at: **http://localhost:8000**

---

## 📖 API Documentation

### Interactive Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available Endpoints

#### 1. Health Check

```bash
GET /
GET /health
```

**Example:**
```bash
curl http://localhost:8000/health
```

**Response:**
```json
{
  "status": "healthy",
  "settings": {
    "data_path": "data/",
    "chunk_size": 1500,
    "qdrant_mode": "docker"
  },
  "vector_store": {
    "name": "iso_documents",
    "vectors_count": 150,
    "points_count": 150
  }
}
```

---

#### 2. Ingest Documents

Loads PDFs from `data/` folder and stores them in the vector database.

```bash
POST /ingest
```

**Example:**
```bash
curl -X POST http://localhost:8000/ingest
```

**Response:**
```json
{
  "message": "Documents ingested successfully",
  "total_chunks": 150
}
```

---

#### 3. Query RAG System

Search for relevant information and get AI-generated answers.

```bash
POST /query
```

**Request Body:**
```json
{
  "query": "What is ISO 27001?",
  "top_k": 3
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ISO 27001?", "top_k": 3}'
```

**Response:**
```json
{
  "answer": "Based on the documents...",
  "sources": [
    {
      "content": "ISO/IEC 27001:2022 specifies...",
      "metadata": {
        "source": "data/isoiec_27001_2022.pdf",
        "page": 1
      },
      "score": 0.89
    }
  ]
}
```

---

#### 4. Get Collection Info

Get statistics about the vector store.

```bash
GET /collection/info
```

**Example:**
```bash
curl http://localhost:8000/collection/info
```

**Response:**
```json
{
  "name": "iso_documents",
  "vectors_count": 150,
  "points_count": 150,
  "status": "green"
}
```

---

#### 5. Clear Vector Store

Delete all documents from the vector database.

```bash
DELETE /clear
```

**Example:**
```bash
curl -X DELETE http://localhost:8000/clear
```

**Response:**
```json
{
  "message": "Vector store cleared successfully"
}
```

---

## 📁 Project Structure

```
backend/
├── data/                           # PDF documents
│   ├── isoiec_27001_2022.pdf
│   └── isoiec_27002_2022.pdf
│
├── docker/                         # Docker configuration (optional)
│   └── qdrant_storage/            # Persistent Qdrant data
│
├── utils/                          # Core utilities
│   ├── __init__.py
│   ├── settings.py                # Configuration management
│   ├── document_processor.py      # PDF loading and chunking
│   └── vector_store.py            # Qdrant vector store operations
│
├── main.py                         # FastAPI application
├── docker-compose.yml              # Qdrant Docker setup
├── pyproject.toml                  # Python dependencies
├── .env                            # Environment variables (create from .env.example)
├── .env.example                    # Environment template
└── README.md                       # This file
```

---

## 🛠️ Development

### Test Document Processing

Test PDF loading and chunking without starting the API:

```bash
python -m utils.document_processor
```

This will:
- Load all PDFs from `data/`
- Chunk them according to your settings
- Display statistics

---

### Test Vector Store

Test Qdrant operations:

```bash
python -m utils.vector_store
```

This will:
- Connect to Qdrant
- Process and ingest documents
- Run a test search query

---

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .
```

---

## 🔍 Troubleshooting

### Qdrant Connection Issues

**Problem**: Can't connect to Qdrant

**Solution**:
```bash
# Check if Qdrant is running
docker ps

# View Qdrant logs
docker logs qdrant

# Restart Qdrant
docker-compose restart

# Or rebuild
docker-compose down
docker-compose up -d
```

---

### OpenAI API Errors

**Problem**: Authentication errors or rate limits

**Solution**:
1. Verify your API key in `.env` is correct
2. Check your OpenAI account has credits
3. Reduce request frequency if hitting rate limits

---

### PDF Loading Issues

**Problem**: PDFs not found or can't be loaded

**Solution**:
```bash
# Verify PDFs exist
ls data/

# Check file permissions
chmod 644 data/*.pdf

# Verify path in .env
cat .env | grep DATA_PATH
```

---

### Import Errors

**Problem**: Module not found errors

**Solution**:
```bash
# Reinstall dependencies
pip install -e . --force-reinstall

# Or create fresh virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

---

### Memory Issues

**Problem**: Out of memory when processing large PDFs

**Solution**:
1. Reduce `CHUNK_SIZE` in `.env` (e.g., from 1500 to 1000)
2. Process PDFs in smaller batches
3. Use Docker mode for better memory management

---

### Port Already in Use

**Problem**: Port 8000 or 6333 already in use

**Solution**:
```bash
# For API (port 8000)
uvicorn main:app --port 8080

# For Qdrant (port 6333)
# Edit docker-compose.yml and change port mapping:
# ports:
#   - "6334:6333"  # Use port 6334 on host
```

---

## 🛑 Stopping the Application

### Stop API Server

Press `Ctrl+C` in the terminal where uvicorn is running.

### Stop Qdrant (Docker Mode)

```bash
# Stop Qdrant (data persists)
docker-compose down

# Stop and remove all data
docker-compose down -v
```

---

## 📝 Notes

### Storage Modes

**In-Memory Mode (`QDRANT_MODE=memory`)**:
- ✅ Quick setup, no Docker required
- ✅ Fast performance
- ❌ Data lost on restart
- ✅ Good for: Development, testing

**Docker Mode (`QDRANT_MODE=docker`)**:
- ✅ Data persists between restarts
- ✅ Production-ready
- ✅ Scalable
- ❌ Requires Docker
- ✅ Good for: Production, persistent storage

---

### Chunking Strategy

The default settings (`CHUNK_SIZE=1500`, `CHUNK_OVERLAP=300`) are optimized for ISO standards because:
- ISO documents have clear hierarchical sections
- 1500 characters ≈ 1-2 complete subsections
- 300 overlap ensures cross-references stay connected

Adjust these values based on your documents:
- **Technical docs with sections**: 1500-2000 chunk size
- **Dense continuous text**: 1000-1500 chunk size
- **Short articles**: 500-1000 chunk size

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

---

## 📄 License

This project is for educational and internal use with ISO standard documents.

---

## 🤝 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review API documentation at `/docs`
3. Check application logs for error details

---

**Happy RAG-ing! 🚀**