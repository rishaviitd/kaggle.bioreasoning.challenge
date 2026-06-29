# Example 081: `Rps5_Nampt`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Rps5` |
| **Gene of interest** | `Nampt` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Rps5
Gene of interest: Nampt

Predict the effect of CRISPRi knockdown of Rps5 on Nampt:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section. Use the structured framework below to guide your
analysis. You do not need to answer every question — use whichever are relevant to reach a
well-justified conclusion.

─────────────────────────────────────────────────────────────────────────────
REASONING FRAMEWORK
─────────────────────────────────────────────────────────────────────────────

PHASE 1 — PRIMITIVE IDENTITY (What are these genes?)

  1.1 Functional Classification
      What is the primary biochemical class of Rps5 and Nampt?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Rps5 and Nampt reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Rps5 and Nampt proteins physically assemble into a complex?
      If yes, is Nampt dependent on Rps5 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Rps5 directly regulate transcription of Nampt?
      (Is Rps5 a known TF/co-factor that binds the Nampt promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Rps5 and Nampt in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Rps5 affect Nampt?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Rps5 directly activate or repress Nampt expression?
      Knocking down Rps5 — does it remove a known activator or a known repressor of Nampt?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Rps5 upstream of Nampt in a defined signaling pathway?
      Does loss of Rps5 block a phosphorylation/activation event required to regulate Nampt?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Rps5 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Nampt expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Rps5?
      Could loss of Rps5 lead to upregulation of Nampt as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Rps5 and Nampt protein products members of the same complex?
      If Rps5 is knocked down, does Nampt protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Rps5 and Nampt in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Rps5 directly controls Nampt
  [ 2. Indirect Path ] — Rps5 affects Nampt through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Nampt
  [ 4. Null Topology ] — no meaningful functional link exists

─────────────────────────────────────────────────────────────────────────────

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:
```
