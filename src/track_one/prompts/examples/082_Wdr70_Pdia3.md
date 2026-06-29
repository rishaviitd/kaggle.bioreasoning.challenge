# Example 082: `Wdr70_Pdia3`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Wdr70` |
| **Gene of interest** | `Pdia3` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Wdr70
Gene of interest: Pdia3

Predict the effect of CRISPRi knockdown of Wdr70 on Pdia3:
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
      What is the primary biochemical class of Wdr70 and Pdia3?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Wdr70 and Pdia3 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Wdr70 and Pdia3 proteins physically assemble into a complex?
      If yes, is Pdia3 dependent on Wdr70 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Wdr70 directly regulate transcription of Pdia3?
      (Is Wdr70 a known TF/co-factor that binds the Pdia3 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Wdr70 and Pdia3 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Wdr70 affect Pdia3?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Wdr70 directly activate or repress Pdia3 expression?
      Knocking down Wdr70 — does it remove a known activator or a known repressor of Pdia3?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Wdr70 upstream of Pdia3 in a defined signaling pathway?
      Does loss of Wdr70 block a phosphorylation/activation event required to regulate Pdia3?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Wdr70 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Pdia3 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Wdr70?
      Could loss of Wdr70 lead to upregulation of Pdia3 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Wdr70 and Pdia3 protein products members of the same complex?
      If Wdr70 is knocked down, does Pdia3 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Wdr70 and Pdia3 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Wdr70 directly controls Pdia3
  [ 2. Indirect Path ] — Wdr70 affects Pdia3 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Pdia3
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
