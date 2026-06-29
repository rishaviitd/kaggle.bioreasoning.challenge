# Example 084: `Trem2_Psma6`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Trem2` |
| **Gene of interest** | `Psma6` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Trem2
Gene of interest: Psma6

Predict the effect of CRISPRi knockdown of Trem2 on Psma6:
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
      What is the primary biochemical class of Trem2 and Psma6?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Trem2 and Psma6 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Trem2 and Psma6 proteins physically assemble into a complex?
      If yes, is Psma6 dependent on Trem2 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Trem2 directly regulate transcription of Psma6?
      (Is Trem2 a known TF/co-factor that binds the Psma6 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Trem2 and Psma6 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Trem2 affect Psma6?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Trem2 directly activate or repress Psma6 expression?
      Knocking down Trem2 — does it remove a known activator or a known repressor of Psma6?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Trem2 upstream of Psma6 in a defined signaling pathway?
      Does loss of Trem2 block a phosphorylation/activation event required to regulate Psma6?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Trem2 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Psma6 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Trem2?
      Could loss of Trem2 lead to upregulation of Psma6 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Trem2 and Psma6 protein products members of the same complex?
      If Trem2 is knocked down, does Psma6 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Trem2 and Psma6 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Trem2 directly controls Psma6
  [ 2. Indirect Path ] — Trem2 affects Psma6 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Psma6
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
