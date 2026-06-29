# Example 009: `Slc7a6os_Plaur`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Slc7a6os` |
| **Gene of interest** | `Plaur` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Slc7a6os
Gene of interest: Plaur

Predict the effect of CRISPRi knockdown of Slc7a6os on Plaur:
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
      What is the primary biochemical class of Slc7a6os and Plaur?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Slc7a6os and Plaur reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Slc7a6os and Plaur proteins physically assemble into a complex?
      If yes, is Plaur dependent on Slc7a6os for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Slc7a6os directly regulate transcription of Plaur?
      (Is Slc7a6os a known TF/co-factor that binds the Plaur promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Slc7a6os and Plaur in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Slc7a6os affect Plaur?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Slc7a6os directly activate or repress Plaur expression?
      Knocking down Slc7a6os — does it remove a known activator or a known repressor of Plaur?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Slc7a6os upstream of Plaur in a defined signaling pathway?
      Does loss of Slc7a6os block a phosphorylation/activation event required to regulate Plaur?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Slc7a6os trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Plaur expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Slc7a6os?
      Could loss of Slc7a6os lead to upregulation of Plaur as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Slc7a6os and Plaur protein products members of the same complex?
      If Slc7a6os is knocked down, does Plaur protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Slc7a6os and Plaur in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Slc7a6os directly controls Plaur
  [ 2. Indirect Path ] — Slc7a6os affects Plaur through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Plaur
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
