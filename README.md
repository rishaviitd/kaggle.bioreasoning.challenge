<p align="center">
  <img src="https://www.kaggle.com/competitions/139769/images/header" alt="BioReasoning Challenge overview" width="100%">
</p>

<h1 align="center">
  <a href="https://genentech.github.io/BioReasoningChallenge/" style="text-decoration: none; color: inherit;">MLGenX Bio Reasoning Challenge ↗️</a>
</h1>

<p align="justify">
  Predicting gene expression changes from CRISPRi perturbations in mouse bone marrow-derived macrophages (BMDMs) using DSPy-optimized prompts and fine-tuned LLMs.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Kaggle-20BEFF?logo=Kaggle&logoColor=white" alt="Kaggle">
  <img src="https://img.shields.io/badge/OpenAI-412991?logo=openai&logoColor=white" alt="OpenAI">
</p>

## Project Highlights

| Track | Stack | Purpose |
|---|---|---|
| **Track A: Prompt Optimization** | <img src="https://storage.googleapis.com/lightning-avatars/litpages/01hsbt485wd2m6xgwhsh8xw26j/3c7af255-9b22-4d05-b476-d105c32acfd2.png" height="20" align="top"> DSPy, GEPA, GPT-OSS-120B | Automatically optimize the biological reasoning instructions for a 120B parameter model using Generative Error-driven Prompt Adaptation (GEPA). |
| **Track C: Fine-Tuning** | <img src="https://r2.madebyagents.com/qwen.webp" height="20" align="top"> Qwen 3.5 9B | Fine-tune a compact (<10B) open-weights LLM to intrinsically learn the causal gene networks without relying on complex runtime prompts. |

## Overview

Participants are given (perturbation, gene) pairs and must predict a **ternary** effect on the target gene: `up`, `down`, or `none`. 

Submissions provide two probabilities per row: `prediction_up` and `prediction_down` (where `P(none) = 1 - P(up) - P(down)`). Models are evaluated using the average of Differential Expression (DE) AUROC and Direction (DIR) AUROC against ground-truth CRISPRi labels.

## Track A: Prompt Optimization Architecture

To maximize the zero-shot capabilities of the 120B parameter model, we use an automated prompt optimization loop (GEPA) that iteratively improves the biological reasoning instructions.

```mermaid
flowchart TD
    EVAL["Evaluate Baseline Prompt<br/>(Student: 120B)"] --> METRIC{"Compare to Ground Truth"}
    METRIC -->|"Correct"| PASS["Skip Feedback"]
    METRIC -->|"Incorrect"| TEACHER["Teacher Critique<br/>(Teacher: 20B)"]
    TEACHER --> FLAW["Prediction Flaw Analysis<br/>(Probability math check)"]
    FLAW --> REFLECT["Reflection LLM<br/>(120B)"]
    REFLECT -->|"Rewrites rules based on systemic failures"| NEW_PROMPT["New Optimized Prompt"]
    NEW_PROMPT --> EVAL
    
    classDef model fill:#eef2ff,stroke:#6366f1,color:#1e293b;
    classDef logic fill:#fef9c3,stroke:#eab308,color:#1e293b;
    classDef fallback fill:#ffedd5,stroke:#f97316,color:#1e293b;
    
    class EVAL,TEACHER,REFLECT model;
    class METRIC,FLAW,PASS logic;
```

* **Student Model (120B):** Generates biological reasoning traces and raw log-probabilities for the final ternary decision.
* **Teacher Model (20B):** Analyzes the student's failures and writes a mechanistic critique of what biological pathway was missed.
* **Reflection Engine:** Synthesizes the teacher's critiques and the probability math to surgically rewrite the seed instructions to prevent future hallucinations.
