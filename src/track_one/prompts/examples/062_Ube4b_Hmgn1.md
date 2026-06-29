# Example 062: `Ube4b_Hmgn1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Ube4b` |
| **Gene of interest** | `Hmgn1` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Ube4b
Gene of interest: Hmgn1

Predict the effect of CRISPRi knockdown of Ube4b on Hmgn1:
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
      What is the primary biochemical class of Ube4b and Hmgn1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Ube4b and Hmgn1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Ube4b and Hmgn1 proteins physically assemble into a complex?
      If yes, is Hmgn1 dependent on Ube4b for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Ube4b directly regulate transcription of Hmgn1?
      (Is Ube4b a known TF/co-factor that binds the Hmgn1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Ube4b and Hmgn1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Ube4b affect Hmgn1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Ube4b directly activate or repress Hmgn1 expression?
      Knocking down Ube4b — does it remove a known activator or a known repressor of Hmgn1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Ube4b upstream of Hmgn1 in a defined signaling pathway?
      Does loss of Ube4b block a phosphorylation/activation event required to regulate Hmgn1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Ube4b trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Hmgn1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Ube4b?
      Could loss of Ube4b lead to upregulation of Hmgn1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Ube4b and Hmgn1 protein products members of the same complex?
      If Ube4b is knocked down, does Hmgn1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Ube4b and Hmgn1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Ube4b directly controls Hmgn1
  [ 2. Indirect Path ] — Ube4b affects Hmgn1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Hmgn1
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
