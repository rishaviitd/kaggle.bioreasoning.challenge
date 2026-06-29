# Example 047: `Pfn1_Hp`

| Field | Value |
|-------|-------|
| **Perturbation (pert)** | `Pfn1` |
| **Gene of interest** | `Hp` |
| **Ground-truth label** | `DOWN` — B) down-regulated |

---

## Prompt

```
You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from
bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived
macrophages (BMDMs).

Perturbation: Pfn1
Gene of interest: Hp

Predict the effect of CRISPRi knockdown of Pfn1 on Hp:
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
      What is the primary biochemical class of Pfn1 and Hp?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of Pfn1 and Hp reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do Pfn1 and Hp proteins physically assemble into a complex?
      If yes, is Hp dependent on Pfn1 for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does Pfn1 directly regulate transcription of Hp?
      (Is Pfn1 a known TF/co-factor that binds the Hp promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are Pfn1 and Hp in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of Pfn1 affect Hp?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does Pfn1 directly activate or repress Hp expression?
      Knocking down Pfn1 — does it remove a known activator or a known repressor of Hp?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is Pfn1 upstream of Hp in a defined signaling pathway?
      Does loss of Pfn1 block a phosphorylation/activation event required to regulate Hp?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of Pfn1 trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter Hp expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of Pfn1?
      Could loss of Pfn1 lead to upregulation of Hp as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are Pfn1 and Hp protein products members of the same complex?
      If Pfn1 is knocked down, does Hp protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are Pfn1 and Hp in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes
the relationship:

  [ 1. Direct Edge ]  — Pfn1 directly controls Hp
  [ 2. Indirect Path ] — Pfn1 affects Hp through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches Hp
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
