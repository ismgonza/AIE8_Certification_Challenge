# RAGAS Evaluation Guide

## 📂 Files Overview

### 1. `evaluation_utils.py`
Reusable functions for running evaluations:
- `run_rag_on_dataset()` - Runs RAG pipeline on test questions
- `evaluate_rag_dataset()` - Runs RAGAS evaluation with metrics
- `display_results_table()` - Displays results in a formatted table
- `compare_evaluations()` - Compares baseline vs advanced performance
- `save_results()` - Saves evaluation results to CSV

### 2. `02_evaluations.ipynb`
Complete evaluation notebook for Tasks 5, 6, and 7:
1. Load golden dataset (`golden_test_data.csv`)
2. **Baseline Evaluation** - Naive Agentic RAG
3. **Advanced Evaluation** - With Ensemble Retrieval (Vector + BM25 + Cohere)
4. **Comparison** - Side-by-side performance metrics

### 3. `01_generate_synthetic_data.ipynb`
Generates synthetic test data using RAGAS (already completed)

---

## 🚀 How to Run Complete Evaluation

### Step 1: Start Qdrant (if needed)
```bash
cd docker
docker-compose up -d
```

### Step 2: Open Jupyter Notebook
```bash
cd ragas
jupyter notebook 02_evaluations.ipynb
```

### Step 3: Run All Cells
The notebook is organized into clear sections:
1. **Setup** - Load dependencies and dataset
2. **Baseline** - Run naive agentic RAG (top_k=3)
3. **Advanced** - Run with ensemble retrieval (Vector + BM25 + Cohere)
4. **Comparison** - Compare both approaches

---

## ⚙️ Current Configuration

### Baseline (Naive Agentic RAG)
```python
rag = RAGPipeline(
    top_k=3,          # Retrieve top 3 documents
    use_tavily=True,  # Web search for implementation examples
    use_agents=True   # Multi-agent LangGraph workflow
)
```

**Retrieval Process:**
- Vector search retrieves **3 documents**
- No reranking applied

### Advanced (With Ensemble Retrieval)
```python
rag_advanced = RAGPipeline(
    top_k=3,           # Final output: 3 documents
    use_tavily=True,   # Web search enabled
    use_agents=True,   # Multi-agent workflow
    use_ensemble=True  # ✨ Ensemble retrieval
)
```

**Retrieval Process:**
- Vector search retrieves **15 documents** (semantic)
- BM25 retrieves **15 documents** (keyword matching)
- Cohere reranks vector results **15 → 7** (precision filter)
- Reciprocal rank fusion combines all three streams
- Ensemble selects best **3 documents** from merged results

---

## 📊 RAGAS Metrics Evaluated

| Metric | What it Measures | Good Score |
|--------|-----------------|------------|
| **Faithfulness** | Response grounded in retrieved context (no hallucinations) | > 0.7 |
| **Response Relevancy** | Response relevance to the question | > 0.7 |
| **Factual Correctness** | Response matches reference answer | > 0.6 |
| **Context Precision** | Retrieved contexts are relevant | > 0.6 |
| **Context Recall** | All necessary contexts retrieved | > 0.6 |

---

## 📈 Expected Outputs

### Task 5 Deliverable: Baseline Results Table
```
====================================================================
📊 Baseline (Naive Agentic RAG) - RAGAS Evaluation Results
====================================================================

📈 Summary Statistics:
Metric                    Average    Std Dev      Min      Max
faithfulness                0.XXX      0.XXX    0.XXX    0.XXX
response_relevancy          0.XXX      0.XXX    0.XXX    0.XXX
factual_correctness         0.XXX      0.XXX    0.XXX    0.XXX
context_precision           0.XXX      0.XXX    0.XXX    0.XXX
context_recall              0.XXX      0.XXX    0.XXX    0.XXX
====================================================================
```

### Task 7 Deliverable: Comparison Table
```
====================================================================
📊 RAGAS Evaluation Comparison
====================================================================

                           Baseline    Advanced    Improvement
Faithfulness                  0.XXX       0.XXX        +X.XX%
Response Relevancy            0.XXX       0.XXX        +X.XX%
Factual Correctness           0.XXX       0.XXX        +X.XX%
Context Precision             0.XXX       0.XXX        +X.XX%
Context Recall                0.XXX       0.XXX        +X.XX%
====================================================================
```

---

## 🔄 Comparing Results (Without Re-running)

If you've already saved results and want to compare them:

