# Example 067: `Rb1cc1_Polr2a`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Rb1cc1` |
| **Gene of interest** | `Polr2a` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Rb1cc1
Gene of interest: Polr2a

Predict the effect of CRISPRi knockdown of Rb1cc1 on Polr2a:
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
      What is the primary biochemical class of Rb1cc1 and Polr2a?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Rb1cc1 and Polr2a reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Rb1cc1 and Polr2a proteins physically assemble into a complex?
      If yes, is Polr2a dependent on Rb1cc1 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Rb1cc1 directly regulate transcription of Polr2a?
      (Is Rb1cc1 a known TF/co-factor that binds the Polr2a promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Rb1cc1 and Polr2a in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Rb1cc1 affect Polr2a?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Rb1cc1 directly activate or repress Polr2a expression?
      Knocking down Rb1cc1 — does it remove a known activator or a known repressor of Polr2a?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Rb1cc1 upstream of Polr2a in a defined signaling pathway?
      Does loss of Rb1cc1 block a phosphorylation/activation event required to regulate Polr2a?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Rb1cc1 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Polr2a expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Rb1cc1?
      Could loss of Rb1cc1 lead to upregulation of Polr2a as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Rb1cc1 and Polr2a protein products members of the same complex?
      If Rb1cc1 is knocked down, does Polr2a protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Rb1cc1 and Polr2a in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Rb1cc1 directly controls Polr2a
  [ 2. Indirect Path ] — Rb1cc1 affects Polr2a through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Polr2a
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
