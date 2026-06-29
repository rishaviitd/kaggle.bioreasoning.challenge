# Example 006: `Chmp6_Trmt10c`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Chmp6` |
| **Gene of interest** | `Trmt10c` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Chmp6
Gene of interest: Trmt10c

Predict the effect of CRISPRi knockdown of Chmp6 on Trmt10c:
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
      What is the primary biochemical class of Chmp6 and Trmt10c?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Chmp6 and Trmt10c reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Chmp6 and Trmt10c proteins physically assemble into a complex?
      If yes, is Trmt10c dependent on Chmp6 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Chmp6 directly regulate transcription of Trmt10c?
      (Is Chmp6 a known TF/co-factor that binds the Trmt10c promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Chmp6 and Trmt10c in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Chmp6 affect Trmt10c?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Chmp6 directly activate or repress Trmt10c expression?
      Knocking down Chmp6 — does it remove a known activator or a known repressor of Trmt10c?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Chmp6 upstream of Trmt10c in a defined signaling pathway?
      Does loss of Chmp6 block a phosphorylation/activation event required to regulate Trmt10c?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Chmp6 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Trmt10c expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Chmp6?
      Could loss of Chmp6 lead to upregulation of Trmt10c as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Chmp6 and Trmt10c protein products members of the same complex?
      If Chmp6 is knocked down, does Trmt10c protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Chmp6 and Trmt10c in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Chmp6 directly controls Trmt10c
  [ 2. Indirect Path ] — Chmp6 affects Trmt10c through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Trmt10c
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
