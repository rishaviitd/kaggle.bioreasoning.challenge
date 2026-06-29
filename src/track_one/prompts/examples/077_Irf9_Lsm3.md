# Example 077: `Irf9_Lsm3`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Irf9` |
| **Gene of interest** | `Lsm3` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Irf9
Gene of interest: Lsm3

Predict the effect of CRISPRi knockdown of Irf9 on Lsm3:
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
      What is the primary biochemical class of Irf9 and Lsm3?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Irf9 and Lsm3 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Irf9 and Lsm3 proteins physically assemble into a complex?
      If yes, is Lsm3 dependent on Irf9 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Irf9 directly regulate transcription of Lsm3?
      (Is Irf9 a known TF/co-factor that binds the Lsm3 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Irf9 and Lsm3 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Irf9 affect Lsm3?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Irf9 directly activate or repress Lsm3 expression?
      Knocking down Irf9 — does it remove a known activator or a known repressor of Lsm3?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Irf9 upstream of Lsm3 in a defined signaling pathway?
      Does loss of Irf9 block a phosphorylation/activation event required to regulate Lsm3?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Irf9 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Lsm3 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Irf9?
      Could loss of Irf9 lead to upregulation of Lsm3 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Irf9 and Lsm3 protein products members of the same complex?
      If Irf9 is knocked down, does Lsm3 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Irf9 and Lsm3 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Irf9 directly controls Lsm3
  [ 2. Indirect Path ] — Irf9 affects Lsm3 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Lsm3
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
