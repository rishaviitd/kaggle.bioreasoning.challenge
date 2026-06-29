# Example 078: `Emc3_Hsd3b7`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Emc3` |
| **Gene of interest** | `Hsd3b7` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Emc3
Gene of interest: Hsd3b7

Predict the effect of CRISPRi knockdown of Emc3 on Hsd3b7:
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
      What is the primary biochemical class of Emc3 and Hsd3b7?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Emc3 and Hsd3b7 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Emc3 and Hsd3b7 proteins physically assemble into a complex?
      If yes, is Hsd3b7 dependent on Emc3 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Emc3 directly regulate transcription of Hsd3b7?
      (Is Emc3 a known TF/co-factor that binds the Hsd3b7 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Emc3 and Hsd3b7 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Emc3 affect Hsd3b7?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Emc3 directly activate or repress Hsd3b7 expression?
      Knocking down Emc3 — does it remove a known activator or a known repressor of Hsd3b7?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Emc3 upstream of Hsd3b7 in a defined signaling pathway?
      Does loss of Emc3 block a phosphorylation/activation event required to regulate Hsd3b7?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Emc3 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Hsd3b7 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Emc3?
      Could loss of Emc3 lead to upregulation of Hsd3b7 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Emc3 and Hsd3b7 protein products members of the same complex?
      If Emc3 is knocked down, does Hsd3b7 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Emc3 and Hsd3b7 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Emc3 directly controls Hsd3b7
  [ 2. Indirect Path ] — Emc3 affects Hsd3b7 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Hsd3b7
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
