# Example 008: `Junb_Carhsp1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Junb` |
| **Gene of interest** | `Carhsp1` |
| **Ground-truth label** | `DOWN` — B) down-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Junb
Gene of interest: Carhsp1

Predict the effect of CRISPRi knockdown of Junb on Carhsp1:
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
      What is the primary biochemical class of Junb and Carhsp1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Junb and Carhsp1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Junb and Carhsp1 proteins physically assemble into a complex?
      If yes, is Carhsp1 dependent on Junb for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Junb directly regulate transcription of Carhsp1?
      (Is Junb a known TF/co-factor that binds the Carhsp1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Junb and Carhsp1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Junb affect Carhsp1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Junb directly activate or repress Carhsp1 expression?
      Knocking down Junb — does it remove a known activator or a known repressor of Carhsp1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Junb upstream of Carhsp1 in a defined signaling pathway?
      Does loss of Junb block a phosphorylation/activation event required to regulate Carhsp1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Junb trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Carhsp1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Junb?
      Could loss of Junb lead to upregulation of Carhsp1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Junb and Carhsp1 protein products members of the same complex?
      If Junb is knocked down, does Carhsp1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Junb and Carhsp1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Junb directly controls Carhsp1
  [ 2. Indirect Path ] — Junb affects Carhsp1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Carhsp1
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
