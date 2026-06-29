# Example 010: `Rps5_Cks1b`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Rps5` |
| **Gene of interest** | `Cks1b` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Rps5
Gene of interest: Cks1b

Predict the effect of CRISPRi knockdown of Rps5 on Cks1b:
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
      What is the primary biochemical class of Rps5 and Cks1b?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Rps5 and Cks1b reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Rps5 and Cks1b proteins physically assemble into a complex?
      If yes, is Cks1b dependent on Rps5 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Rps5 directly regulate transcription of Cks1b?
      (Is Rps5 a known TF/co-factor that binds the Cks1b promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Rps5 and Cks1b in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Rps5 affect Cks1b?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Rps5 directly activate or repress Cks1b expression?
      Knocking down Rps5 — does it remove a known activator or a known repressor of Cks1b?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Rps5 upstream of Cks1b in a defined signaling pathway?
      Does loss of Rps5 block a phosphorylation/activation event required to regulate Cks1b?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Rps5 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Cks1b expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Rps5?
      Could loss of Rps5 lead to upregulation of Cks1b as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Rps5 and Cks1b protein products members of the same complex?
      If Rps5 is knocked down, does Cks1b protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Rps5 and Cks1b in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Rps5 directly controls Cks1b
  [ 2. Indirect Path ] — Rps5 affects Cks1b through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Cks1b
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
