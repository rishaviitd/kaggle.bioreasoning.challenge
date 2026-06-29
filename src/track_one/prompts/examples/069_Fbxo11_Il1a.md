# Example 069: `Fbxo11_Il1a`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Fbxo11` |
| **Gene of interest** | `Il1a` |
| **Ground-truth label** | `DOWN` — B) down-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Fbxo11
Gene of interest: Il1a

Predict the effect of CRISPRi knockdown of Fbxo11 on Il1a:
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
      What is the primary biochemical class of Fbxo11 and Il1a?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Fbxo11 and Il1a reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Fbxo11 and Il1a proteins physically assemble into a complex?
      If yes, is Il1a dependent on Fbxo11 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Fbxo11 directly regulate transcription of Il1a?
      (Is Fbxo11 a known TF/co-factor that binds the Il1a promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Fbxo11 and Il1a in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Fbxo11 affect Il1a?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Fbxo11 directly activate or repress Il1a expression?
      Knocking down Fbxo11 — does it remove a known activator or a known repressor of Il1a?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Fbxo11 upstream of Il1a in a defined signaling pathway?
      Does loss of Fbxo11 block a phosphorylation/activation event required to regulate Il1a?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Fbxo11 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Il1a expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Fbxo11?
      Could loss of Fbxo11 lead to upregulation of Il1a as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Fbxo11 and Il1a protein products members of the same complex?
      If Fbxo11 is knocked down, does Il1a protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Fbxo11 and Il1a in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Fbxo11 directly controls Il1a
  [ 2. Indirect Path ] — Fbxo11 affects Il1a through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Il1a
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
