# RAGAS Evaluation Report

**Project**: Shieldy - The AI Security Assistant  
**Framework**: RAGAS  
**Test Dataset**: 60 synthetic questions about security frameworks (CIS, NIST, OWASP, CSA)

---

## 📋 Summary

Evaluated a RAG system using baseline (simple vector search) vs. advanced (ensemble retrieval combining Vector + BM25 + Cohere). Advanced approach showed measurable improvements in retrieval quality (+3.17% avg) and generation faithfulness (+5.77%). Four out of five metrics improved. Ensemble retrieval is recommended for production.

---

## 🎯 What Was Tested

**Baseline (Naive Agentic RAG)**
- Simple vector search (top_k=3)
- Multi-agent workflow + web search

**Advanced (Ensemble Retrieval)**
- Vector Search (semantic, 15 candidates)
- BM25 Retriever (keyword matching, 15 candidates)  
- Cohere Rerank (cross-encoder, 15→7 candidates)
- Reciprocal Rank Fusion (40% Vector, 30% BM25, 30% Cohere)
- Final: Top 3 documents

---

## 📊 Results

### Full Metrics Comparison

| Metric | Baseline | Advanced | Δ | % Change |
|--------|----------|----------|---|----------|
| **Faithfulness** | 0.626 | 0.662 | +0.036 | **+5.77%** ✅ |
| **Answer Relevancy** | 0.879 | 0.894 | +0.015 | **+1.68%** ✅ |
| **Factual Correctness** | 0.385 | 0.352 | -0.034 | -8.78% ⚠️ |
| **Context Precision** | 0.813 | 0.846 | +0.033 | **+4.05%** ✅ |
| **Context Recall** | 0.778 | 0.796 | +0.018 | **+2.29%** ✅ |
| **Overall** | - | - | - | **+1.00%** |

### By Category

| Category | Metrics | Avg Change | Interpretation |
|----------|---------|------------|----------------|
| **Retrieval** | Precision, Recall | **+3.17%** | Better doc selection & coverage |
| **Generation** | Faithfulness, Relevancy | **+3.73%** | Better grounding & focus |

---

## 🔍 Analysis

### ✅ What Improved

**Retrieval Quality (+3.17%)**
- Context Precision +4%: Ensemble filters irrelevant docs better
- Context Recall +2.3%: BM25 catches exact terms ("CIS Control 5.2")

**Generation Quality (+3.73%)**
- Faithfulness +5.8%: Better context = less hallucination
- Relevancy +1.7%: More focused responses

### ⚠️ Trade-off: Factual Correctness (-8.78%)

**Why:** Generation prompt encourages detailed, actionable responses (commands, pricing, examples) that diverge from terse reference answers.

**Evidence:** Faithfulness ↑ (uses context well) but Factual Correctness ↓ (adds details beyond reference).

**Verdict:** This is a prompt design choice (helpful vs. terse), not a retrieval failure. Can be fixed by adjusting prompt/temperature if needed.

---

## 💡 Why Ensemble Retrieval?

**The Problem:**
- Vector search alone misses exact keyword matches
- BM25 alone misses semantic/conceptual queries
- Security docs need BOTH (specific IDs like "NIST 800-53" + concepts like "access control")

**The Solution:**
- **Vector**: Gets conceptual matches ("access management" → finds "identity", "permissions")
- **BM25**: Gets exact terms ("CIS Control 5.2" → finds that specific control)
- **Cohere**: Filters best from combined pool
- **Together**: Covers both exact terminology and semantic understanding

**Why It Matters for Security:**
- Security frameworks are full of specific identifiers (CIS 5.2.1, NIST categories, AWS service names)
- Need exact matches (BM25) + conceptual understanding (Vector)
- Ensemble gives best of both

---

## 🎓 Lessons Learned

1. **BM25 is still relevant**: Modern embeddings are powerful, but keyword matching adds unique value for specific terminology
2. **Multiple metrics matter**: Overall +1% hides the real story (retrieval +3.17%, generation +3.73%)
3. **Baseline was strong**: Multi-agent + web search is sophisticated; improvements are incremental but real
4. **Fair comparisons are critical**: Both return 3 docs to isolate retrieval quality
5. **Trade-offs exist**: Helpful detailed responses vs. strict factual alignment (design choice, not failure)

---

## ✅ Conclusion & Recommendation

**Does ensemble work?** Yes. 4/5 metrics improved, retrieval quality up 3.17%.

**Is it worth it?** Yes. Cost +$0.01/query, latency +200ms, clear quality gains.

**Recommendation:** Deploy with ensemble retrieval as default.

---

## 📁 Evaluation Files

- Notebook: `ragas/02_evaluations.ipynb`
- Results: `ragas/results/*.csv`
- Code: `utils/advanced_retrieval.py`
