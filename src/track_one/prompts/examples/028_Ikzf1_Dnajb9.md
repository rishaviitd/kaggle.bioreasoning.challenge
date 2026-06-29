# Example 028: `Ikzf1_Dnajb9`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Ikzf1` |
| **Gene of interest** | `Dnajb9` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Ikzf1
Gene of interest: Dnajb9

Predict the effect of CRISPRi knockdown of Ikzf1 on Dnajb9:
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
      What is the primary biochemical class of Ikzf1 and Dnajb9?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Ikzf1 and Dnajb9 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Ikzf1 and Dnajb9 proteins physically assemble into a complex?
      If yes, is Dnajb9 dependent on Ikzf1 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Ikzf1 directly regulate transcription of Dnajb9?
      (Is Ikzf1 a known TF/co-factor that binds the Dnajb9 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Ikzf1 and Dnajb9 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Ikzf1 affect Dnajb9?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Ikzf1 directly activate or repress Dnajb9 expression?
      Knocking down Ikzf1 — does it remove a known activator or a known repressor of Dnajb9?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Ikzf1 upstream of Dnajb9 in a defined signaling pathway?
      Does loss of Ikzf1 block a phosphorylation/activation event required to regulate Dnajb9?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Ikzf1 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Dnajb9 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Ikzf1?
      Could loss of Ikzf1 lead to upregulation of Dnajb9 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Ikzf1 and Dnajb9 protein products members of the same complex?
      If Ikzf1 is knocked down, does Dnajb9 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Ikzf1 and Dnajb9 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Ikzf1 directly controls Dnajb9
  [ 2. Indirect Path ] — Ikzf1 affects Dnajb9 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Dnajb9
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
