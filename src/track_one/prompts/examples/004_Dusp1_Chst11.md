# Example 004: `Dusp1_Chst11`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Dusp1` |
| **Gene of interest** | `Chst11` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Dusp1
Gene of interest: Chst11

Predict the effect of CRISPRi knockdown of Dusp1 on Chst11:
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
      What is the primary biochemical class of Dusp1 and Chst11?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Dusp1 and Chst11 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Dusp1 and Chst11 proteins physically assemble into a complex?
      If yes, is Chst11 dependent on Dusp1 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Dusp1 directly regulate transcription of Chst11?
      (Is Dusp1 a known TF/co-factor that binds the Chst11 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Dusp1 and Chst11 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Dusp1 affect Chst11?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Dusp1 directly activate or repress Chst11 expression?
      Knocking down Dusp1 — does it remove a known activator or a known repressor of Chst11?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Dusp1 upstream of Chst11 in a defined signaling pathway?
      Does loss of Dusp1 block a phosphorylation/activation event required to regulate Chst11?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Dusp1 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Chst11 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Dusp1?
      Could loss of Dusp1 lead to upregulation of Chst11 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Dusp1 and Chst11 protein products members of the same complex?
      If Dusp1 is knocked down, does Chst11 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Dusp1 and Chst11 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Dusp1 directly controls Chst11
  [ 2. Indirect Path ] — Dusp1 affects Chst11 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Chst11
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
