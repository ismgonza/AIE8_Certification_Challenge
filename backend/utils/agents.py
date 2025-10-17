"""
Agentic RAG system with LangGraph for ISO implementation guidance.
"""
from typing import TypedDict, List, Annotated
import logging

from langchain_openai import ChatOpenAI
from langchain.schema import Document
from langgraph.graph import StateGraph, END
import operator

from utils import settings
from utils.vector_store import VectorStore
from utils.tools import search_tavily
from utils.prompts import IMPLEMENTATION_CONSULTANT_PROMPT

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# ============================================================================
# State Definition
# ============================================================================

class AgentState(TypedDict):
    """State passed between agents."""
    question: str
    iso_requirements: str  # From Analysis Agent
    research_results: str  # From Research Agent
    implementation_plan: str  # From Generation Agent
    sources: List[Document]  # Retrieved documents
    error: str  # Error message if any


# ============================================================================
# Agent Functions
# ============================================================================

def analysis_agent(state: AgentState) -> AgentState:
    """
    AGENT 1: Analyze the query and extract ISO requirements.
    
    - Parse what control is being asked about
    - Retrieve relevant ISO documentation
    - Extract specific requirements
    """
    logger.info("🔍 Analysis Agent: Analyzing query and retrieving ISO requirements")
    
    question = state["question"]
    
    # Retrieve ISO documentation from vector store
    vs = VectorStore()
    docs = vs.search(question, top_k=5)
    
    # Create context from retrieved docs
    iso_context = "\n\n".join([doc.page_content for doc in docs])
    
    # Analyze with LLM
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    analysis_prompt = f"""You are analyzing an ISO 27001/27002 implementation question.

Question: {question}

ISO Documentation:
{iso_context}

Extract and summarize:
1. Which ISO control(s) this relates to
2. Specific requirements from the ISO standard
3. What deliverables are needed for compliance
4. Key terms and concepts to research

Be concise but comprehensive. Format as bullet points."""
    
    analysis = llm.invoke(analysis_prompt)
    
    return {
        **state,
        "iso_requirements": analysis.content,
        "sources": docs
    }


def research_agent(state: AgentState) -> AgentState:
    """
    AGENT 2: Research implementation approaches, tools, and best practices.
    
    - Search web for implementation guides
    - Find tool recommendations
    - Gather pricing and examples
    """
    logger.info("🔎 Research Agent: Searching for implementation examples and tools")
    
    question = state["question"]
    iso_requirements = state["iso_requirements"]
    
    # Search Tavily for implementation resources
    tavily_results = search_tavily(question, max_results=5)
    
    # Analyze research findings
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    research_prompt = f"""You are researching implementation approaches for an ISO control.

Question: {question}

ISO Requirements:
{iso_requirements}

Web Research Results:
{tavily_results or "No web results available"}

Summarize your research findings:
1. Specific tools and products (with pricing)
2. Implementation approaches from real examples
3. Common configurations or settings
4. Best practices from industry

Focus on ACTIONABLE information (tool names, prices, specific steps)."""
    
    research = llm.invoke(research_prompt)
    
    return {
        **state,
        "research_results": research.content
    }


def generation_agent(state: AgentState) -> AgentState:
    """
    AGENT 3: Generate comprehensive implementation plan.
    
    - Combine ISO requirements + research findings
    - Create step-by-step plan with real content
    - Include copy-paste templates
    - List audit evidence
    """
    logger.info("📝 Generation Agent: Creating implementation plan")
    
    question = state["question"]
    iso_requirements = state["iso_requirements"]
    research_results = state["research_results"]
    
    # Combine all context
    full_context = f"""**ISO 27001/27002 Documentation:**

{iso_requirements}

{research_results}
"""
    
    # Generate implementation plan
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0.3,  # Slightly higher for creative implementation ideas
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    messages = IMPLEMENTATION_CONSULTANT_PROMPT.format_messages(
        context=full_context,
        question=question
    )
    
    response = llm.invoke(messages)
    
    return {
        **state,
        "implementation_plan": response.content
    }


# ============================================================================
# Graph Construction
# ============================================================================

def create_agent_graph() -> StateGraph:
    """
    Create the agentic RAG workflow graph.
    
    Flow:
    Query → Analysis Agent → Research Agent → Generation Agent → Answer
    """
    logger.info("🔧 Building agentic RAG graph")
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("analyze", analysis_agent)
    workflow.add_node("research", research_agent)
    workflow.add_node("generate", generation_agent)
    
    # Add edges (sequential flow)
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "research")
    workflow.add_edge("research", "generate")
    workflow.add_edge("generate", END)
    
    # Compile
    app = workflow.compile()
    
    logger.info("✅ Agentic RAG graph built successfully")
    return app


# ============================================================================
# Main Interface
# ============================================================================

def run_agentic_rag(question: str) -> dict:
    """
    Run the full agentic RAG pipeline.
    
    Args:
        question: User's implementation question
        
    Returns:
        Dict with implementation_plan and sources
    """
    logger.info(f"🚀 Starting agentic RAG for: '{question}'")
    
    # Create graph
    app = create_agent_graph()
    
    # Initialize state
    initial_state = {
        "question": question,
        "iso_requirements": "",
        "research_results": "",
        "implementation_plan": "",
        "sources": [],
        "error": ""
    }
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    logger.info("✅ Agentic RAG completed")
    
    return {
        "answer": final_state["implementation_plan"],
        "sources": [
            {
                "content": doc.page_content,
                "metadata": doc.metadata
            }
            for doc in final_state.get("sources", [])
        ]
    }

