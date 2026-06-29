PROMPT_V0 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPRi knockdown of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section.

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:"""


PROMPT_V1 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPRi knockdown of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section. Use the structured framework below to guide your analysis. You do not need to answer every question — use whichever are relevant to reach a well-justified conclusion.

─────────────────────────────────────────────────────────────────────────────
REASONING FRAMEWORK
─────────────────────────────────────────────────────────────────────────────

PHASE 1 — PRIMITIVE IDENTITY (What are these genes?)

  1.1 Functional Classification
      What is the primary biochemical class of {pert} and {gene}?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of {pert} and {gene} reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do {pert} and {gene} proteins physically assemble into a complex?
      If yes, is {gene} dependent on {pert} for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does {pert} directly regulate transcription of {gene}?
      (Is {pert} a known TF/co-factor that binds the {gene} promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are {pert} and {gene} in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of {pert} affect {gene}?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does {pert} directly activate or repress {gene} expression?
      Knocking down {pert} — does it remove a known activator or a known repressor of {gene}?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is {pert} upstream of {gene} in a defined signaling pathway?
      Does loss of {pert} block a phosphorylation/activation event required to regulate {gene}?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of {pert} trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter {gene} expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of {pert}?
      Could loss of {pert} lead to upregulation of {gene} as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are {pert} and {gene} protein products members of the same complex?
      If {pert} is knocked down, does {gene} protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are {pert} and {gene} in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes the relationship:

  [ 1. Direct Edge ]     — {pert} directly controls {gene}
  [ 2. Indirect Path ]   — {pert} affects {gene} through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches {gene}
  [ 4. Null Topology ]   — no meaningful functional link exists

─────────────────────────────────────────────────────────────────────────────

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:"""


PROMPT_V3 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Think step by step using the two-stage reasoning below.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 1 — Is there any effect?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

If you knockdown {pert} using CRISPRi, does the expression of {gene} change at all?

  A) Knockdown of {pert} does NOT impact the expression of {gene}.
  B) Knockdown of {pert} results in differential expression of {gene}.

→ If your Stage 1 answer is A, your final output is C (no significant effect). Stop here.
→ If your Stage 1 answer is B, continue to Stage 2.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STAGE 2 — In which direction? (only if Stage 1 = B)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Given that knockdown of {pert} does affect {gene}, in which direction does {gene} change?

  A) {gene} is up-regulated.
  B) {gene} is down-regulated.

→ If your Stage 2 answer is A, your final output is A (up-regulated).
→ If your Stage 2 answer is B, your final output is B (down-regulated).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A  → up-regulated
B  → down-regulated
C  → no significant effect

Reasoning:

Final output:"""


PROMPT_V4 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) were differentiated from bone marrow precursors of Cas9-transgenic mice using M-CSF. Cells were transduced with a pooled CRISPR knockout library targeting genes involved in inflammatory signaling and macrophage-relevant processes. Cells were then stimulated with bacterial lipopolysaccharide (LPS) to induce an inflammatory immune response, and single-cell RNA-seq profiles were collected 9 hours after LPS stimulation.

A gene is considered differentially expressed if it meets both criteria:
  - Adjusted p-value (FDR) < 0.05
  - |shrunken log2 fold-change| >= log2(1.5)  (i.e., at least a ~1.5x change)

Predictions are relative to control cells carrying Olfactory receptor gene perturbations.

The following question is about a CRISPR knockout experiment in LPS-stimulated mouse bone marrow-derived macrophages (BMDMs) at 9 hours post-stimulation.

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section.

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:"""


PROMPT_V5 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors of Cas9-transgenic mice using M-CSF.

A gene is considered differentially expressed if it meets both criteria:
  - Adjusted p-value (FDR) < 0.05
  - |shrunken log2 fold-change| >= log2(1.5)  (i.e., at least a ~1.5x change)

Predictions are relative to control cells carrying Olfactory receptor gene perturbations.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section.

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:"""
