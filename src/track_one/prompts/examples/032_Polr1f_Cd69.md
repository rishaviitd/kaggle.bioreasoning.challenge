# Example 032: `Polr1f_Cd69`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Polr1f` |
| **Gene of interest** | `Cd69` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Polr1f
Gene of interest: Cd69

Predict the effect of CRISPRi knockdown of Polr1f on Cd69:
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
      What is the primary biochemical class of Polr1f and Cd69?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Polr1f and Cd69 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Polr1f and Cd69 proteins physically assemble into a complex?
      If yes, is Cd69 dependent on Polr1f for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Polr1f directly regulate transcription of Cd69?
      (Is Polr1f a known TF/co-factor that binds the Cd69 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Polr1f and Cd69 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Polr1f affect Cd69?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Polr1f directly activate or repress Cd69 expression?
      Knocking down Polr1f — does it remove a known activator or a known repressor of Cd69?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Polr1f upstream of Cd69 in a defined signaling pathway?
      Does loss of Polr1f block a phosphorylation/activation event required to regulate Cd69?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Polr1f trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Cd69 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Polr1f?
      Could loss of Polr1f lead to upregulation of Cd69 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Polr1f and Cd69 protein products members of the same complex?
      If Polr1f is knocked down, does Cd69 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Polr1f and Cd69 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Polr1f directly controls Cd69
  [ 2. Indirect Path ] — Polr1f affects Cd69 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Cd69
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
