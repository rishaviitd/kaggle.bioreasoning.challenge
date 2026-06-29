# Example 026: `Chmp3_Hilpda`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Chmp3` |
| **Gene of interest** | `Hilpda` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Chmp3
Gene of interest: Hilpda

Predict the effect of CRISPRi knockdown of Chmp3 on Hilpda:
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
      What is the primary biochemical class of Chmp3 and Hilpda?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Chmp3 and Hilpda reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Chmp3 and Hilpda proteins physically assemble into a complex?
      If yes, is Hilpda dependent on Chmp3 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Chmp3 directly regulate transcription of Hilpda?
      (Is Chmp3 a known TF/co-factor that binds the Hilpda promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Chmp3 and Hilpda in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Chmp3 affect Hilpda?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Chmp3 directly activate or repress Hilpda expression?
      Knocking down Chmp3 — does it remove a known activator or a known repressor of Hilpda?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Chmp3 upstream of Hilpda in a defined signaling pathway?
      Does loss of Chmp3 block a phosphorylation/activation event required to regulate Hilpda?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Chmp3 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Hilpda expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Chmp3?
      Could loss of Chmp3 lead to upregulation of Hilpda as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Chmp3 and Hilpda protein products members of the same complex?
      If Chmp3 is knocked down, does Hilpda protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Chmp3 and Hilpda in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Chmp3 directly controls Hilpda
  [ 2. Indirect Path ] — Chmp3 affects Hilpda through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Hilpda
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
