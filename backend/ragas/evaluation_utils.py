"""
Reusable evaluation utilities for RAGAS assessment.

This module provides simple functions to:
1. Run RAG pipeline on test datasets
2. Evaluate with RAGAS metrics
3. Display and compare results

Usage:
    from evaluation_utils import run_rag_on_dataset, evaluate_rag_dataset, display_results_table
    
    # Run RAG on your test data
    df_with_outputs = run_rag_on_dataset(df, rag_pipeline)
    
    # Evaluate with RAGAS
    results = evaluate_rag_dataset(df_with_outputs, evaluator_llm)
    
    # Display results
    display_results_table(results, name="Baseline")
"""

import time
import pandas as pd
from typing import List, Optional
from tqdm import tqdm


class ResultsWrapper:
    """
    Wrapper for loading RAGAS results from CSV files.
    Provides a consistent interface with RAGAS result objects.
    """
    def __init__(self, csv_file_or_df):
        """
        Initialize ResultsWrapper with either a CSV file path or DataFrame.
        
        Args:
            csv_file_or_df: Either a path to CSV file (str) or a pandas DataFrame
        """
        if isinstance(csv_file_or_df, str):
            self.df = pd.read_csv(csv_file_or_df)
        else:
            self.df = csv_file_or_df
    
    def to_pandas(self):
        """Return the underlying DataFrame."""
        return self.df


def run_rag_on_dataset(
    df: pd.DataFrame, 
    rag_pipeline, 
    batch_size: Optional[int] = None,
    delay_seconds: float = 1.0
) -> pd.DataFrame:
    """
    Run RAG pipeline on all questions in the dataset.
    
    Args:
        df: DataFrame with 'user_input' column containing questions
        rag_pipeline: Your RAG pipeline instance (must have .query() method)
        batch_size: If provided, only process first N questions (for testing)
        delay_seconds: Delay between requests to avoid rate limiting
        
    Returns:
        DataFrame with added columns:
            - 'response': RAG generated answers
            - 'retrieved_contexts': RAG retrieved document chunks
    """
    print(f"🚀 Running RAG pipeline on dataset...")
    
    # Make a copy to avoid modifying original
    df_result = df.copy()
    
    # Limit batch size if specified
    if batch_size:
        df_result = df_result.head(batch_size)
        print(f"⚠️ Processing only first {batch_size} questions (test mode)")
    
    # Storage for results
    responses = []
    retrieved_contexts_list = []
    
    print(f"Processing {len(df_result)} questions...")
    print("⏳ This may take a while due to agentic workflow + potential web searches\n")
    
    # Process each question
    for idx, row in tqdm(df_result.iterrows(), total=len(df_result), desc="RAG Pipeline"):
        question = row['user_input']
        
        try:
            # Call RAG pipeline
            result = rag_pipeline.query(question, return_sources=True)
            
            # Extract response (answer)
            response = result.get('answer', '')
            
            # Extract retrieved contexts (sources)
            sources = result.get('sources', [])
            retrieved_contexts = [
                source['content'] if isinstance(source, dict) else source.page_content 
                for source in sources
            ]
            
            responses.append(response)
            retrieved_contexts_list.append(retrieved_contexts)
            
            # Delay to avoid rate limiting
            time.sleep(delay_seconds)
            
        except Exception as e:
            print(f"\n❌ Error on question {idx}: {e}")
            responses.append("")
            retrieved_contexts_list.append([])
    
    # Add results to dataframe
    df_result['response'] = responses
    df_result['retrieved_contexts'] = retrieved_contexts_list
    
    # Summary
    valid_responses = sum(1 for r in responses if r)
    print(f"\n✅ Completed: {valid_responses}/{len(df_result)} successful queries")
    
    return df_result


def evaluate_rag_dataset(
    df: pd.DataFrame,
    evaluator_llm,
    metrics: Optional[List] = None,
    timeout: int = 600,
    max_workers: int = 4
) -> object:
    """
    Run RAGAS evaluation on dataset with RAG outputs.
    
    Args:
        df: DataFrame with columns:
            - user_input: questions
            - reference_contexts: ground truth contexts
            - reference: ground truth answers
            - response: RAG generated answers (from run_rag_on_dataset)
            - retrieved_contexts: RAG retrieved contexts (from run_rag_on_dataset)
        evaluator_llm: RAGAS LLM wrapper for evaluation
        metrics: List of RAGAS metric instances. If None, uses default set.
        timeout: Timeout for evaluation in seconds
        max_workers: Number of parallel workers
        
    Returns:
        RAGAS evaluation results object
    """
    from ragas import evaluate, EvaluationDataset, RunConfig
    from ragas.metrics import (
        Faithfulness, 
        ResponseRelevancy, 
        FactualCorrectness, 
        ContextPrecision, 
        ContextRecall
    )
    import ast
    
    print(f"📊 Preparing dataset for RAGAS evaluation...")
    
    # Make a copy
    df_eval = df.copy()
    
    # Convert string representations of lists to actual lists if needed
    if 'reference_contexts' in df_eval.columns:
        if isinstance(df_eval['reference_contexts'].iloc[0], str):
            df_eval['reference_contexts'] = df_eval['reference_contexts'].apply(ast.literal_eval)
    
    # Create RAGAS evaluation dataset
    evaluation_dataset = EvaluationDataset.from_pandas(df_eval)
    
    print(f"Dataset features: {evaluation_dataset.features()}")
    print(f"Number of samples: {len(evaluation_dataset)}")
    
    # Use default metrics if none provided
    if metrics is None:
        metrics = [
            Faithfulness(),
            ResponseRelevancy(),
            FactualCorrectness(),
            ContextPrecision(),
            ContextRecall()
        ]
    
    # Configure evaluation
    run_config = RunConfig(
        timeout=timeout,
        max_workers=max_workers
    )
    
    print(f"\n🚀 Starting RAGAS evaluation with metrics:")
    for metric in metrics:
        print(f"   - {metric.name}")
    print()
    
    # Run evaluation
    results = evaluate(
        dataset=evaluation_dataset,
        metrics=metrics,
        llm=evaluator_llm,
        run_config=run_config
    )
    
    print("✅ Evaluation complete!")
    
    return results


