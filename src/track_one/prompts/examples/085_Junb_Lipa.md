# Example 085: `Junb_Lipa`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Junb` |
| **Gene of interest** | `Lipa` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Junb
Gene of interest: Lipa

Predict the effect of CRISPRi knockdown of Junb on Lipa:
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
      What is the primary biochemical class of Junb and Lipa?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Junb and Lipa reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Junb and Lipa proteins physically assemble into a complex?
      If yes, is Lipa dependent on Junb for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Junb directly regulate transcription of Lipa?
      (Is Junb a known TF/co-factor that binds the Lipa promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Junb and Lipa in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Junb affect Lipa?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Junb directly activate or repress Lipa expression?
      Knocking down Junb — does it remove a known activator or a known repressor of Lipa?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Junb upstream of Lipa in a defined signaling pathway?
      Does loss of Junb block a phosphorylation/activation event required to regulate Lipa?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Junb trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Lipa expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Junb?
      Could loss of Junb lead to upregulation of Lipa as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Junb and Lipa protein products members of the same complex?
      If Junb is knocked down, does Lipa protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Junb and Lipa in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Junb directly controls Lipa
  [ 2. Indirect Path ] — Junb affects Lipa through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Lipa
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
