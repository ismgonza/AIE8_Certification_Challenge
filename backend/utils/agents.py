"""
Agentic RAG system with LangGraph for security implementation guidance.
Provides answers based on CIS, NIST, OWASP, and CSA frameworks.
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
from utils.prompts import SECURITY_ADVISOR_PROMPT

# Setup logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


# ============================================================================
# State Definition
# ============================================================================

class AgentState(TypedDict):
    """State passed between agents."""
    question: str
    iso_requirements: str  # Security requirements from Analysis Agent (CIS, NIST, OWASP, CSA)
    research_results: str  # From Research Agent
    implementation_plan: str  # From Generation Agent
    sources: List[Document]  # Retrieved documents
    used_web_search: bool  # Whether Tavily was used
    error: str  # Error message if any
    # Advanced retrieval settings (Task 6)
    use_reranking: bool
    reranker_model: str
    use_ensemble: bool


# ============================================================================
# Agent Functions
# ============================================================================

def analysis_agent(state: AgentState) -> AgentState:
    """
    AGENT 1: Analyze the query and extract security requirements.
    
    - Parse what security control/practice is being asked about
    - Retrieve relevant documentation (CIS, NIST, OWASP, CSA)
    - Extract specific requirements and recommendations
    """
    logger.info("🔍 Analysis Agent: Analyzing query and retrieving security documentation")
    
    question = state["question"]
    
    # Get advanced retrieval settings from state
    use_reranking = state.get("use_reranking", False)
    reranker_model = state.get("reranker_model", "cohere")
    use_ensemble = state.get("use_ensemble", False)
    
    # Retrieve security documentation from vector store
    vs = VectorStore()
    
    # Use ensemble retrieval if enabled (Vector + BM25 + Cohere)
    if use_ensemble:
        logger.info("Using ensemble retrieval in analysis agent")
        from utils.advanced_retrieval import get_ensemble_retriever
        ensemble_retriever = get_ensemble_retriever(vs, top_k=5, use_cohere=True)
        docs = ensemble_retriever.get_relevant_documents(question)[:5]
    # Fallback: Legacy reranking or simple vector search
    else:
        # Get more docs if reranking (better recall before reranking filters)
        initial_top_k = 15 if use_reranking else 5
        docs = vs.search(question, top_k=initial_top_k)
        
        # Apply reranking if enabled
        if use_reranking and len(docs) > 5:
            from utils.advanced_retrieval import rerank_documents
            docs = rerank_documents(question, docs, top_k=5, model=reranker_model)
    
    # Create context from retrieved docs
    security_context = "\n\n".join([doc.page_content for doc in docs])
    
    # Analyze with LLM
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    analysis_prompt = f"""You are analyzing a security implementation question.

Question: {question}

Security Documentation (CIS Benchmarks, NIST, OWASP, CSA):
{security_context}

Extract and summarize:
1. Which security controls or best practices this relates to
2. Specific requirements from the standards
3. What needs to be configured or implemented
4. Key technical terms and concepts

Be concise but comprehensive. Format as bullet points."""
    
    analysis = llm.invoke(analysis_prompt)
    
    return {
        **state,
        "iso_requirements": analysis.content,  # Keep name for backward compatibility
        "sources": docs
    }


def should_search_web(state: AgentState) -> str:
    """
    Decision node: Determine if web search is needed.
    
    Returns:
        "search_web" or "skip_web"
    """
    question = state["question"]
    iso_requirements = state["iso_requirements"]
    sources = state.get("sources", [])
    
    # Quick heuristic: if we found less than 3 good sources, might need web
    if len(sources) < 3:
        logger.info("⚠️ Limited sources found - will search web")
        return "search_web"
    
    # Smart check: If sources are from CIS Benchmarks, they're ALWAYS actionable
    # CIS Benchmarks contain specific commands and configurations
    source_names = [doc.metadata.get("source", "").lower() for doc in sources]
    cis_benchmark_count = sum(1 for name in source_names if "cis" in name and "benchmark" in name)
    
    if cis_benchmark_count >= 2:
        logger.info(f"✅ Found {cis_benchmark_count} CIS Benchmark sources - skipping web search")
        logger.info("💡 CIS Benchmarks contain specific commands and configurations")
        return "skip_web"
    
    # Check if question is asking for product recommendations or comparisons
    # These need web search for current pricing and options
    question_lower = question.lower()
    needs_market_info = any(keyword in question_lower for keyword in [
        "best", "recommend", "which tool", "which product", "compare",
        "pricing", "cost", "free", "open source alternatives"
    ])
    
    if needs_market_info:
        logger.info("🔍 Question asks for tool recommendations - will search web for current options")
        return "search_web"
    
    # For other cases, do a quick LLM check
    # But look at actual source content, not just the analysis
    sample_content = "\n\n".join([
        f"Source {i+1}: {doc.page_content[:300]}"
        for i, doc in enumerate(sources[:3])
    ])
    
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    completeness_check = f"""Does this documentation contain SPECIFIC commands, scripts, or configuration steps to answer the question?

