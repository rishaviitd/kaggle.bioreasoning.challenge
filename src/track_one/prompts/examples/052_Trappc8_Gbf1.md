# Example 052: `Trappc8_Gbf1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Trappc8` |
| **Gene of interest** | `Gbf1` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Trappc8
Gene of interest: Gbf1

Predict the effect of CRISPRi knockdown of Trappc8 on Gbf1:
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
      What is the primary biochemical class of Trappc8 and Gbf1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Trappc8 and Gbf1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Trappc8 and Gbf1 proteins physically assemble into a complex?
      If yes, is Gbf1 dependent on Trappc8 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Trappc8 directly regulate transcription of Gbf1?
      (Is Trappc8 a known TF/co-factor that binds the Gbf1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Trappc8 and Gbf1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Trappc8 affect Gbf1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Trappc8 directly activate or repress Gbf1 expression?
      Knocking down Trappc8 — does it remove a known activator or a known repressor of Gbf1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Trappc8 upstream of Gbf1 in a defined signaling pathway?
      Does loss of Trappc8 block a phosphorylation/activation event required to regulate Gbf1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Trappc8 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Gbf1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Trappc8?
      Could loss of Trappc8 lead to upregulation of Gbf1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Trappc8 and Gbf1 protein products members of the same complex?
      If Trappc8 is knocked down, does Gbf1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Trappc8 and Gbf1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Trappc8 directly controls Gbf1
  [ 2. Indirect Path ] — Trappc8 affects Gbf1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Gbf1
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
