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


PROMPT_V6 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

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

─────────────────────────────────────────────────────────────────────────────

CRITICAL CALIBRATION RULES:
1. "No significant effect" (C) must only be chosen if the genes are biologically isolated (Null Topology) or if competing pathways perfectly cancel each other out. Do NOT use C as a "safe guess" if you are simply unsure about the direction of a known pathway.
2. Track the sign of regulation carefully:
   - Knocking down a POSITIVE regulator of a gene leads to DOWN-regulation (B).
   - Knocking down a NEGATIVE regulator (repressor) leads to UP-regulation (A).
3. Do not invent long, unproven pathways. If a pathway connection is highly speculative or weak, it is likely a Null Topology (C).

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:"""

PROMPT_V7 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

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




PROMPT_V9 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section.

CRITICAL REASONING GUIDELINES:
1. Balanced Confidence: Most random gene pairs in biology do not interact; "no significant effect" (C) is frequently the correct answer. However, if your step-by-step reasoning deduces a strong, biologically plausible mechanism (e.g., loss of a repressor leading to de-repression, or indirect pathway cross-talk), trust your logic and predict a directional change (A or B). Do not hedge and default to C just because you cannot recall literature confirming the exact pair.
2. Compensatory Upregulation: When a perturbation impairs a specific cellular function or organelle (e.g., lysosomal trafficking, oxidative phosphorylation, DNA repair), strongly consider that the cell may trigger compensatory transcriptional upregulation of related genes to overcome the defect, rather than downregulating them.
3. Systemic Responses: Recognize that gene expression changes are often driven by indirect, systemic cellular responses rather than direct transcription factor-target interactions. Explicitly consider broad pathways like ER stress, nucleolar stress, DNA damage response, and the unfolded protein response.
4. Meta-Reasoning: Base your prediction strictly on biological mechanisms and systems-level logic. Do NOT attempt to guess the intent of the exam or rely on typical test-taking heuristics. Treat this as a real biological system, not a multiple-choice test.
5. Uncharacterized Genes: When dealing with poorly characterized genes (e.g., those starting with Gm-, -Rik), do not automatically assume no significant effect. Consider the global effects of the perturbed gene on transcription or mRNA stability.

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:"""

PROMPT_V10 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Think step by step in the reasoning section. Base your prediction strictly on biological mechanisms and systems-level logic.

CRITICAL REASONING GUIDELINES:
1. Null Topology (C): Most random gene pairs in biology do not interact. If there is no plausible biological link between the genes (e.g. they operate in completely unrelated cellular compartments with no cross-talk), confidently predict C.
2. Compensatory Upregulation (A): When a perturbation impairs a specific cellular function or organelle, the cell often triggers compensatory transcriptional upregulation of related genes to overcome the defect.
3. De-repression (A): Loss of a transcriptional repressor or insulator leads to UP-regulation of its targets.
4. Loss of Activator (B): Loss of a positive transcriptional regulator or required upstream signaling kinase leads to DOWN-regulation.
5. Systemic Stress Responses: Explicitly consider broad pathways like ER stress, nucleolar stress, and DNA damage response.

EXAMPLES:

--- Example 1 ---
Perturbation: Ctcf
Gene of interest: Fgd2
Predict the effect of CRISPR knockout of Ctcf on Fgd2:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Ctcf is a CCCTC-binding factor that acts as a transcriptional regulator and chromatin insulator. It often restricts gene expression by insulating genes from enhancer elements. Fgd2 encodes a guanine nucleotide exchange factor involved in actin cytoskeleton remodeling, which is expressed in macrophages. Because Ctcf often acts as a transcriptional repressor or insulator, the CRISPR knockout of Ctcf will lead to a loss of this insulation (de-repression). De-repression of the Fgd2 locus will allow enhancer activation. Therefore, the loss of this repressor strongly suggests that Fgd2 will be up-regulated.
Final output:
A

