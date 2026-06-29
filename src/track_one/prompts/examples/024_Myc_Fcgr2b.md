# Example 024: `Myc_Fcgr2b`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Myc` |
| **Gene of interest** | `Fcgr2b` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Myc
Gene of interest: Fcgr2b

Predict the effect of CRISPRi knockdown of Myc on Fcgr2b:
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
      What is the primary biochemical class of Myc and Fcgr2b?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Myc and Fcgr2b reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Myc and Fcgr2b proteins physically assemble into a complex?
      If yes, is Fcgr2b dependent on Myc for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Myc directly regulate transcription of Fcgr2b?
      (Is Myc a known TF/co-factor that binds the Fcgr2b promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Myc and Fcgr2b in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Myc affect Fcgr2b?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Myc directly activate or repress Fcgr2b expression?
      Knocking down Myc — does it remove a known activator or a known repressor of Fcgr2b?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Myc upstream of Fcgr2b in a defined signaling pathway?
      Does loss of Myc block a phosphorylation/activation event required to regulate Fcgr2b?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Myc trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Fcgr2b expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Myc?
      Could loss of Myc lead to upregulation of Fcgr2b as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Myc and Fcgr2b protein products members of the same complex?
      If Myc is knocked down, does Fcgr2b protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Myc and Fcgr2b in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Myc directly controls Fcgr2b
  [ 2. Indirect Path ] — Myc affects Fcgr2b through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Fcgr2b
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
