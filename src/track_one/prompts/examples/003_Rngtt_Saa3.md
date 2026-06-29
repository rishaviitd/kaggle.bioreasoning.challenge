# Example 003: `Rngtt_Saa3`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Rngtt` |
| **Gene of interest** | `Saa3` |
| **Ground-truth label** | `DOWN` — B) down-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Rngtt
Gene of interest: Saa3

Predict the effect of CRISPRi knockdown of Rngtt on Saa3:
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
      What is the primary biochemical class of Rngtt and Saa3?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Rngtt and Saa3 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Rngtt and Saa3 proteins physically assemble into a complex?
      If yes, is Saa3 dependent on Rngtt for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Rngtt directly regulate transcription of Saa3?
      (Is Rngtt a known TF/co-factor that binds the Saa3 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Rngtt and Saa3 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Rngtt affect Saa3?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Rngtt directly activate or repress Saa3 expression?
      Knocking down Rngtt — does it remove a known activator or a known repressor of Saa3?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Rngtt upstream of Saa3 in a defined signaling pathway?
      Does loss of Rngtt block a phosphorylation/activation event required to regulate Saa3?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Rngtt trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Saa3 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Rngtt?
      Could loss of Rngtt lead to upregulation of Saa3 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Rngtt and Saa3 protein products members of the same complex?
      If Rngtt is knocked down, does Saa3 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Rngtt and Saa3 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Rngtt directly controls Saa3
  [ 2. Indirect Path ] — Rngtt affects Saa3 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Saa3
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
