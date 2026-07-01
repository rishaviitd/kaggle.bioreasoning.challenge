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


SOLUTION_GENERATION_V0 = """You are an expert computational biologist tasked with explaining the empirical results of a CRISPR knockout screen.

### Biological Context
* **Cell Type:** Primary mouse bone marrow-derived macrophages (BMDMs) stimulated with LPS for 9 hours (active inflammatory state).
* **Perturbation Mechanism:** CRISPR knockout — the perturbed gene's protein is completely absent.
* **Measurement:** Differential expression is computed using ebnm-shrunken log2 fold-changes. A gene is labelled 'up' or 'down' only if it passes FDR < 5% AND |shrunken log2FC| >= log2(1.5). Shrinkage pulls weak or indirect effects toward zero. Therefore, 'none' does NOT always mean there is no biological connection — it means the effect was too weak, too indirect, or too noisy to survive the statistical threshold.
* **Dataset construction:** 'none' target genes are NOT randomly selected — they are specifically nearby genes that showed sub-threshold effects. Expect a plausible but weak/indirect connection.

### Task
You are given the Perturbed Gene, a Target Gene, and the GROUND TRUTH empirical label from the experiment. Your job is to reverse-engineer the biological mechanism. Write a detailed, step-by-step causal chain that logically justifies WHY this specific outcome occurred in LPS-stimulated mouse macrophages.

### Formatting Constraints
1. **Be Authoritative:** Do NOT use conversational meta-language like "We need to explain why..." or "Let's discuss". Write in the third person like a textbook.
2. **Be Direct:** State the facts of the genes, link the mechanistic pathway, and conclude logically.
3. **Mandatory Conclusion:** Your reasoning trace MUST end with the exact wording indicating the final label. (e.g. "Therefore, {gene} is up-regulated.")

### Ground Truth Event
* Perturbation (Knockout): {pert}
* Target Gene: {gene}
* True Empirical Outcome: {true_label}

Explain the mechanistic pathway that leads exactly to this outcome.

Reasoning:"""