```python
# Load saved results
from evaluation_utils import ResultsWrapper
import pandas as pd

# Load baseline (files are in results/ folder)
baseline_df = pd.read_csv("results/baseline_results_TIMESTAMP.csv")
baseline_results = ResultsWrapper(baseline_df)

# Load advanced
advanced_df = pd.read_csv("results/advanced_results_TIMESTAMP.csv")
advanced_results = ResultsWrapper(advanced_df)

# Compare
from evaluation_utils import compare_evaluations
comparison = compare_evaluations(
    baseline_results,
    advanced_results,
    baseline_name="Baseline (Naive)",
    advanced_name="Advanced (Ensemble)"
)
comparison
```

---

## ⚠️ Important Tips

### Before Running
1. ✅ Ensure Qdrant is running (`docker-compose up -d`)
2. ✅ Verify documents are ingested (check collection has vectors)
3. ✅ Set API keys in `.env` (OPENAI_API_KEY, COHERE_API_KEY, TAVILY_API_KEY)
4. ✅ Update `settings.py` if you want different defaults

### During Evaluation
- **Time**: Full 60-question run takes 15-30 minutes
- **Cost**: Approximately $2-5 in API costs (OpenAI + Cohere + Tavily)
- **Progress**: Watch the progress bar, don't interrupt
- **Rate Limits**: Built-in delays prevent API throttling

### After Running
- 📁 Results saved to `results/` folder with timestamps
- 📊 Both individual and comparison tables displayed
- 🔄 Can re-compare results without re-running evaluation

---

## 🐛 Troubleshooting

**Error: "Column 'retrieved_contexts' not found"**
→ Run `run_rag_on_dataset()` first to generate RAG outputs before evaluation

**Error: Rate limit exceeded**
→ Increase `delay_seconds` parameter in `run_rag_on_dataset()` (try 2.0 or 3.0)

**Error: Qdrant connection failed**
→ Start Qdrant: `cd docker && docker-compose up -d`

**Error: No documents in collection**
→ Run document ingestion: `cd .. && python utils/vector_store.py`

**Evaluation hangs or takes too long**
→ Reduce `max_workers` in `RunConfig` from 4 to 2

**Cohere API key error**
→ Add `COHERE_API_KEY` to `.env` file

---

## 🎯 Task Completion Checklist

### ✅ Task 5: Golden Test Data Set & Baseline Evaluation
- [x] Generate golden dataset (`01_generate_synthetic_data.ipynb`)
- [x] Run baseline RAG on all 60 questions
- [x] Evaluate with RAGAS framework
- [x] Display results table

### ✅ Task 6: Advanced Retrieval Implementation
- [x] Implement ensemble retrieval (Vector + BM25 + Cohere)
- [x] Integrate into RAG pipeline
- [x] Document rationale and architecture

### ✅ Task 7: Performance Assessment
- [x] Run advanced retrieval evaluation
- [x] Compare baseline vs advanced
- [x] Generate comparison table
- [x] Save results for reporting

---

## 📞 Quick Reference Commands

```python
# Import utilities
from evaluation_utils import (
    run_rag_on_dataset,
    evaluate_rag_dataset, 
    display_results_table,
    compare_evaluations,
    save_results,
    ResultsWrapper
)

# Run RAG on dataset
df_with_outputs = run_rag_on_dataset(
    df=df,
    rag_pipeline=rag,
    batch_size=None,      # None = all questions
    delay_seconds=1.0
)

# Evaluate with RAGAS
results = evaluate_rag_dataset(
    df=df_with_outputs,
    evaluator_llm=evaluator_llm
)

# Display results
summary_table = display_results_table(
    results,
    name="Baseline (Naive Agentic RAG)"
)

# Save results
results_file, dataset_file = save_results(
    results,
    df_with_outputs,
    output_prefix="baseline"
)

# Compare two evaluations
comparison = compare_evaluations(
    baseline_results,
    advanced_results,
    baseline_name="Baseline (Naive)",
    advanced_name="Advanced (Ensemble)"
)
```

---

## 📚 Additional Resources

- **Advanced Retrieval Details**: See `../ADVANCED_RETRIEVAL.md`
- **Task 6 Summary**: See `../TASK_6_SUMMARY.md`
- **Main Project README**: See `../README.md`

---

## 🎓 Key Learnings

1. **Agentic RAG is Already Sophisticated**: The baseline uses multi-agent workflow with web search
2. **Ensemble Retrieval Adds Value**: Combining semantic, lexical, and precision approaches improves results
3. **BM25 Complements Embeddings**: Catches exact keywords that semantic search might miss
4. **Evaluation is Reusable**: Save results to compare without re-running expensive evaluations
5. **Fair Comparisons Matter**: Both configurations return same number of docs (3) for fair comparison

---

**Ready to run evaluation?** Open `02_evaluations.ipynb` and execute all cells! 🚀