Question: {question}

Sample from documentation:
{sample_content}

Answer ONLY: YES or NO

YES = Has bash/PowerShell commands, specific config files, step-by-step technical procedures
NO = Mostly theory, principles, or recommendations without specific commands"""
    
    completeness = llm.invoke(completeness_check)
    decision = "skip_web" if "YES" in completeness.content.upper() else "search_web"
    
    logger.info(f"🎯 Decision: {decision.upper().replace('_', ' ')}")
    return decision


def web_search_agent(state: AgentState) -> AgentState:
    """
    AGENT 2a: Search web for additional details.
    Only called if should_search_web returns "search_web"
    """
    logger.info("📡 Web Search Agent: Searching for implementation examples")
    
    question = state["question"]
    tavily_results = search_tavily(question, max_results=5)
    
    return {
        **state,
        "research_results": f"**Web Research Results:**\n{tavily_results or 'No results found'}",
        "used_web_search": True
    }


def skip_web_agent(state: AgentState) -> AgentState:
    """
    AGENT 2b: Skip web search.
    Only called if should_search_web returns "skip_web"
    """
    logger.info("✅ Skip Web Agent: PDF documentation is sufficient")
    
    return {
        **state,
        "research_results": "**Note:** Using only documentation from CIS/NIST/OWASP (web search not needed)",
        "used_web_search": False
    }


def generation_agent(state: AgentState) -> AgentState:
    """
    AGENT 3: Generate comprehensive implementation plan.
    
    - Combine security standards + research findings
    - Create step-by-step plan with real content
    - Include copy-paste commands and scripts
    - Provide verification steps
    """
    logger.info("📝 Generation Agent: Creating implementation plan")
    
    question = state["question"]
    iso_requirements = state["iso_requirements"]  # Actually contains all security docs
    research_results = state["research_results"]
    
    # Combine all context
    full_context = f"""**Security Standards Documentation (CIS, NIST, OWASP, CSA):**

{iso_requirements}

**Additional Research:**
{research_results}
"""
    
    # Generate implementation plan
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0.3,  # Slightly higher for creative implementation ideas
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    messages = SECURITY_ADVISOR_PROMPT.format_messages(
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
    Create the agentic RAG workflow graph with conditional web search.
    
    Flow:
    Query → Analysis → [Decision] → Web Search OR Skip → Generation → Answer
                           ↓              ↓
                      (if needed)    (if sufficient)
    """
    logger.info("🔧 Building agentic RAG graph with conditional Tavily")
    
    # Create graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("analyze", analysis_agent)
    workflow.add_node("web_search", web_search_agent)
    workflow.add_node("skip_web", skip_web_agent)
    workflow.add_node("generate", generation_agent)
    
    # Add edges
    workflow.set_entry_point("analyze")
    
    # Conditional edge: decide if we need web search
    workflow.add_conditional_edges(
        "analyze",
        should_search_web,  # Decision function
        {
            "search_web": "web_search",  # If needs more info
            "skip_web": "skip_web"       # If PDFs are sufficient
        }
    )
    
    # Both paths lead to generation
    workflow.add_edge("web_search", "generate")
    workflow.add_edge("skip_web", "generate")
    workflow.add_edge("generate", END)
    
    # Compile
    app = workflow.compile()
    
    logger.info("✅ Agentic RAG graph built with conditional Tavily")
    return app


