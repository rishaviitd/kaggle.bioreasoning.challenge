# Example 022: `Yrdc_Slc25a13`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Yrdc` |
| **Gene of interest** | `Slc25a13` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Yrdc
Gene of interest: Slc25a13

Predict the effect of CRISPRi knockdown of Yrdc on Slc25a13:
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
      What is the primary biochemical class of Yrdc and Slc25a13?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Yrdc and Slc25a13 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Yrdc and Slc25a13 proteins physically assemble into a complex?
      If yes, is Slc25a13 dependent on Yrdc for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Yrdc directly regulate transcription of Slc25a13?
      (Is Yrdc a known TF/co-factor that binds the Slc25a13 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Yrdc and Slc25a13 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Yrdc affect Slc25a13?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Yrdc directly activate or repress Slc25a13 expression?
      Knocking down Yrdc — does it remove a known activator or a known repressor of Slc25a13?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Yrdc upstream of Slc25a13 in a defined signaling pathway?
      Does loss of Yrdc block a phosphorylation/activation event required to regulate Slc25a13?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Yrdc trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Slc25a13 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Yrdc?
      Could loss of Yrdc lead to upregulation of Slc25a13 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Yrdc and Slc25a13 protein products members of the same complex?
      If Yrdc is knocked down, does Slc25a13 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Yrdc and Slc25a13 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Yrdc directly controls Slc25a13
  [ 2. Indirect Path ] — Yrdc affects Slc25a13 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Slc25a13
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
