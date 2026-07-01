Task Context:

In this challenge, participants tackle the focused but scientifically meaningful task of predicting the outcome of a Perturb-seq experiment: given a knockout of gene X, predict whether a target gene Y will be up-regulated, down-regulated, or unchanged in activated macrophages.

This framing turns perturbation biology into a benchmark for machine reasoning: can an AI system combine biological knowledge, causal intuition, and structured inference to anticipate the downstream effects of intervention?

The core task is a supervised predictive challenge where participants must infer the effect of a specific gene perturbation on the expression of a target gene. Structurally, the task is defined as: Perturbation gene X → gene Y up/down/no-change. Participants will be scored based on their prediction of these post-processed labels, which indicate whether gene Y is up-regulated, down-regulated, or unchanged following the perturbation of gene X.

Label definitions:

up: The target gene is significantly upregulated (FDR < 5%, logFC >= log2(1.5)).
down: The target gene is significantly downregulated (FDR < 5%, logFC <= -log2(1.5)).
none: The target gene is not significantly differentially expressed (does not meet the criteria above).

constraints:

Given a fixed LLM with no finetuning, provide a prompt which will encourage the model to give the best result.

Fixed base LLM: GPT-OSS-120B
No tools, single call
3 samples per question (seeds 42, 43, 44)
Max 4,096 prompt tokens

Data Context:

The data consists of a set of ternary questions regarding the genetic perturbation effects in macrophage cells.

Biological background
This dataset contains gene expression profiles from primary mouse bone marrow-derived macrophages (BMDMs), which are innate immune cells differentiated from bone marrow cells isolated from Cas9-transgenic mice. The cells were transduced with a pooled CRISPR knockout library targeting genes involved in inflammatory signaling and other macrophage-relevant processes, then stimulated with bacterial lipopolysaccharide (LPS) to induce an immune response. Nine hours after stimulation, single-cell RNA profiles were collected together with perturbation identities, enabling analysis of how specific gene knockouts (perturbation) alter macrophage transcriptional states during inflammation.

Preprocessing
Differential expression analysis was performed on the top 10,000 highly variable features selected by scanpy. For each perturbation, we used glmGamPoi to fit a negative binomial regression comparing the perturbed cells against 2,000 random cells containing control perturbations (Olfactory receptor genes), while controlling for batch as a covariate. Each of the 4 guides per gene were pooled and counted as a single perturbation for this analysis. We performed shrinkage on the log-fold-changes by applying ebnm to the flattened log-fold-change matrix, assuming a point-normal prior. To assess false positive rates of the differential expression results, we generated 500 artificial perturbations by sampling random quartets of Olfactory receptor genes. Defining differential expressed genes (DEGs) using cutoffs of 5% FDR and |shrunken log2FC| ≥ log2(1.5), 471 (of 500) artificial perturbations had 0 DEGs, while 25 artificial perturbations had 1 DEG, and 4 had 2 DEGs. By contrast, the true perturbations had a median of 193 DEGs (IQR 56–516.5 DEGs).

Following the differential expression analysis, we processed the data similarly to the PerturbQA format, except with ternary labels. Differential expressed genes were determined as genes with FDR < 0.05 and |shrunken log2FC| ≥ log2(1.5). Perturbations with less than 9 differentially expressed genes (DEGs) were excluded, and then remaining perturbations were separated into 80% train, 10% val, 10% test splits. The full 10,000 possible target genes are partitioned to be used in different splits with 60% train / 20% val / 20% test. For each perturbation, up to 9 of the top DEGs are added to the dataset. A similar number of non-DEGs are then added using a negative sampling strategy to ensure the dataset is balanced. There are 482 perturbations and 2,206 target genes in total with 386/48/48 perturbations and 1,570/331/305 target genes belonging to the final train / val / test splits, respectively.

Useful Context
Gene names follow mouse nomenclature (e.g., Aars, Actb, Stat1).
The cell type is mouse bone marrow-derived macrophages (BMDMs).
The perturbation mechanism is CRISPR (knockout).
Fold-change values are shrunken log2 fold-changes (not raw).
Sampling: For each perturbation, up to 9 of the top differentially expressed genes (DEGs) are added to the dataset, labeled up or down according to the sign of logFC. A similar number of non-DE genes are then added using a negative sampling strategy (labeled none) to keep the dataset balanced. 482 perturbations are retained (those with at least 9 DEGs).
