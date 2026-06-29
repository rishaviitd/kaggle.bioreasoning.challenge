# Example 040: `Dync1i2_Fmr1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Dync1i2` |
| **Gene of interest** | `Fmr1` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Dync1i2
Gene of interest: Fmr1

Predict the effect of CRISPRi knockdown of Dync1i2 on Fmr1:
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
      What is the primary biochemical class of Dync1i2 and Fmr1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Dync1i2 and Fmr1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Dync1i2 and Fmr1 proteins physically assemble into a complex?
      If yes, is Fmr1 dependent on Dync1i2 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Dync1i2 directly regulate transcription of Fmr1?
      (Is Dync1i2 a known TF/co-factor that binds the Fmr1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Dync1i2 and Fmr1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Dync1i2 affect Fmr1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Dync1i2 directly activate or repress Fmr1 expression?
      Knocking down Dync1i2 — does it remove a known activator or a known repressor of Fmr1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Dync1i2 upstream of Fmr1 in a defined signaling pathway?
      Does loss of Dync1i2 block a phosphorylation/activation event required to regulate Fmr1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Dync1i2 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Fmr1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Dync1i2?
      Could loss of Dync1i2 lead to upregulation of Fmr1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Dync1i2 and Fmr1 protein products members of the same complex?
      If Dync1i2 is knocked down, does Fmr1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Dync1i2 and Fmr1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Dync1i2 directly controls Fmr1
  [ 2. Indirect Path ] — Dync1i2 affects Fmr1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Fmr1
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