# ============================================================================
# Question Relevance Check
# ============================================================================

def check_question_relevance(question: str) -> tuple[bool, str]:
    """
    Check if the question is related to security, IT infrastructure, or technology.
    
    Args:
        question: User's question
        
    Returns:
        Tuple of (is_relevant: bool, reason: str)
    """
    llm = ChatOpenAI(
        model=settings.LLM_MODEL,
        temperature=0,
        openai_api_key=settings.OPENAI_API_KEY
    )
    
    relevance_check_prompt = f"""You are a security assistant filter. Determine if this question is related to:
- Cybersecurity (firewalls, encryption, authentication, etc.)
- IT infrastructure (servers, networking, cloud, databases)
- Technology configuration (Windows, Linux, macOS, routers, etc.)
- Security frameworks (CIS Controls, NIST, OWASP, CSA, ISO, etc.)
- DevOps/DevSecOps
- Compliance and security best practices

Question: "{question}"

Answer with ONLY one of these responses:
- "RELEVANT" if the question is about security, IT, or technology
- "NOT_RELEVANT: [brief reason]" if it's about something else (pets, cooking, sports, etc.)

Your response:"""
    
    response = llm.invoke(relevance_check_prompt)
    answer = response.content.strip()
    
    if answer.startswith("RELEVANT"):
        return True, ""
    else:
        # Extract reason
        reason = answer.replace("NOT_RELEVANT:", "").strip()
        return False, reason


# ============================================================================
# Main Interface
# ============================================================================

def run_agentic_rag(
    question: str, 
    use_reranking: bool = False,
    reranker_model: str = "cohere",
    use_ensemble: bool = False
) -> dict:
    """
    Run the full agentic RAG pipeline.
    
    Args:
        question: User's implementation question
        use_reranking: Enable Cohere reranking for better precision (legacy)
        reranker_model: Reranker model to use (default: "cohere")
        use_ensemble: Enable ensemble retrieval (Vector + BM25 + Cohere) [Task 6]
        
    Returns:
        Dict with implementation_plan and sources
    """
    logger.info(f"🚀 Starting agentic RAG for: '{question}'")
    
    # ✅ Step 1: Check if question is relevant to security/IT
    is_relevant, reason = check_question_relevance(question)
    
    if not is_relevant:
        logger.warning(f"❌ Question rejected as out-of-scope: {reason}")
        return {
            "answer": f"""# ⚠️ Out of Scope Question

I'm a **Security Maturity Assistant** specialized in:
- 🔒 Cybersecurity best practices
- 🖥️ IT infrastructure hardening  
- ⚙️ Technology configuration (Windows, Linux, cloud, networks)
- 📋 Security frameworks (CIS Controls, NIST, OWASP, CSA)

**Your question appears to be about:** {reason}

### 💡 Try asking me things like:
- "How to harden a Windows Server?"
- "Best practices for securing Ubuntu Linux?"
- "How to configure MFA for Microsoft 365?"
- "Cisco router baseline security configuration"
- "How to secure AWS S3 buckets?"

Please ask a security or IT-related question, and I'll provide you with a detailed, actionable implementation guide!
""",
            "sources": [],
            "used_web_search": False
        }
    
    # ✅ Step 2: Question is relevant, proceed with RAG
    logger.info("✅ Question is relevant to security/IT - proceeding with RAG")
    
    # Create graph
    app = create_agent_graph()
    
    # Initialize state
    initial_state = {
        "question": question,
        "iso_requirements": "",
        "research_results": "",
        "implementation_plan": "",
        "sources": [],
        "used_web_search": False,
        "error": "",
        # Advanced retrieval settings
        "use_reranking": use_reranking,
        "reranker_model": reranker_model,
        "use_ensemble": use_ensemble
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
        ],
        "used_web_search": final_state.get("used_web_search", False)
    }

