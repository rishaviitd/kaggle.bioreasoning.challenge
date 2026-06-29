# Example 068: `Nol10_Cotl1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Nol10` |
| **Gene of interest** | `Cotl1` |
| **Ground-truth label** | `DOWN` — B) down-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Nol10
Gene of interest: Cotl1

Predict the effect of CRISPRi knockdown of Nol10 on Cotl1:
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
      What is the primary biochemical class of Nol10 and Cotl1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Nol10 and Cotl1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Nol10 and Cotl1 proteins physically assemble into a complex?
      If yes, is Cotl1 dependent on Nol10 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Nol10 directly regulate transcription of Cotl1?
      (Is Nol10 a known TF/co-factor that binds the Cotl1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Nol10 and Cotl1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Nol10 affect Cotl1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Nol10 directly activate or repress Cotl1 expression?
      Knocking down Nol10 — does it remove a known activator or a known repressor of Cotl1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Nol10 upstream of Cotl1 in a defined signaling pathway?
      Does loss of Nol10 block a phosphorylation/activation event required to regulate Cotl1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Nol10 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Cotl1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Nol10?
      Could loss of Nol10 lead to upregulation of Cotl1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Nol10 and Cotl1 protein products members of the same complex?
      If Nol10 is knocked down, does Cotl1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Nol10 and Cotl1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Nol10 directly controls Cotl1
  [ 2. Indirect Path ] — Nol10 affects Cotl1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Cotl1
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
