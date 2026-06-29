# Example 025: `Arpc3_Gsto1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Arpc3` |
| **Gene of interest** | `Gsto1` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Arpc3
Gene of interest: Gsto1

Predict the effect of CRISPRi knockdown of Arpc3 on Gsto1:
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
      What is the primary biochemical class of Arpc3 and Gsto1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Arpc3 and Gsto1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Arpc3 and Gsto1 proteins physically assemble into a complex?
      If yes, is Gsto1 dependent on Arpc3 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Arpc3 directly regulate transcription of Gsto1?
      (Is Arpc3 a known TF/co-factor that binds the Gsto1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Arpc3 and Gsto1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Arpc3 affect Gsto1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Arpc3 directly activate or repress Gsto1 expression?
      Knocking down Arpc3 — does it remove a known activator or a known repressor of Gsto1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Arpc3 upstream of Gsto1 in a defined signaling pathway?
      Does loss of Arpc3 block a phosphorylation/activation event required to regulate Gsto1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Arpc3 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Gsto1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Arpc3?
      Could loss of Arpc3 lead to upregulation of Gsto1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Arpc3 and Gsto1 protein products members of the same complex?
      If Arpc3 is knocked down, does Gsto1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Arpc3 and Gsto1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Arpc3 directly controls Gsto1
  [ 2. Indirect Path ] — Arpc3 affects Gsto1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Gsto1
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
