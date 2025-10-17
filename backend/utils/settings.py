# backend/utils/settings.py
# Environment variables, API keys, paths

"""
Configuration settings loaded from environment variables.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# API Keys
# ============================================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Validate required API keys
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")


# ============================================================================
# Model Configuration
# ============================================================================
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")


# ============================================================================
# Qdrant Configuration
# ============================================================================
QDRANT_MODE = os.getenv("QDRANT_MODE", "docker")  # "memory" or "docker"
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "iso_collections")


# ============================================================================
# Document Processing
# ============================================================================
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))


# ============================================================================
# Paths
# ============================================================================
# Get the project root directory (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / os.getenv("DATA_PATH", "data/")


# ============================================================================
# Retrieval Settings
# ============================================================================
TOP_K = int(os.getenv("TOP_K", "3"))


# ============================================================================
# Logging
# ============================================================================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


# ============================================================================
# Helper function to print configuration (useful for debugging)
# ============================================================================
def print_settings():
    """Print current configuration settings (without sensitive data)"""
    print("=" * 60)
    print("CONFIGURATION SETTINGS")
    print("=" * 60)
    print(f"LLM Model:          {LLM_MODEL}")
    print(f"Embedding Model:    {EMBEDDING_MODEL}")
    print(f"Qdrant Mode:        {QDRANT_MODE}")
    print(f"Qdrant Host:        {QDRANT_HOST}:{QDRANT_PORT}")
    print(f"Qdrant Collection:  {QDRANT_COLLECTION}")
    print(f"Chunk Size:         {CHUNK_SIZE}")
    print(f"Chunk Overlap:      {CHUNK_OVERLAP}")
    print(f"Top K Results:      {TOP_K}")
    print(f"Data Path:          {DATA_PATH}")
    print(f"Log Level:          {LOG_LEVEL}")
    print("=" * 60)


# Uncomment to print settings when module is imported:
# print_settings()