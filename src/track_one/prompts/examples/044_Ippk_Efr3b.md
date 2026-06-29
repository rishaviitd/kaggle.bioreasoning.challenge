# Example 044: `Ippk_Efr3b`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Ippk` |
| **Gene of interest** | `Efr3b` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Ippk
Gene of interest: Efr3b

Predict the effect of CRISPRi knockdown of Ippk on Efr3b:
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
      What is the primary biochemical class of Ippk and Efr3b?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Ippk and Efr3b reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Ippk and Efr3b proteins physically assemble into a complex?
      If yes, is Efr3b dependent on Ippk for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Ippk directly regulate transcription of Efr3b?
      (Is Ippk a known TF/co-factor that binds the Efr3b promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Ippk and Efr3b in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Ippk affect Efr3b?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Ippk directly activate or repress Efr3b expression?
      Knocking down Ippk — does it remove a known activator or a known repressor of Efr3b?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Ippk upstream of Efr3b in a defined signaling pathway?
      Does loss of Ippk block a phosphorylation/activation event required to regulate Efr3b?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Ippk trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Efr3b expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Ippk?
      Could loss of Ippk lead to upregulation of Efr3b as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Ippk and Efr3b protein products members of the same complex?
      If Ippk is knocked down, does Efr3b protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Ippk and Efr3b in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Ippk directly controls Efr3b
  [ 2. Indirect Path ] — Ippk affects Efr3b through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Efr3b
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
