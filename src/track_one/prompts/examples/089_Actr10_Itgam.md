# Example 089: `Actr10_Itgam`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Actr10` |
| **Gene of interest** | `Itgam` |
| **Ground-truth label** | `DOWN` — B) down-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Actr10
Gene of interest: Itgam

Predict the effect of CRISPRi knockdown of Actr10 on Itgam:
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
      What is the primary biochemical class of Actr10 and Itgam?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Actr10 and Itgam reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Actr10 and Itgam proteins physically assemble into a complex?
      If yes, is Itgam dependent on Actr10 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Actr10 directly regulate transcription of Itgam?
      (Is Actr10 a known TF/co-factor that binds the Itgam promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Actr10 and Itgam in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Actr10 affect Itgam?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Actr10 directly activate or repress Itgam expression?
      Knocking down Actr10 — does it remove a known activator or a known repressor of Itgam?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Actr10 upstream of Itgam in a defined signaling pathway?
      Does loss of Actr10 block a phosphorylation/activation event required to regulate Itgam?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Actr10 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Itgam expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Actr10?
      Could loss of Actr10 lead to upregulation of Itgam as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Actr10 and Itgam protein products members of the same complex?
      If Actr10 is knocked down, does Itgam protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Actr10 and Itgam in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Actr10 directly controls Itgam
  [ 2. Indirect Path ] — Actr10 affects Itgam through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Itgam
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
