# Example 054: `Smg5_Vwa3b`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Smg5` |
| **Gene of interest** | `Vwa3b` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Smg5
Gene of interest: Vwa3b

Predict the effect of CRISPRi knockdown of Smg5 on Vwa3b:
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
      What is the primary biochemical class of Smg5 and Vwa3b?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Smg5 and Vwa3b reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Smg5 and Vwa3b proteins physically assemble into a complex?
      If yes, is Vwa3b dependent on Smg5 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Smg5 directly regulate transcription of Vwa3b?
      (Is Smg5 a known TF/co-factor that binds the Vwa3b promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Smg5 and Vwa3b in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Smg5 affect Vwa3b?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Smg5 directly activate or repress Vwa3b expression?
      Knocking down Smg5 — does it remove a known activator or a known repressor of Vwa3b?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Smg5 upstream of Vwa3b in a defined signaling pathway?
      Does loss of Smg5 block a phosphorylation/activation event required to regulate Vwa3b?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Smg5 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Vwa3b expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Smg5?
      Could loss of Smg5 lead to upregulation of Vwa3b as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Smg5 and Vwa3b protein products members of the same complex?
      If Smg5 is knocked down, does Vwa3b protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Smg5 and Vwa3b in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Smg5 directly controls Vwa3b
  [ 2. Indirect Path ] — Smg5 affects Vwa3b through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Vwa3b
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
