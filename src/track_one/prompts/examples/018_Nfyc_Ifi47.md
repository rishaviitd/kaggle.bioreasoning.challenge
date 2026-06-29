# Example 018: `Nfyc_Ifi47`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Nfyc` |
| **Gene of interest** | `Ifi47` |
| **Ground-truth label** | `NONE` — C) no significant effect |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Nfyc
Gene of interest: Ifi47

Predict the effect of CRISPRi knockdown of Nfyc on Ifi47:
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
      What is the primary biochemical class of Nfyc and Ifi47?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Nfyc and Ifi47 reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Nfyc and Ifi47 proteins physically assemble into a complex?
      If yes, is Ifi47 dependent on Nfyc for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Nfyc directly regulate transcription of Ifi47?
      (Is Nfyc a known TF/co-factor that binds the Ifi47 promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Nfyc and Ifi47 in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Nfyc affect Ifi47?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Nfyc directly activate or repress Ifi47 expression?
      Knocking down Nfyc — does it remove a known activator or a known repressor of Ifi47?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Nfyc upstream of Ifi47 in a defined signaling pathway?
      Does loss of Nfyc block a phosphorylation/activation event required to regulate Ifi47?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Nfyc trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Ifi47 expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Nfyc?
      Could loss of Nfyc lead to upregulation of Ifi47 as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Nfyc and Ifi47 protein products members of the same complex?
      If Nfyc is knocked down, does Ifi47 protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Nfyc and Ifi47 in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Nfyc directly controls Ifi47
  [ 2. Indirect Path ] — Nfyc affects Ifi47 through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Ifi47
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
