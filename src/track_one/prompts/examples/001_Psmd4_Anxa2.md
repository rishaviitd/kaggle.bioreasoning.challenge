# Example 001: `Psmd4_Anxa2`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Psmd4` |
| **Gene of interest** | `Anxa2` |
| **Ground-truth label** | `DOWN` — B) down-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Psmd4
Gene of interest: Anxa2

Predict the effect of CRISPRi knockdown of Psmd4 on Anxa2:
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
      What is the primary biochemical class of Psmd4 and Anxa2?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Psmd4 and Anxa2 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Psmd4 and Anxa2 proteins physically assemble into a complex?
      If yes, is Anxa2 dependent on Psmd4 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Psmd4 directly regulate transcription of Anxa2?
      (Is Psmd4 a known TF/co-factor that binds the Anxa2 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Psmd4 and Anxa2 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Psmd4 affect Anxa2?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Psmd4 directly activate or repress Anxa2 expression?
      Knocking down Psmd4 — does it remove a known activator or a known repressor of Anxa2?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Psmd4 upstream of Anxa2 in a defined signaling pathway?
      Does loss of Psmd4 block a phosphorylation/activation event required to regulate Anxa2?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Psmd4 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Anxa2 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Psmd4?
      Could loss of Psmd4 lead to upregulation of Anxa2 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Psmd4 and Anxa2 protein products members of the same complex?
      If Psmd4 is knocked down, does Anxa2 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Psmd4 and Anxa2 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Psmd4 directly controls Anxa2
  [ 2. Indirect Path ] — Psmd4 affects Anxa2 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Anxa2
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