--- Example 2 ---
Perturbation: Vps33a
Gene of interest: Lipa
Predict the effect of CRISPR knockout of Vps33a on Lipa:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Vps33a is a core component of the HOPS complex, which is essential for lysosomal trafficking and fusion. Lipa encodes Lysosomal Acid Lipase A, a critical enzyme for lipid degradation inside the lysosome. Knocking out Vps33a will severely impair lysosomal function and trafficking. In response to lysosomal stress and dysfunction, macrophages typically activate the TFEB transcription factor (the master regulator of lysosomal biogenesis) as a compensatory mechanism. TFEB activation will trigger the compensatory upregulation of lysosomal enzymes, including Lipa, to overcome the functional defect. Therefore, Lipa will be up-regulated.
Final output:
A

--- Example 3 ---
Perturbation: Acin1
Gene of interest: Cotl1
Predict the effect of CRISPR knockout of Acin1 on Cotl1:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Acin1 (Apoptotic chromatin condensation inducer 1) is an RNA-binding protein involved in apoptosis and RNA processing in the nucleus. Cotl1 (Cortactin-like protein 1) is an actin-binding protein involved in cytoskeleton remodeling and cell motility in the cytoplasm. These two genes operate in completely different cellular compartments (nucleus vs. cytoskeleton) and serve entirely different functional roles (RNA processing vs. actin polymerization). There is no known direct regulatory relationship or obvious pathway cross-talk between them. Without a plausible systemic or direct link, this represents a Null Topology.
Final output:
C

--- Example 4 ---
Perturbation: Irf8
Gene of interest: Cd86
Predict the effect of CRISPR knockout of Irf8 on Cd86:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Irf8 (Interferon Regulatory Factor 8) is a critical, lineage-determining transcription factor in macrophages that drives the expression of pro-inflammatory and activation-related genes. Cd86 is a classic co-stimulatory molecule expressed on the surface of activated macrophages and dendritic cells. Irf8 is known to positively regulate the transcription of activation markers like Cd86. Knocking out Irf8 removes this essential positive transcriptional activator. Therefore, without Irf8 to drive its expression, Cd86 will be down-regulated.
Final output:
B
----------------

Now, answer the following:

Perturbation: {pert}
Gene of interest: {gene}
Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Reasoning:

Final output:"""

PROMPT_V11 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Think step by step in the reasoning section. Base your prediction strictly on biological mechanisms and systems-level logic.

CRITICAL REASONING GUIDELINES:
1. Null Topology (C): Most random gene pairs in biology do not interact. If there is no plausible biological link between the genes (e.g. they operate in completely unrelated cellular compartments with no cross-talk), confidently predict C.
2. Compensatory Upregulation (A): When a perturbation impairs a specific cellular function or organelle, the cell often triggers compensatory transcriptional upregulation of related genes to overcome the defect.
3. De-repression (A): Loss of a transcriptional repressor or insulator leads to UP-regulation of its targets.
4. Loss of Activator (B): Loss of a positive transcriptional regulator or required upstream signaling kinase leads to DOWN-regulation.
5. Systemic Stress Responses: Explicitly consider broad pathways like ER stress, nucleolar stress, and DNA damage response.

REAL-WORLD PERTURB-SEQ EXAMPLES IN MACROPHAGES:

--- Example 1 (Loss of Activator) ---
Perturbation: Spi1
Gene of interest: Tlr4
Predict the effect of CRISPR knockout of Spi1 on Tlr4:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Spi1 encodes the master transcription factor PU.1, which is essential for macrophage lineage determination and activation. Tlr4 is the primary receptor for LPS and a core component of the macrophage inflammatory response. PU.1 is known to directly bind and positively regulate the transcription of Tlr4 and the broader NF-kB signaling cascade. Knocking out the Spi1 (PU.1) master activator removes the positive transcriptional drive for these genes. Therefore, without its required activator, Tlr4 will be down-regulated.
Final output:
B

--- Example 2 (Loss of Pathway Regulator) ---
Perturbation: Gsk3b
Gene of interest: Ciita
Predict the effect of CRISPR knockout of Gsk3b on Ciita:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Gsk3b encodes Glycogen synthase kinase-3 beta, a central kinase involved in multiple signaling pathways including macrophage activation. Ciita is the master transactivator for MHC class II genes. In macrophages, the GSK3b pathway is required to positively regulate the expression of Ciita in response to inflammatory stimuli like IFN-g. Knocking out Gsk3b disrupts this essential upstream signaling cascade, preventing the proper activation of Ciita. Therefore, Ciita will be down-regulated.
Final output:
B

--- Example 3 (Null Topology) ---
Perturbation: Nop16
Gene of interest: Gbp8
Predict the effect of CRISPR knockout of Nop16 on Gbp8:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Nop16 is a nucleolar protein primarily involved in ribosome biogenesis and rRNA processing. Gbp8 is a Guanylate-binding protein involved in the interferon-driven immune response against intracellular pathogens in the cytoplasm. These two genes operate in entirely different subcellular compartments and biological modules (ribosome biogenesis vs. antiviral immunity). There is no known direct regulatory relationship or robust pathway cross-talk linking Nop16 to Gbp8. Without a clear mechanism, this is a Null Topology.
Final output:
C

--- Example 4 (Compensatory Upregulation / Stress) ---
Perturbation: Atg5
Gene of interest: Sqstm1
Predict the effect of CRISPR knockout of Atg5 on Sqstm1:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Atg5 is an essential core component of the autophagy machinery. Sqstm1 (p62) is an autophagy receptor that targets cargo for degradation and is itself degraded by autophagy. Knocking out Atg5 completely blocks autophagy, leading to the massive accumulation of undegraded proteins and cellular stress. In response to this profound autophagic stress, the cell activates compensatory transcriptional pathways (such as Nrf2) which heavily up-regulate the transcription of Sqstm1 to attempt to overcome the defect. Therefore, Sqstm1 will be up-regulated.
Final output:
A
----------------

Now, answer the following:

Perturbation: {pert}
Gene of interest: {gene}
Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Reasoning:

Final output:"""

PROMPT_V12 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section. Use the structured framework below to guide your analysis. You do not need to answer every question — use whichever are relevant to reach a well-justified conclusion.

─────────────────────────────────────────────────────────────────────────────
REASONING FRAMEWORK
─────────────────────────────────────────────────────────────────────────────

PHASE 1 — PRIMITIVE IDENTITY (What are these genes?)
  1.1 Functional Classification
  1.2 Subcellular Compartmentalization
  1.3 Tissue & Cell-Type Baseline

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)
  2.1 Physical Interaction (Interactome)
  2.2 Regulatory Hierarchy (Direct Transcription)
  2.3 Co-Pathway Membership (Signaling / Metabolic)

PHASE 3 — PERTURBATION MECHANICS (Why would knockout of {pert} affect {gene}?)
  CATEGORY A — Direct Information Flow Failure (The Command Chain)
  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
  CATEGORY E — Complex Stability & Degradation (The House of Cards)
  CATEGORY F — Null Topology (No Functional Link)

─────────────────────────────────────────────────────────────────────────────

CRITICAL CALIBRATION RULES:
1. "No significant effect" (C) must only be chosen if the genes are biologically isolated (Null Topology) or if competing pathways perfectly cancel each other out. Do NOT use C as a "safe guess" if you are simply unsure about the direction of a known pathway.
2. Track the sign of regulation carefully:
   - Knocking down a POSITIVE regulator of a gene leads to DOWN-regulation (B).
   - Knocking down a NEGATIVE regulator (repressor) leads to UP-regulation (A).
3. Do not invent long, unproven pathways. If a pathway connection is highly speculative or weak, it is likely a Null Topology (C).

REAL-WORLD PERTURB-SEQ EXAMPLES IN MACROPHAGES:

--- Example 1 (Loss of Activator) ---
Perturbation: Spi1
Gene of interest: Tlr4
Predict the effect of CRISPR knockout of Spi1 on Tlr4:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Spi1 encodes the master transcription factor PU.1, which is essential for macrophage lineage determination and activation. Tlr4 is the primary receptor for LPS and a core component of the macrophage inflammatory response. PU.1 is known to directly bind and positively regulate the transcription of Tlr4 and the broader NF-kB signaling cascade. Knocking out the Spi1 (PU.1) master activator removes the positive transcriptional drive for these genes. Therefore, without its required activator, Tlr4 will be down-regulated.
Final output:
B

--- Example 2 (Loss of Pathway Regulator) ---
Perturbation: Gsk3b
Gene of interest: Ciita
Predict the effect of CRISPR knockout of Gsk3b on Ciita:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Gsk3b encodes Glycogen synthase kinase-3 beta, a central kinase involved in multiple signaling pathways including macrophage activation. Ciita is the master transactivator for MHC class II genes. In macrophages, the GSK3b pathway is required to positively regulate the expression of Ciita in response to inflammatory stimuli like IFN-g. Knocking out Gsk3b disrupts this essential upstream signaling cascade, preventing the proper activation of Ciita. Therefore, Ciita will be down-regulated.
Final output:
B

--- Example 3 (Null Topology) ---
Perturbation: Nop16
Gene of interest: Gbp8
Predict the effect of CRISPR knockout of Nop16 on Gbp8:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Nop16 is a nucleolar protein primarily involved in ribosome biogenesis and rRNA processing. Gbp8 is a Guanylate-binding protein involved in the interferon-driven immune response against intracellular pathogens in the cytoplasm. These two genes operate in entirely different subcellular compartments and biological modules (ribosome biogenesis vs. antiviral immunity). There is no known direct regulatory relationship or robust pathway cross-talk linking Nop16 to Gbp8. Without a clear mechanism, this is a Null Topology.
Final output:
C

--- Example 4 (Compensatory Upregulation / Stress) ---
Perturbation: Atg5
Gene of interest: Sqstm1
Predict the effect of CRISPR knockout of Atg5 on Sqstm1:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Atg5 is an essential core component of the autophagy machinery. Sqstm1 (p62) is an autophagy receptor that targets cargo for degradation and is itself degraded by autophagy. Knocking out Atg5 completely blocks autophagy, leading to the massive accumulation of undegraded proteins and cellular stress. In response to this profound autophagic stress, the cell activates compensatory transcriptional pathways (such as Nrf2) which heavily up-regulate the transcription of Sqstm1 to attempt to overcome the defect. Therefore, Sqstm1 will be up-regulated.
Final output:
A
----------------

Now, answer the following:

Perturbation: {pert}
Gene of interest: {gene}
Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Reasoning:

Final output:"""

PROMPT_V13 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Think step by step in the reasoning section.

EXAMPLES:

--- Example 1 ---
Perturbation: Spi1
Gene of interest: Tlr4
Predict the effect of CRISPR knockout of Spi1 on Tlr4:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Spi1 encodes the master transcription factor PU.1, which is essential for macrophage lineage determination and activation. Tlr4 is the primary receptor for LPS and a core component of the macrophage inflammatory response. PU.1 is known to directly bind and positively regulate the transcription of Tlr4 and the broader NF-kB signaling cascade. Knocking out the Spi1 (PU.1) master activator removes the positive transcriptional drive for these genes. Therefore, without its required activator, Tlr4 will be down-regulated.
Final output:
B

--- Example 2 ---
Perturbation: Gsk3b
Gene of interest: Ciita
Predict the effect of CRISPR knockout of Gsk3b on Ciita:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Gsk3b encodes Glycogen synthase kinase-3 beta, a central kinase involved in multiple signaling pathways including macrophage activation. Ciita is the master transactivator for MHC class II genes. In macrophages, the GSK3b pathway is required to positively regulate the expression of Ciita in response to inflammatory stimuli like IFN-g. Knocking out Gsk3b disrupts this essential upstream signaling cascade, preventing the proper activation of Ciita. Therefore, Ciita will be down-regulated.
Final output:
B

--- Example 3 ---
Perturbation: Nop16
Gene of interest: Gbp8
Predict the effect of CRISPR knockout of Nop16 on Gbp8:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Nop16 is a nucleolar protein primarily involved in ribosome biogenesis and rRNA processing. Gbp8 is a Guanylate-binding protein involved in the interferon-driven immune response against intracellular pathogens in the cytoplasm. These two genes operate in entirely different subcellular compartments and biological modules (ribosome biogenesis vs. antiviral immunity). There is no known direct regulatory relationship or robust pathway cross-talk linking Nop16 to Gbp8. Without a clear mechanism, this is a Null Topology.
Final output:
C

--- Example 4 ---
Perturbation: Atg5
Gene of interest: Sqstm1
Predict the effect of CRISPR knockout of Atg5 on Sqstm1:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Atg5 is an essential core component of the autophagy machinery. Sqstm1 (p62) is an autophagy receptor that targets cargo for degradation and is itself degraded by autophagy. Knocking out Atg5 completely blocks autophagy, leading to the massive accumulation of undegraded proteins and cellular stress. In response to this profound autophagic stress, the cell activates compensatory transcriptional pathways (such as Nrf2) which heavily up-regulate the transcription of Sqstm1 to attempt to overcome the defect. Therefore, Sqstm1 will be up-regulated.
Final output:
A
----------------

Now, answer the following:

Perturbation: {pert}
Gene of interest: {gene}
Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Reasoning:

Final output:"""

PROMPT_V14 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Think step by step in the reasoning section.

EXAMPLES:

--- Example 1 ---
Perturbation: Spi1
Gene of interest: Tlr4
Predict the effect of CRISPR knockout of Spi1 on Tlr4:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Spi1 encodes the master transcription factor PU.1, which is essential for macrophage lineage determination and activation. Tlr4 is the primary receptor for LPS and a core component of the macrophage inflammatory response. PU.1 is known to directly bind and positively regulate the transcription of Tlr4 and the broader NF-kB signaling cascade. Knocking out the Spi1 (PU.1) master activator removes the positive transcriptional drive for these genes. Therefore, without its required activator, Tlr4 will be down-regulated.
Final output:
B

--- Example 2 ---
Perturbation: Gsk3b
Gene of interest: Ciita
Predict the effect of CRISPR knockout of Gsk3b on Ciita:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Gsk3b encodes Glycogen synthase kinase-3 beta, a central kinase involved in multiple signaling pathways including macrophage activation. Ciita is the master transactivator for MHC class II genes. In macrophages, the GSK3b pathway is required to positively regulate the expression of Ciita in response to inflammatory stimuli like IFN-g. Knocking out Gsk3b disrupts this essential upstream signaling cascade, preventing the proper activation of Ciita. Therefore, Ciita will be down-regulated.
Final output:
B

--- Example 3 ---
Perturbation: Mmp9
Gene of interest: Polr2a
Predict the effect of CRISPR knockout of Mmp9 on Polr2a:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Mmp9 encodes Matrix metalloproteinase-9, an enzyme secreted into the extracellular matrix to degrade structural proteins during tissue remodeling and inflammation. Polr2a encodes the central catalytic subunit of RNA polymerase II, which resides in the nucleus and is responsible for all mRNA transcription. These two genes operate in entirely different subcellular compartments (extracellular vs. nucleus) and biological modules. Knocking out a secreted protease will have no direct or significant indirect effect on the basal transcription of the core RNA polymerase II subunit. Without a clear mechanism, this is a Null Topology.
Final output:
C

