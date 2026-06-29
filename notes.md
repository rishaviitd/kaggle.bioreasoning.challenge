Phase 1: Primitive Identity Questions (The "What")Before analyzing the interaction, the expert establishes the basic identity of each player.What is the baseline function of the Perturbed Gene (Gene X)?Biologist's thoughts: Is it a transcription factor (turns genes on/off)? An enzyme? A structural protein? A membrane transporter?Example (Slc35b1): It is a solute carrier transporter located in the endoplasmic reticulum (ER) membrane.What is the baseline function of the Target Gene (Gene Y)?Biologist's thoughts: What is its everyday job in the cell?Example (Pdia6): It is a protein disulfide isomerase. Its job is folding proteins inside the ER and managing ER stress.Where do they live? (Cellular Localization)Biologist's thoughts: Are they even in the same room? If Gene X is in the nucleus and Gene Y is outside the cell, a direct interaction is impossible.Example: Both Slc35b1 and Pdia6 operate in the Endoplasmic Reticulum. This shared location instantly triggers high suspicion of a connection.Phase 2: Relational Questions (The "How")Next, the expert looks for existing cellular highways connecting the two genes.Are they in the same biological pathway?Biologist's thoughts: Do they work together to achieve a single goal (e.g., cell division, metabolic breakdown, immune response)?Is there physical contact (Protein-Protein Interaction)?Biologist's thoughts: Do these two proteins physically bind to each other to form a molecular machine?Is Gene X a known regulator of Gene Y?Biologist's thoughts: Does literature show that Gene X directly binds to the promoter/enhancer region of Gene Y?Phase 3: Knockdown Mechanics & Directional Logic (The "Why")This is where the expert applies the specific constraint of a knockdown (reducing the expression of Gene X) to predict the outcome. They ask:"If I break Gene X, what goes wrong in the cell?"Biologist's thoughts on the example: If I knock down the transporter Slc35b1, transport into the ER fails. This will cause un-folded proteins to pile up, causing severe ER stress."How does Gene Y naturally respond to that specific stress?"Biologist's thoughts: Gene Y (Pdia6) handles ER stress. If ER stress spikes because Gene X is broken, the cell will desperately try to survive by producing more Pdia6 to fix the unfolded proteins.Conclusion Mapping:Breaking Gene X causes a stressful condition → The cell turns up Gene Y to fight the stress → Prediction: up.

To build an exhaustive framework that serves as an unshakeable guiding principle for an LLM, we must turn these questions into a highly structured, mutually exclusive, and collectively exhaustive (MECE) diagnostic tree.
In biology, when you knock down a gene, things go wrong in highly predictable ways. By breaking down the generalized question "If I break Gene X, what goes wrong in the cell?" into functional categories, we cover every possible reason a target gene would react.
Here is the exhaustive, generalized question framework an expert systems biologist uses, designed to be plugged directly into your prompt.

---

## Phase 1: Exhaustive Primitive Identity (The "What")

Before looking at connections, establish the precise molecular profile of each gene.

- Q1.1: Functional Classification – What is the primary biochemical class of Gene X and Gene Y?
- Is it a Transcription Factor (direct DNA binding), Epigenetic Modifier, RNA-binding protein, Kinase/Phosphatase (signaling), Metabolic Enzyme, Structural Protein, Membrane Receptor, Transporter, or Uncharacterized Open Reading Frame (e.g., Riken/LOC genes)?
- Q1.2: Absolute Subcellular Compartmentalization – Where do the mature proteins reside?
- Nucleus, Nucleolus, Cytoplasm, Plasma Membrane, Endoplasmic Reticulum, Golgi Apparatus, Mitochondria, Lysosome/Peroxisome, or Secreted Extracellularly?
- Q1.3: Tissue/Cell-Line Context Baseline – What is the native expression status of both genes in this specific cell type?
- Are they ubiquitously expressed (housekeeping), highly cell-type specific, or normally silent until induced by stress?

---

## Phase 2: Exhaustive Relational Topology (The "How")

Map every possible biological highway or structural link between the two entities.

- Q2.1: Physical Interaction (Interactome) – Do the proteins physically assemble?
- Are they subunits of the same stable multi-protein complex, or do they exhibit transient binary physical contact (Protein-Protein Interaction)?
- Q2.2: Regulatory Hierarchy (Direct Transcription) – Does a direct command structure exist?
- Does Gene X bind to the promoter, enhancer, or locus control region of Gene Y? Does it modify the chromatin accessibility (methylation/acetylation) at Gene Y’s locus?
- Q2.3: Co-Pathway Membership (Metabolic/Signaling) – Are they workers on the same assembly line?
- Are they part of the same canonical signaling pathway (e.g., MAPK, Wnt, JAK/STAT) or metabolic cascade? Do they share identical Gene Ontology (GO) biological process terms?

