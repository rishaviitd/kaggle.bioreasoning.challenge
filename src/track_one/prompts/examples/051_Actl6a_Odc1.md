# Example 051: `Actl6a_Odc1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Actl6a` |
| **Gene of interest** | `Odc1` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Actl6a
Gene of interest: Odc1

Predict the effect of CRISPRi knockdown of Actl6a on Odc1:
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
      What is the primary biochemical class of Actl6a and Odc1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Actl6a and Odc1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Actl6a and Odc1 proteins physically assemble into a complex?
      If yes, is Odc1 dependent on Actl6a for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Actl6a directly regulate transcription of Odc1?
      (Is Actl6a a known TF/co-factor that binds the Odc1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Actl6a and Odc1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Actl6a affect Odc1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Actl6a directly activate or repress Odc1 expression?
      Knocking down Actl6a — does it remove a known activator or a known repressor of Odc1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Actl6a upstream of Odc1 in a defined signaling pathway?
      Does loss of Actl6a block a phosphorylation/activation event required to regulate Odc1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Actl6a trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Odc1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Actl6a?
      Could loss of Actl6a lead to upregulation of Odc1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Actl6a and Odc1 protein products members of the same complex?
      If Actl6a is knocked down, does Odc1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Actl6a and Odc1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Actl6a directly controls Odc1
  [ 2. Indirect Path ] — Actl6a affects Odc1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Odc1
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
