# Example 075: `Cnot1_Trem2`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Cnot1` |
| **Gene of interest** | `Trem2` |
| **Ground-truth label** | `UP` — A) up-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Cnot1
Gene of interest: Trem2

Predict the effect of CRISPRi knockdown of Cnot1 on Trem2:
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
      What is the primary biochemical class of Cnot1 and Trem2?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Cnot1 and Trem2 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Cnot1 and Trem2 proteins physically assemble into a complex?
      If yes, is Trem2 dependent on Cnot1 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Cnot1 directly regulate transcription of Trem2?
      (Is Cnot1 a known TF/co-factor that binds the Trem2 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Cnot1 and Trem2 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Cnot1 affect Trem2?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Cnot1 directly activate or repress Trem2 expression?
      Knocking down Cnot1 — does it remove a known activator or a known repressor of Trem2?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Cnot1 upstream of Trem2 in a defined signaling pathway?
      Does loss of Cnot1 block a phosphorylation/activation event required to regulate Trem2?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Cnot1 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Trem2 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Cnot1?
      Could loss of Cnot1 lead to upregulation of Trem2 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Cnot1 and Trem2 protein products members of the same complex?
      If Cnot1 is knocked down, does Trem2 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Cnot1 and Trem2 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Cnot1 directly controls Trem2
  [ 2. Indirect Path ] — Cnot1 affects Trem2 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Trem2
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
