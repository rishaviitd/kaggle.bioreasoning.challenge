# Example 017: `Wdr1_Vcl`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Wdr1` |
| **Gene of interest** | `Vcl` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Wdr1
Gene of interest: Vcl

Predict the effect of CRISPRi knockdown of Wdr1 on Vcl:
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
      What is the primary biochemical class of Wdr1 and Vcl?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Wdr1 and Vcl reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Wdr1 and Vcl proteins physically assemble into a complex?
      If yes, is Vcl dependent on Wdr1 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Wdr1 directly regulate transcription of Vcl?
      (Is Wdr1 a known TF/co-factor that binds the Vcl promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Wdr1 and Vcl in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Wdr1 affect Vcl?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Wdr1 directly activate or repress Vcl expression?
      Knocking down Wdr1 — does it remove a known activator or a known repressor of Vcl?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Wdr1 upstream of Vcl in a defined signaling pathway?
      Does loss of Wdr1 block a phosphorylation/activation event required to regulate Vcl?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Wdr1 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Vcl expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Wdr1?
      Could loss of Wdr1 lead to upregulation of Vcl as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Wdr1 and Vcl protein products members of the same complex?
      If Wdr1 is knocked down, does Vcl protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Wdr1 and Vcl in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Wdr1 directly controls Vcl
  [ 2. Indirect Path ] — Wdr1 affects Vcl through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Vcl
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
