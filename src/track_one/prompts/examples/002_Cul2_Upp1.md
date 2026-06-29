# Example 002: `Cul2_Upp1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Cul2` |
| **Gene of interest** | `Upp1` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Cul2
Gene of interest: Upp1

Predict the effect of CRISPRi knockdown of Cul2 on Upp1:
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
      What is the primary biochemical class of Cul2 and Upp1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Cul2 and Upp1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Cul2 and Upp1 proteins physically assemble into a complex?
      If yes, is Upp1 dependent on Cul2 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Cul2 directly regulate transcription of Upp1?
      (Is Cul2 a known TF/co-factor that binds the Upp1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Cul2 and Upp1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Cul2 affect Upp1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Cul2 directly activate or repress Upp1 expression?
      Knocking down Cul2 — does it remove a known activator or a known repressor of Upp1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Cul2 upstream of Upp1 in a defined signaling pathway?
      Does loss of Cul2 block a phosphorylation/activation event required to regulate Upp1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Cul2 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Upp1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Cul2?
      Could loss of Cul2 lead to upregulation of Upp1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Cul2 and Upp1 protein products members of the same complex?
      If Cul2 is knocked down, does Upp1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Cul2 and Upp1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Cul2 directly controls Upp1
  [ 2. Indirect Path ] — Cul2 affects Upp1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Upp1
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