--- Example 4 ---
Perturbation: Atg5
Gene of interest: Sqstm1
Predict the effect of CRISPR knockout of Atg5 on Sqstm1:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Atg5 is an essential core component of the autophagy machinery. Sqstm1 (p62) is an autophagy receptor that targets cargo for degradation and is itself degraded by autophagy. Knocking out Atg5 completely blocks autophagy, leading to the massive accumulation of undegraded proteins and cellular stress. In response to this profound autophagic stress, the cell activates compensatory transcriptional pathways (such as Nrf2) which heavily up-regulate the transcription of Sqstm1 to attempt to overcome the defect. Therefore, Sqstm1 will be up-regulated.
Final output:
A
----------------

Now, answer the following:

Perturbation: {pert}
Gene of interest: {gene}
Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Reasoning:

Final output:"""

PROMPT_V15 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Think step by step in the reasoning section. Base your prediction strictly on biological mechanisms and systems-level logic.

CRITICAL REASONING GUIDELINES:
1. Null Topology (C): Most random gene pairs in biology do not interact. If there is no plausible biological link between the genes (e.g. they operate in completely unrelated cellular compartments with no cross-talk), confidently predict C.
2. Compensatory Upregulation (A): When a perturbation impairs a specific cellular function or organelle, the cell often triggers compensatory transcriptional upregulation of related genes to overcome the defect.
3. De-repression (A): Loss of a transcriptional repressor or insulator leads to UP-regulation of its targets.
4. Loss of Activator (B): Loss of a positive transcriptional regulator or required upstream signaling kinase leads to DOWN-regulation.
5. Systemic Stress Responses: Explicitly consider broad pathways like ER stress, nucleolar stress, and DNA damage response.

REAL-WORLD PERTURB-SEQ EXAMPLES IN MACROPHAGES:

--- Example 1 (Loss of Activator) ---
Perturbation: Spi1
Gene of interest: Tlr4
Predict the effect of CRISPR knockout of Spi1 on Tlr4:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Spi1 encodes the master transcription factor PU.1, which is essential for macrophage lineage determination and activation. Tlr4 is the primary receptor for LPS and a core component of the macrophage inflammatory response. PU.1 is known to directly bind and positively regulate the transcription of Tlr4 and the broader NF-kB signaling cascade. Knocking out the Spi1 (PU.1) master activator removes the positive transcriptional drive for these genes. Therefore, without its required activator, Tlr4 will be down-regulated.
Final output:
B

--- Example 2 (Loss of Pathway Regulator) ---
Perturbation: Gsk3b
Gene of interest: Ciita
Predict the effect of CRISPR knockout of Gsk3b on Ciita:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Gsk3b encodes Glycogen synthase kinase-3 beta, a central kinase involved in multiple signaling pathways including macrophage activation. Ciita is the master transactivator for MHC class II genes. In macrophages, the GSK3b pathway is required to positively regulate the expression of Ciita in response to inflammatory stimuli like IFN-g. Knocking out Gsk3b disrupts this essential upstream signaling cascade, preventing the proper activation of Ciita. Therefore, Ciita will be down-regulated.
Final output:
B

--- Example 3 (Null Topology) ---
Perturbation: Mmp9
Gene of interest: Polr2a
Predict the effect of CRISPR knockout of Mmp9 on Polr2a:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Mmp9 encodes Matrix metalloproteinase-9, an enzyme secreted into the extracellular matrix to degrade structural proteins during tissue remodeling and inflammation. Polr2a encodes the central catalytic subunit of RNA polymerase II, which resides in the nucleus and is responsible for all mRNA transcription. These two genes operate in entirely different subcellular compartments (extracellular vs. nucleus) and biological modules. Knocking out a secreted protease will have no direct or significant indirect effect on the basal transcription of the core RNA polymerase II subunit. Without a clear mechanism, this is a Null Topology.
Final output:
C

--- Example 4 (Compensatory Upregulation / Stress) ---
Perturbation: Atg5
Gene of interest: Sqstm1
Predict the effect of CRISPR knockout of Atg5 on Sqstm1:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Atg5 is an essential core component of the autophagy machinery. Sqstm1 (p62) is an autophagy receptor that targets cargo for degradation and is itself degraded by autophagy. Knocking out Atg5 completely blocks autophagy, leading to the massive accumulation of undegraded proteins and cellular stress. In response to this profound autophagic stress, the cell activates compensatory transcriptional pathways (such as Nrf2) which heavily up-regulate the transcription of Sqstm1 to attempt to overcome the defect. Therefore, Sqstm1 will be up-regulated.
Final output:
A
----------------

Now, answer the following:

Perturbation: {pert}
Gene of interest: {gene}
Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Reasoning:

Final output:"""


