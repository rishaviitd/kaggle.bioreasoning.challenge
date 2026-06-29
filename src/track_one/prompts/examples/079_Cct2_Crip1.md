# Example 079: `Cct2_Crip1`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Cct2` |
| **Gene of interest** | `Crip1` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Cct2
Gene of interest: Crip1

Predict the effect of CRISPRi knockdown of Cct2 on Crip1:
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
      What is the primary biochemical class of Cct2 and Crip1?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Cct2 and Crip1 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Cct2 and Crip1 proteins physically assemble into a complex?
      If yes, is Crip1 dependent on Cct2 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Cct2 directly regulate transcription of Crip1?
      (Is Cct2 a known TF/co-factor that binds the Crip1 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Cct2 and Crip1 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Cct2 affect Crip1?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Cct2 directly activate or repress Crip1 expression?
      Knocking down Cct2 — does it remove a known activator or a known repressor of Crip1?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Cct2 upstream of Crip1 in a defined signaling pathway?
      Does loss of Cct2 block a phosphorylation/activation event required to regulate Crip1?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Cct2 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Crip1 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Cct2?
      Could loss of Cct2 lead to upregulation of Crip1 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Cct2 and Crip1 protein products members of the same complex?
      If Cct2 is knocked down, does Crip1 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Cct2 and Crip1 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Cct2 directly controls Crip1
  [ 2. Indirect Path ] — Cct2 affects Crip1 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Crip1
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
