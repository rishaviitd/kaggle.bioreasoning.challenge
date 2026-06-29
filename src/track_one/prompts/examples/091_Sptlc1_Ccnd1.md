# Example 091: `Sptlc1_Ccnd1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Sptlc1` |
| **Gene of interest** | `Ccnd1` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Sptlc1
Gene of interest: Ccnd1

Predict the effect of CRISPRi knockdown of Sptlc1 on Ccnd1:
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
      What is the primary biochemical class of Sptlc1 and Ccnd1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Sptlc1 and Ccnd1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Sptlc1 and Ccnd1 proteins physically assemble into a complex?
      If yes, is Ccnd1 dependent on Sptlc1 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Sptlc1 directly regulate transcription of Ccnd1?
      (Is Sptlc1 a known TF/co-factor that binds the Ccnd1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Sptlc1 and Ccnd1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Sptlc1 affect Ccnd1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Sptlc1 directly activate or repress Ccnd1 expression?
      Knocking down Sptlc1 — does it remove a known activator or a known repressor of Ccnd1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Sptlc1 upstream of Ccnd1 in a defined signaling pathway?
      Does loss of Sptlc1 block a phosphorylation/activation event required to regulate Ccnd1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Sptlc1 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Ccnd1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Sptlc1?
      Could loss of Sptlc1 lead to upregulation of Ccnd1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Sptlc1 and Ccnd1 protein products members of the same complex?
      If Sptlc1 is knocked down, does Ccnd1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Sptlc1 and Ccnd1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Sptlc1 directly controls Ccnd1
  [ 2. Indirect Path ] — Sptlc1 affects Ccnd1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Ccnd1
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
