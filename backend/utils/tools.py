"""
External tools for RAG enhancement (Tavily search, etc.)
"""
from typing import Optional
import logging

from tavily import TavilyClient

from utils import settings

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def search_tavily(query: str, max_results: int = 3) -> Optional[str]:
    """
    Search Tavily for real-world implementation examples.
    
    Args:
        query: Search query
        max_results: Number of results to return
        
    Returns:
        Formatted search results or None
    """
    if not settings.TAVILY_API_KEY:
        logger.warning("Tavily API key not configured")
        return None
    
    try:
        logger.info(f"Searching Tavily for: '{query}'")
        
        # Initialize client
        client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        
        # Search for implementation examples
        search_query = f"{query} implementation guide best practices tools"
        results = client.search(query=search_query, max_results=max_results)
        
        if not results.get('results'):
            return None
        
        # Format results
        tavily_context = "\n\n**Additional Resources from Web:**\n\n"
        for idx, result in enumerate(results['results'][:max_results], 1):
            tavily_context += f"{idx}. **{result.get('title', 'Resource')}**\n"
            tavily_context += f"   {result.get('content', '')[:200]}...\n"
            tavily_context += f"   Source: {result.get('url', '')}\n\n"
        
        logger.info(f"✅ Found {len(results['results'])} Tavily results")
        return tavily_context
    
    except Exception as e:
        logger.warning(f"Tavily search failed: {e}")
        return None

