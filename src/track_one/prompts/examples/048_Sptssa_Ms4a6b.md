# Example 048: `Sptssa_Ms4a6b`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Sptssa` |
| **Gene of interest** | `Ms4a6b` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Sptssa
Gene of interest: Ms4a6b

Predict the effect of CRISPRi knockdown of Sptssa on Ms4a6b:
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
      What is the primary biochemical class of Sptssa and Ms4a6b?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Sptssa and Ms4a6b reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Sptssa and Ms4a6b proteins physically assemble into a complex?
      If yes, is Ms4a6b dependent on Sptssa for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Sptssa directly regulate transcription of Ms4a6b?
      (Is Sptssa a known TF/co-factor that binds the Ms4a6b promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Sptssa and Ms4a6b in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Sptssa affect Ms4a6b?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Sptssa directly activate or repress Ms4a6b expression?
      Knocking down Sptssa — does it remove a known activator or a known repressor of Ms4a6b?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Sptssa upstream of Ms4a6b in a defined signaling pathway?
      Does loss of Sptssa block a phosphorylation/activation event required to regulate Ms4a6b?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Sptssa trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Ms4a6b expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Sptssa?
      Could loss of Sptssa lead to upregulation of Ms4a6b as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Sptssa and Ms4a6b protein products members of the same complex?
      If Sptssa is knocked down, does Ms4a6b protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Sptssa and Ms4a6b in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Sptssa directly controls Ms4a6b
  [ 2. Indirect Path ] — Sptssa affects Ms4a6b through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Ms4a6b
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