---

## Phase 3: Exhaustive Perturbation Mechanics (The "Why")

This is the core expansion of "If I break Gene X, what goes wrong?" broken down into generalized biological failure modes.
When Gene X is knocked down, it causes a failure. The target Gene Y responds to that failure. Look through these 5 exhaustive categories to find the mechanism:

## Category A: Direct Information Flow Failure (The Command Chain)

- Generalized Question: Did we destroy the direct switch that controls Gene Y?
- If Gene X is a known transcription activator/inducer of Gene Y: Its loss removes the activation signal $\rightarrow$ Prediction: down
  - If Gene X is a known transcription repressor/silencer of Gene Y: Its loss removes the brake, causing spontaneous expression $\rightarrow$ Prediction: up

## Category B: Linear Signaling Cascade Disruption (The Telephone Game)

- Generalized Question: Did we cut the wire upstream of Gene Y in a signaling path?
- If Gene X is an upstream positive activator (e.g., a kinase) in a pathway that ends in turning Gene Y on: Knocking it down halts the signal before it reaches Gene Y $\rightarrow$ Prediction: down
  - If Gene X is a negative regulator (e.g., a phosphatase) that normally shuts off the pathway activating Gene Y: Knocking it down leaves the pathway permanently turned "on" $\rightarrow$ Prediction: up

## Category C: Organelle Homeostasis & Cellular Stress (The Emergency Response)

- Generalized Question: Does losing Gene X cause a physical crisis (stress) in a specific cellular compartment that Gene Y is designed to fix?
- If Gene X maintains organelle stability (e.g., ER folding, mitochondrial polarization, lysosomal acidity) and its loss causes organelle stress: The cell will upregulate stress-response genes (Gene Y) located in that same organelle to prevent cell death $\rightarrow$ Prediction: up

## Category D: Functional Redundancy & Genetic Compensation (The Back-Up Plan)

- Generalized Question: Are Gene X and Gene Y structural twins or paralogs?
- If Gene X and Gene Y perform the exact same biochemical backup function (paralogs): Knocking down Gene X creates a functional void. The cell will sense this lack of activity and overexpress Gene Y to compensate and take over the workload $\rightarrow$ Prediction: up

## Category E: Complex Stability & Degradation (The House of Cards)

- Generalized Question: Does Gene Y depend physically on Gene X to survive or stay clean?
- If Gene X is a protective chaperone or mandatory stabilization subunit of a complex containing Gene Y: Without Gene X, Gene Y becomes unstable, misfolds, or is rapidly degraded by the proteasome $\rightarrow$ Prediction: down
  - If Gene X is a component of the degradation machinery (e.g., an E3 ubiquitin ligase) that targets Gene Y for destruction: Knocking down Gene X prevents Gene Y from being degraded, causing it to accumulate $\rightarrow$ Prediction: up

## Category F: Null Topology (No Functional Link)

- Generalized Question: Are they completely isolated from one another?
- If Gene X and Gene Y share no common compartments, have no direct or indirect pathway connections, do not share paralogous functions, and the loss of Gene X creates no stress that impacts Gene Y's domain: The perturbation has no effect $\rightarrow$ Prediction: no-change

---

## Framework Integration for Your Prompt

You can feed this exact breakdown to your LLM. By forcing it to explicitly classify the interaction into one of these Category A-F mechanisms, you eliminate random guessing.

### Exhaustive Mechanistic Decision Tree

Evaluate the knockdown of Gene X on Gene Y by selecting exactly ONE primary mechanism from this exhaustive checklist:

- Category A (Direct Switch): X is a direct transcriptional activator [down] or repressor [up] of Y.
- Category B (Signaling Wire): X is an upstream positive pathway component [down] or negative component [up] relative to Y.
- Category C (Organelle Stress): X's loss causes local organelle failure, forcing Y (a stress-rescue gene in that compartment) to adapt [up].
- Category D (Paralog Compensation): X and Y are functional duplicates; losing X forces Y to ramp up to substitute [up].
- Category E (Physical Stability): X physically protects Y from degradation [down], or X is part of the machinery that destroys Y [up].
- Category F (Null Topology): No direct/indirect functional, physical, pathways, or stress link exists between X and Y [no-change].

To continue building this out, let me know:

- Would you like me to translate this exhaustive framework into a fully structured prompt template with a designated Chain-of-Thought parsing area?
- Do you want to discuss how to instruct the LLM to handle uncharacterised "Riken" genes (like 9930111J21Rik2), which often map to Category F unless structural domain data is extracted?
- Should we evaluate how to format few-shot examples using these exact mechanistic categories?
