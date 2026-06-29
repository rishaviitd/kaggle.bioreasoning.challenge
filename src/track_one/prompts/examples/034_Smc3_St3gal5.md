# Example 034: `Smc3_St3gal5`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Smc3` |
| **Gene of interest** | `St3gal5` |
| **Ground-truth label** | `DOWN` — B) down-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Smc3
Gene of interest: St3gal5

Predict the effect of CRISPRi knockdown of Smc3 on St3gal5:
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
      What is the primary biochemical class of Smc3 and St3gal5?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Smc3 and St3gal5 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Smc3 and St3gal5 proteins physically assemble into a complex?
      If yes, is St3gal5 dependent on Smc3 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Smc3 directly regulate transcription of St3gal5?
      (Is Smc3 a known TF/co-factor that binds the St3gal5 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Smc3 and St3gal5 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Smc3 affect St3gal5?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Smc3 directly activate or repress St3gal5 expression?
      Knocking down Smc3 — does it remove a known activator or a known repressor of St3gal5?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Smc3 upstream of St3gal5 in a defined signaling pathway?
      Does loss of Smc3 block a phosphorylation/activation event required to regulate St3gal5?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Smc3 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter St3gal5 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Smc3?
      Could loss of Smc3 lead to upregulation of St3gal5 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Smc3 and St3gal5 protein products members of the same complex?
      If Smc3 is knocked down, does St3gal5 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Smc3 and St3gal5 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Smc3 directly controls St3gal5
  [ 2. Indirect Path ] — Smc3 affects St3gal5 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches St3gal5
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