PROMPT_V16 = """You are an expert computational biologist specialising in CRISPRi gene perturbation screens in mouse bone marrow-derived macrophages (BMDMs). The perturbation mechanism is CRISPRi (transcriptional repression / knockdown), NOT CRISPR knockout. This means only direct transcriptional targets and immediate first-order downstream effects are detectable. Protein-level interactions that do not affect transcription of the target gene are not relevant evidence.

Labels are derived from CROPseq pooled screens processed through the CropFlow pipeline: a gene is labelled 'up' or 'down' only if it passes 5% FDR (Benjamini-Hochberg) AND a minimum apeglm-shrunken |log2FC| threshold. apeglm shrinkage pulls weak effects toward zero, so the 'no-change' class is wider than a raw fold-change threshold would suggest. Borderline targets of weak regulators are systematically labelled no-change.

Default to no-change. Override this default only when you can identify a specific, evidence-backed mechanistic link between the perturbation and the target gene in macrophages or closely related myeloid cells. Speculative multi-step pathways that are not supported by macrophage-specific evidence do not justify overriding the default.

Do not include confidence scores, constraint checklists, or capability verification statements. Begin your analysis immediately with Step 1.

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


PROMPT_V17 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived macrophages (BMDMs).

Think step by step in the reasoning section.

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

--- Example 1 ---
Perturbation: Spi1
Gene of interest: Tlr4
Predict the effect of CRISPRi knockdown of Spi1 on Tlr4:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Spi1 encodes the master transcription factor PU.1, which is essential for macrophage lineage determination and activation. Tlr4 is the primary receptor for LPS and a core component of the macrophage inflammatory response. PU.1 is known to directly bind and positively regulate the transcription of Tlr4. Knocking down the Spi1 (PU.1) master activator removes the positive transcriptional drive for these genes. Therefore, without its required activator, Tlr4 will be down-regulated.
Final output:
B

--- Example 2 ---
Perturbation: Gsk3b
Gene of interest: Ciita
Predict the effect of CRISPRi knockdown of Gsk3b on Ciita:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Gsk3b encodes Glycogen synthase kinase-3 beta, a central kinase involved in multiple signaling pathways including macrophage activation. Ciita is the master transactivator for MHC class II genes. In macrophages, the GSK3b pathway is required to positively regulate the expression of Ciita in response to inflammatory stimuli like IFN-g. Knocking down Gsk3b disrupts this essential upstream signaling cascade, preventing the proper activation of Ciita. Therefore, Ciita will be down-regulated.
Final output:
B

--- Example 3 ---
Perturbation: Mmp9
Gene of interest: Polr2a
Predict the effect of CRISPRi knockdown of Mmp9 on Polr2a:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Mmp9 encodes Matrix metalloproteinase-9, an enzyme secreted into the extracellular matrix to degrade structural proteins during tissue remodeling and inflammation. Polr2a encodes the central catalytic subunit of RNA polymerase II, which resides in the nucleus and is responsible for all mRNA transcription. These two genes operate in entirely different subcellular compartments (extracellular vs. nucleus). Knocking down a secreted protease will have no direct or significant indirect effect on the basal transcription of the core RNA polymerase II subunit.
Final output:
C
----------------

Now, answer the following:

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPRi knockdown of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Reasoning:

Final output:"""