PROMPT_V1 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived macrophages (BMDMs).

### BIOLOGICAL REASONING FRAMEWORK
You are predicting the effect of a CRISPRi knockdown of a Perturbation Gene (Gene A) on a Target Gene (Gene B) in resting (M0) mouse bone marrow-derived macrophages (BMDMs). 

**Core Premise:** CRISPRi reduces the expression of Gene A (Loss of Function). You must determine how the loss of Gene A impacts Gene B. Ground-truth labels are strict (|log2FC| >= log2(1.5)); therefore, weak, indirect, or buffered connections should be classified as `none`.

**EXECUTION CONSTRAINT:** In your thought process, you MUST first construct a "Simulated Biological Knowledge Graph" and then evaluate ALL 10 steps of the Decision Tree in order before giving your final answer.

**Part 1: Simulated Biological Knowledge Graph**
Write down a structured mapping of known relationships before reasoning:
- **Node A (Perturbation):** [Gene A Name] -> [Primary GO Process] -> [Subcellular Location] -> [Basal expression state in M0 macrophages: Active/Repressing/Dormant]
- **Node B (Target):** [Gene B Name] -> [Primary GO Process] -> [Subcellular Location] -> [Basal expression state in M0 macrophages: Expressed/Off]
- **Direct Edges (Max 2 steps):** [List known STRING database interactions or KEGG pathway links connecting A and B, e.g., "A activates C, C represses B"]

**Part 2: Strict Decision Tree**

1. **Check for Paralogy (Compensation):** 
   - Are Gene A and Gene B paralogs or highly similar family members?
   - *Rule:* If YES, predict `up` (the cell upregulates B to compensate for the loss of A).

2. **Check for Shared Protein Complex (Co-regulation):**
   - Are Gene A and Gene B subunits of the exact same protein complex?
   - *Rule:* If YES, predict `down` (loss of one subunit usually destabilizes the complex and co-regulates the other subunit down).

3. **Check Epigenetic / Global Regulators:**
   - Is Gene A a global chromatin modifier (e.g., HDAC, DNMT, HAT, SWI/SNF)?
   - *Rule:* If A is a global repressor/silencer (e.g., HDAC) -> predict `up` (loss of silencing).
   - *Rule:* If A is a global activator (e.g., HAT) -> predict `down` (loss of activation).

4. **Check Core Essential / Global Stress:**
   - Is Gene A a core essential lethality gene (e.g., ribosomal subunit, core proteasome, RNA polymerase)?
   - *Rule:* If YES, and B is a stress-response or apoptosis gene (e.g., chaperone, p53 target) -> predict `up`.
   - *Rule:* If YES, and B is a cell-cycle/proliferation gene -> predict `down`.

5. **Check Metabolic Pathway Coupling:**
   - Are Gene A and Gene B enzymes in the exact same linear metabolic pathway?
   - *Rule:* If A is upstream and its loss starves B of substrate, the pathway is abandoned -> predict `down`.
   - *Rule:* If loss of A causes a toxic metabolite buildup that stresses the cell, and B is a stress-response gene -> predict `up`.

6. **Check Feedback Loops:**
   - Is Gene B an established *negative feedback regulator* of Gene A's primary pathway (e.g., SOCS for JAK/STAT)?
   - *Rule:* If YES, predict `down` (loss of A removes the pathway signal that normally induces the feedback loop).

7. **Check Direct Transcriptional / Signaling Links (1-2 steps):**
   - Is Gene A a transcription factor, kinase, or receptor that leads to Gene B's expression? Or is there an immediate intermediary (A -> C -> B)?
   - *Rule for Activators:* If A is an ACTIVATOR of B: Check B's basal expression. If B is expressed basally -> predict `down`. If B is normally "off" -> predict `none` (you cannot lower an unexpressed gene).
   - *Rule for Repressors:* If A is a REPRESSOR of B -> predict `up` (loss of repressor = "de-repression", turning it 'on').
   - *Macrophage Inflammatory Context Rule:* If A is an inflammatory activator (e.g., NF-kB component) and B is an inflammatory cytokine, since the cell is resting (M0), B is already off -> predict `none`. If A is a basal repressor of inflammation, predict `up` for inflammatory targets.

8. **Apply the Biological Distance Threshold:**
   - Based on your Simulated Knowledge Graph, is the distance strictly greater than 2 edges (e.g., A -> C -> D -> B)?
   - *Rule:* If YES, predict `none`. In biological networks, effects >2 steps away are buffered by cellular noise and compensatory mechanisms, failing to meet the strict 5% FDR and log2(1.5) fold-change threshold.

9. **Housekeeping Gene Buffering Check & Default:**
    - Is Gene B a Housekeeping Gene (HEG) (e.g., Actb, Gapdh)? HEGs are highly buffered against non-essential perturbations.
    - *Rule:* If Gene B is an HEG and Gene A is NOT a core essential gene -> predict `none`.
    - If no other specific rules above apply -> predict `none`.

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPRi knockdown of {pert} on {gene}:
  A) Up-regulated.
  B) Down-regulated.
  C) No significant effect.

Think step by step, then provide your final answer.
Answer:"""