def display_results_table(results, name: str = "Results") -> pd.DataFrame:
    """
    Display RAGAS evaluation results as a nice table.
    
    Args:
        results: RAGAS evaluation results object
        name: Name for this evaluation (e.g., "Baseline", "Advanced Retrieval")
        
    Returns:
        Summary DataFrame with average scores
    """
    print(f"\n{'='*60}")
    print(f"📊 {name} - RAGAS Evaluation Results")
    print(f"{'='*60}\n")
    
    # Convert to DataFrame
    results_df = results.to_pandas()
    
    # Define metric columns
    metric_columns = [
        'faithfulness', 
        'answer_relevancy',  # ResponseRelevancy metric outputs as 'answer_relevancy' 
        'factual_correctness', 
        'context_precision', 
        'context_recall'
    ]
    
    # Filter to only metrics that exist
    available_metrics = [col for col in metric_columns if col in results_df.columns]
    
    # Calculate summary statistics
    summary = pd.DataFrame({
        'Metric': available_metrics,
        'Average': [results_df[m].mean() for m in available_metrics],
        'Std Dev': [results_df[m].std() for m in available_metrics],
        'Min': [results_df[m].min() for m in available_metrics],
        'Max': [results_df[m].max() for m in available_metrics]
    })
    
    # Display summary
    print("📈 Summary Statistics:")
    print(summary.to_string(index=False))
    print()
    
    # Display average scores more prominently
    print("🎯 Average Scores:")
    for metric in available_metrics:
        score = results_df[metric].mean()
        print(f"   {metric:.<30} {score:.4f}")
    
    print(f"\n{'='*60}\n")
    
    return summary


def compare_evaluations(
    baseline_results, 
    advanced_results, 
    baseline_name: str = "Baseline",
    advanced_name: str = "Advanced"
) -> pd.DataFrame:
    """
    Compare two RAGAS evaluation results side-by-side.
    
    Args:
        baseline_results: RAGAS results from baseline system
        advanced_results: RAGAS results from improved system
        baseline_name: Name for baseline system
        advanced_name: Name for advanced system
        
    Returns:
        Comparison DataFrame with improvements
    """
    print(f"\n{'='*60}")
    print(f"📊 Comparison: {baseline_name} vs {advanced_name}")
    print(f"{'='*60}\n")
    
    # Convert to DataFrames
    baseline_df = baseline_results.to_pandas()
    advanced_df = advanced_results.to_pandas()
    
    # Define metric columns
    metric_columns = [
        'faithfulness', 
        'answer_relevancy',  # ResponseRelevancy metric outputs as 'answer_relevancy' 
        'factual_correctness', 
        'context_precision', 
        'context_recall'
    ]
    
    # Filter to only metrics that exist in both
    available_metrics = [
        col for col in metric_columns 
        if col in baseline_df.columns and col in advanced_df.columns
    ]
    
    # Calculate comparison
    comparison = pd.DataFrame({
        'Metric': available_metrics,
        baseline_name: [baseline_df[m].mean() for m in available_metrics],
        advanced_name: [advanced_df[m].mean() for m in available_metrics]
    })
    
    # Calculate improvement
    comparison['Absolute Δ'] = comparison[advanced_name] - comparison[baseline_name]
    comparison['Relative Δ (%)'] = (
        (comparison[advanced_name] - comparison[baseline_name]) / comparison[baseline_name] * 100
    )
    
    # Display comparison
    print(comparison.to_string(index=False))
    print()
    
    # Summary
    avg_improvement = comparison['Relative Δ (%)'].mean()
    if avg_improvement > 0:
        print(f"✅ Overall improvement: {avg_improvement:.2f}%")
    else:
        print(f"⚠️ Overall change: {avg_improvement:.2f}%")
    
    print(f"\n{'='*60}\n")
    
    return comparison


def save_results(results, df_with_outputs, output_prefix: str = "evaluation"):
    """
    Save evaluation results and dataset with outputs to files.
    
    Args:
        results: RAGAS evaluation results
        df_with_outputs: DataFrame with RAG outputs and scores
        output_prefix: Prefix for output files
    """
    import os
    from datetime import datetime
    from pathlib import Path
    
    # Create results directory if it doesn't exist
    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)
    
    # Add timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save results DataFrame
    results_df = results.to_pandas()
    results_filename = results_dir / f"{output_prefix}_results_{timestamp}.csv"
    results_df.to_csv(results_filename, index=False)
    print(f"✅ Saved results to: {results_filename}")
    
    # Save full dataset with outputs
    dataset_filename = results_dir / f"{output_prefix}_dataset_{timestamp}.csv"
    df_with_outputs.to_csv(dataset_filename, index=False)
    print(f"✅ Saved dataset to: {dataset_filename}")
    
    return str(results_filename), str(dataset_filename)

