# Example 020: `Pik3c3_Gpnmb`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Pik3c3` |
| **Gene of interest** | `Gpnmb` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Pik3c3
Gene of interest: Gpnmb

Predict the effect of CRISPRi knockdown of Pik3c3 on Gpnmb:
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
      What is the primary biochemical class of Pik3c3 and Gpnmb?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Pik3c3 and Gpnmb reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Pik3c3 and Gpnmb proteins physically assemble into a complex?
      If yes, is Gpnmb dependent on Pik3c3 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Pik3c3 directly regulate transcription of Gpnmb?
      (Is Pik3c3 a known TF/co-factor that binds the Gpnmb promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Pik3c3 and Gpnmb in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Pik3c3 affect Gpnmb?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Pik3c3 directly activate or repress Gpnmb expression?
      Knocking down Pik3c3 — does it remove a known activator or a known repressor of Gpnmb?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Pik3c3 upstream of Gpnmb in a defined signaling pathway?
      Does loss of Pik3c3 block a phosphorylation/activation event required to regulate Gpnmb?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Pik3c3 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Gpnmb expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Pik3c3?
      Could loss of Pik3c3 lead to upregulation of Gpnmb as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Pik3c3 and Gpnmb protein products members of the same complex?
      If Pik3c3 is knocked down, does Gpnmb protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Pik3c3 and Gpnmb in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Pik3c3 directly controls Gpnmb
  [ 2. Indirect Path ] — Pik3c3 affects Gpnmb through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Gpnmb
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
