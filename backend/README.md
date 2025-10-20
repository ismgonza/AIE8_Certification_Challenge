# Security Maturity Assistant - RAG System

A production-grade Retrieval-Augmented Generation (RAG) system for security frameworks (CIS, NIST, OWASP, CSA), featuring multi-agent workflow and advanced retrieval techniques.

## 📋 Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Running the Application](#-running-the-application)
- [API Documentation](#-api-documentation)
- [Evaluation Workflow](#-evaluation-workflow-tasks-5-6-7)
- [Advanced Retrieval](#-advanced-retrieval-task-6)
- [Project Structure](#-project-structure)
- [Development](#️-development)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

### Core Features
- **PDF Document Processing**: Automatic loading and intelligent chunking of security framework PDFs
- **Vector Search**: Semantic search using OpenAI embeddings (`text-embedding-3-small`) and Qdrant
- **Agentic RAG**: Multi-agent workflow with LangGraph
  - Analysis Agent: Retrieves relevant security documentation
  - Research Agent: Conditional web search (Tavily) for implementation examples
  - Planning Agent: Synthesizes actionable implementation plans
- **RESTful API**: FastAPI endpoints with auto-generated documentation
- **Flexible Storage**: In-memory or Docker-based Qdrant

### Advanced Retrieval (Task 6)
- **Ensemble Retrieval**: Combines multiple retrieval strategies with reciprocal rank fusion
  - **Vector Search**: Semantic understanding via embeddings
  - **BM25 Retriever**: Keyword matching for exact terms (e.g., "CIS Control 5.2")
  - **Cohere Reranking**: Cross-encoder precision filtering using `rerank-v3.5`
  - Three-way ensemble with weighted fusion (Vector 40%, BM25 30%, Cohere 30%)
  - Improves retrieval quality and response generation

### Evaluation Framework (Tasks 5 & 7)
- **RAGAS Integration**: Comprehensive evaluation with 5 metrics
  - Faithfulness, Response Relevancy, Factual Correctness
  - Context Precision, Context Recall
- **Synthetic Data Generation**: 60-question golden test dataset
- **Comparison Tools**: Side-by-side baseline vs advanced analysis

---

## 🔧 Prerequisites

- **Python**: 3.10 or higher
- **OpenAI API Key**: For embeddings (`text-embedding-3-small`) and LLM (`gpt-4o-mini`)
- **Cohere API Key**: For ensemble reranking (optional, for advanced retrieval)
- **Tavily API Key**: For web search (optional, for research agent)
- **Docker** (recommended): For persistent Qdrant vector store
- **Security PDFs**: Place in `data/` folder (CIS, NIST, OWASP, CSA benchmarks)

---

## 📦 Installation

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Install Dependencies

**Using uv (recommended):**
```bash
uv sync
```

**Using pip:**
```bash
pip install -e .
```

This installs:
- FastAPI & Uvicorn (API server)
- LangChain & LangGraph (agentic workflow)
- Qdrant Client (vector database)
- OpenAI & Cohere (LLM & reranking)
- PyMuPDF (PDF processing)
- RAGAS (evaluation framework)

### 3. Set Up Qdrant

**Option A: Docker (Recommended - Persistent Storage)**

```bash
cd docker
docker-compose up -d

# Verify it's running
docker ps

# Access dashboard
open http://localhost:6333/dashboard
```

**Option B: In-Memory (Quick Start - No Persistence)**

No setup needed! Set `QDRANT_MODE=memory` in `.env`

---

## ⚙️ Configuration

### 1. Create Environment File

```bash
cp .env.example .env
```

### 2. Add API Keys to `.env`

**Minimum Required:**

```env
# Required
OPENAI_API_KEY=sk-proj-your-key-here

# Optional (but recommended for full features)
COHERE_API_KEY=your-cohere-key-here
TAVILY_API_KEY=tvly-your-key-here
```

### 3. Configuration Settings

All other configuration is in `utils/settings.py` with sensible defaults:

```python
# Model Configuration
EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"

# Qdrant Configuration
QDRANT_MODE = "docker"  # or "memory"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
QDRANT_COLLECTION = "security_knowledge"

# Document Processing
CHUNK_SIZE = 1500      # Optimized for security benchmarks
CHUNK_OVERLAP = 300    # 20% overlap for context

# Retrieval Settings
TOP_K = 3              # Number of documents to retrieve

# Advanced Retrieval (Task 6)
USE_ENSEMBLE = False   # Enable ensemble retrieval (Vector + BM25 + Cohere)

# Logging
LOG_LEVEL = "INFO"
```

**To override defaults**, add to `.env`:

```env
# Override any setting
TOP_K=5
USE_RERANKING=False
CHUNK_SIZE=2000
```

### 4. Add PDF Documents

Place security framework PDFs in `data/`:

```bash
backend/
└── data/
    ├── CIS_Amazon_Web_Services_Foundations_Benchmark_v6.0.0.pdf
    ├── CIS_Controls_Guide_v8.1.2_0325_v2.pdf
    ├── NIST.CSWP.29.pdf
    ├── OWASP_Application_Security_Verification_Standard_5.0.0_en.pdf
    └── ... (more security PDFs)
```

---

## 🚀 Running the Application

### 1. Start Qdrant (if using Docker)

```bash
cd docker
docker-compose up -d
```

### 2. Ingest Documents

**Option A: Via API**
```bash
# Start the API first
uvicorn main:app --reload

# Then ingest (in another terminal)
curl -X POST http://localhost:8000/ingest
```

**Option B: Via Script**
```bash
python utils/vector_store.py
```

### 3. Start the API Server

**Development (with auto-reload):**
```bash
uvicorn main:app --reload
```

**Production:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at **http://localhost:8000**

---

## 📖 API Documentation

### Interactive Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Health Check
```bash
GET /health
```

```bash
curl http://localhost:8000/health
```

#### Ingest Documents
```bash
POST /ingest
```

```bash
curl -X POST http://localhost:8000/ingest
```

#### Query RAG System
```bash
POST /query
```

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the CIS Controls?", "top_k": 3}'
```

**Response:**
```json
{
  "answer": "The CIS Controls are...",
  "sources": [
    {
      "content": "CIS Control 1: Inventory...",
      "metadata": {
        "source": "data/CIS_Controls_Guide_v8.1.2.pdf",
        "page": 5
      }
    }
  ]
}
```

#### Collection Info
```bash
GET /collection/info
```

```bash
curl http://localhost:8000/collection/info
```

#### Clear Vector Store
```bash
DELETE /clear
```

```bash
curl -X DELETE http://localhost:8000/clear
```

---

## 📊 Evaluation Workflow (Tasks 5, 6, 7)

Complete evaluation workflow for measuring RAG performance using RAGAS framework.

### Task 5: Golden Test Dataset & Baseline Evaluation

#### Step 1: Generate Synthetic Test Data (Already Done)

```bash
cd ragas
jupyter notebook 01_generate_synthetic_data.ipynb
```

Generates `golden_test_data.csv` with 60 questions.

#### Step 2: Run Baseline Evaluation

```bash
jupyter notebook 02_evaluations.ipynb
```

The notebook runs:
1. **Baseline RAG**: Naive agentic RAG (top_k=3, no reranking)
2. **RAGAS Evaluation**: 5 metrics (Faithfulness, Response Relevancy, etc.)
3. **Results Table**: Performance summary

**Expected Time**: 15-30 minutes for 60 questions  
**Expected Cost**: ~$2-3 (OpenAI + Tavily)

### Task 6: Advanced Retrieval Implementation

**Implemented Technique: Ensemble Retrieval**

```python
# Baseline (Naive Agentic RAG)
rag_baseline = RAGPipeline(
    top_k=3,          # Retrieve 3 documents
    use_tavily=True,  # Web search enabled
    use_agents=True,  # Multi-agent workflow
    use_ensemble=False
)

# Advanced (Ensemble Retrieval)
rag_advanced = RAGPipeline(
    top_k=3,           # Final output: 3 documents
    use_tavily=True,
    use_agents=True,
    use_ensemble=True  # ✨ Vector + BM25 + Cohere ensemble
)
```

**Why Ensemble Retrieval?**

- **Multiple Perspectives**: Combines semantic (vector), lexical (BM25), and precision (Cohere) strategies
- **Better Coverage**: BM25 catches exact keywords that embeddings might miss
- **Improved Precision**: Cohere reranking filters best candidates from larger pool
- **Reciprocal Rank Fusion**: Intelligently merges results from all three sources
- **Critical for Security**: Ensures both exact terms (e.g., "CIS Control 5.2") and conceptual matches are found

### Task 7: Performance Assessment

Run advanced evaluation in same notebook (`02_evaluations.ipynb`):

```python
# 1. Run advanced RAG on dataset
df_advanced = run_rag_on_dataset(df, rag_advanced)

# 2. Evaluate with RAGAS
advanced_results = evaluate_rag_dataset(df_advanced, evaluator_llm)

# 3. Compare with baseline
comparison = compare_evaluations(
    baseline_results,
    advanced_results,
    baseline_name="Baseline (Naive)",
    advanced_name="Advanced (Ensemble)"
)
```

**Expected Improvements:**
- Context Precision: Improved (better document selection)
- Context Recall: Improved (BM25 catches missed keywords)
- Faithfulness: Improved (higher quality context)
- Response Relevancy: Improved (better grounding)

**Note**: The baseline is already sophisticated (multi-agent + web search), so improvements are incremental but consistent across multiple metrics.

### RAGAS Metrics Explained

| Metric | What it Measures | Good Score |
|--------|-----------------|------------|
| **Faithfulness** | Response grounded in retrieved context (no hallucinations) | > 0.7 |
| **Response Relevancy** | Response relevance to the question | > 0.7 |
| **Factual Correctness** | Response matches reference answer | > 0.6 |
| **Context Precision** | Retrieved contexts are relevant | > 0.6 |
| **Context Recall** | All necessary contexts retrieved | > 0.6 |

### Reusing Saved Results

Load and compare without re-running evaluation:

```python
from evaluation_utils import ResultsWrapper
import pandas as pd

# Load saved CSVs (stored in ragas/results/ folder)
baseline_df = pd.read_csv("results/baseline_results_TIMESTAMP.csv")
baseline_results = ResultsWrapper(baseline_df)

advanced_df = pd.read_csv("results/advanced_results_TIMESTAMP.csv")
advanced_results = ResultsWrapper(advanced_df)

# Compare
from evaluation_utils import compare_evaluations
comparison = compare_evaluations(baseline_results, advanced_results)
```

### Evaluation Documentation

See `ragas/README.md` for detailed evaluation guide.

---

## 🚀 Advanced Retrieval (Task 6)

### Ensemble Retrieval

**Implementation**: `utils/advanced_retrieval.py`

**How it Works:**
1. **Vector Retriever**: Retrieves 15 candidates using semantic embeddings
2. **BM25 Retriever**: Retrieves 15 candidates using keyword matching (exact term scores)
3. **Cohere Reranker**: Reranks vector results from 15 → 7 using cross-encoder
4. **Reciprocal Rank Fusion**: Merges all three streams with weights (Vector 40%, BM25 30%, Cohere 30%)
5. **Final Selection**: Returns top 3 documents after fusion

**Configuration:**

```python
# In code
rag = RAGPipeline(
    top_k=3,
    use_ensemble=True
)

# Or via settings.py
USE_ENSEMBLE = True
```

**Cost**: ~$0.10-0.15 for 60 queries (very affordable)

**Latency**: +200-300ms per query (BM25 indexing + Cohere reranking)

### API Setup

1. Sign up at https://cohere.com
2. Get API key from dashboard
3. Add to `.env`:
   ```env
   COHERE_API_KEY=your-cohere-key-here
   ```

### Testing Ensemble Retrieval

```python
from utils.rag import RAGPipeline

# Test without ensemble
rag_baseline = RAGPipeline(use_ensemble=False)
result1 = rag_baseline.query("What are the CIS Controls?")

# Test with ensemble
rag_advanced = RAGPipeline(use_ensemble=True)
result2 = rag_advanced.query("What are the CIS Controls?")

# Compare sources
print("Baseline sources:", len(result1['sources']))
print("Advanced sources:", len(result2['sources']))
print("\nBaseline retrieval: Vector only")
print("Advanced retrieval: Vector + BM25 + Cohere ensemble")
```

---

## 📁 Project Structure

```
backend/
├── data/                          # PDF documents
│   ├── CIS_*.pdf
│   ├── NIST_*.pdf
│   ├── OWASP_*.pdf
│   └── CSA_*.pdf
│
├── docker/                        # Docker configuration
│   ├── docker-compose.yml
│   └── qdrant_storage/           # Persistent Qdrant data
│
├── ragas/                         # Evaluation framework
│   ├── 01_generate_synthetic_data.ipynb  # Generate test dataset
│   ├── 02_evaluations.ipynb      # Run evaluations (Tasks 5, 6, 7)
│   ├── evaluation_utils.py       # Reusable evaluation functions
│   ├── golden_test_data.csv      # 60-question test dataset
│   ├── results/                   # Evaluation results (CSV files)
│   └── README.md                  # Evaluation guide
│
├── utils/                         # Core utilities
│   ├── __init__.py
│   ├── settings.py                # Configuration (most settings here!)
│   ├── document_processor.py     # PDF loading and chunking
│   ├── vector_store.py            # Qdrant operations
│   ├── rag.py                     # RAG pipeline
│   ├── agents.py                  # LangGraph multi-agent workflow
│   ├── advanced_retrieval.py     # Ensemble retrieval (Vector + BM25 + Cohere)
│   ├── tools.py                   # Tavily web search
│   └── prompts.py                 # LLM prompts
│
├── main.py                        # FastAPI application
├── pyproject.toml                 # Dependencies
├── .env.example                   # Environment template
├── .env                           # Your API keys (create from .env.example)
└── README.md                      # This file
```

---

## 🛠️ Development

### Test Document Processing

```bash
python utils/document_processor.py
```

### Test Vector Store

```bash
python utils/vector_store.py
```

### Test RAG Pipeline

```bash
python utils/rag.py
```

### Test Agentic Workflow

```bash
python utils/agents.py
```

### View Configuration

```python
from utils.settings import print_settings
print_settings()
```

---

## 🔍 Troubleshooting

### Qdrant Connection Issues

```bash
# Check if running
docker ps

# View logs
docker logs qdrant

# Restart
cd docker
docker-compose restart

# Clean restart
docker-compose down
docker-compose up -d
```

### OpenAI Rate Limits

- Check API key in `.env`
- Verify account has credits
- Add delays between requests in evaluation

### Cohere API Errors

```bash
# Install Cohere
pip install cohere

# Add API key to .env
echo "COHERE_API_KEY=your-key" >> .env
```

### Evaluation Hangs

- Reduce `max_workers` in `RunConfig` (from 4 to 2)
- Increase `delay_seconds` in `run_rag_on_dataset()`
- Check API rate limits

### Documents Not Ingested

```bash
# Verify PDFs exist
ls -lh data/

# Check collection
curl http://localhost:6333/collections/security_knowledge

# Re-ingest
curl -X POST http://localhost:8000/ingest
```

### Import Errors

```bash
# Reinstall
pip install -e . --force-reinstall

# Or with uv
uv sync --reinstall
```

### Module Not Found (Jupyter)

```python
# Add parent directory to path (in notebook)
import sys
from pathlib import Path
sys.path.append(str(Path.cwd().parent))
```

### Kernel Restart Required (Jupyter)

After modifying Python files:
1. Restart kernel: Kernel → Restart
2. Re-run setup cells
3. Or reload module: `importlib.reload(module)`

---

## 📊 Performance Characteristics

### Baseline (Naive Agentic RAG)

- **Latency**: 2-5 seconds
- **Cost**: ~$0.04-0.06 per query
- **Accuracy**: Good (multi-agent + web search)

### Advanced (With Ensemble Retrieval)

- **Latency**: 2.3-5.5 seconds (+300ms for BM25 + Cohere)
- **Cost**: ~$0.05-0.08 per query (+~$0.01-0.02)
- **Accuracy**: Better (improvements across multiple metrics)

### Storage

- **16 PDFs**: ~90,000 chunks
- **Disk Space**: ~500MB (Qdrant storage)
- **Memory**: ~2GB RAM (during operation)

---

## 🎯 Key Configuration Decisions

### Why top_k=3?

- Balances context quality vs quantity
- Prevents information overload to LLM
- Fast retrieval and reranking
- Works well with reranking (9 candidates → 3 best)

### Why chunk_size=1500?

- Optimized for security benchmarks
- Captures 1-2 complete subsections
- ~300-400 tokens (efficient for LLM context)
- Good balance of specificity and context

### Why Ensemble Retrieval?

- ✅ **Multiple Strategies**: Combines semantic, lexical, and precision approaches
- ✅ **BM25 for Exact Terms**: Crucial for security docs with specific identifiers (e.g., "CIS Control 5.2.1")
- ✅ **Cohere Precision**: Cross-encoder reranking improves document relevance
- ✅ **Reciprocal Rank Fusion**: Intelligently merges diverse retrieval sources
- ✅ **Measurable Improvements**: Gains across multiple RAGAS metrics
- ✅ **Production-Ready**: Efficient, scalable, and well-supported by LangChain

---

## 📝 Notes

### Agentic Workflow

The multi-agent system provides:
1. **Analysis Agent**: Retrieves security documentation from vector store
2. **Research Agent**: Searches web for implementation examples (conditional)
3. **Planning Agent**: Synthesizes comprehensive implementation plan

**When web search triggers:**
- Question is relevant to security/IT (via LLM filter)
- No sufficient context found in vector store
- Tavily API key is configured

### Fair Comparison

Both baseline and advanced return **3 final documents**:
- **Baseline**: Best 3 from vector search
- **Advanced**: Best 3 from ensemble fusion (Vector + BM25 + Cohere)

This ensures fair comparison while demonstrating the value of combining multiple retrieval strategies.

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Cohere Rerank Documentation](https://docs.cohere.com/docs/reranking)
- [RAGAS Documentation](https://docs.ragas.io/)

---

## 🤝 Support

For issues or questions:
1. Check the [Troubleshooting](#-troubleshooting) section
2. Review API documentation at `/docs`
3. Check application logs for error details
4. See `ragas/README.md` for evaluation-specific help

---

**Built with ❤️ for security professionals**

Happy RAG-ing! 🚀
