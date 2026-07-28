PROMPT_V0 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPRi knockdown of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section.

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:"""

PROMPT_V1 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPRi knockdown experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPRi knockdown of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Think step by step in the reasoning section. Use the structured framework below to guide your analysis. You do not need to answer every question — use whichever are relevant to reach a well-justified conclusion.

─────────────────────────────────────────────────────────────────────────────
REASONING FRAMEWORK
─────────────────────────────────────────────────────────────────────────────

PHASE 1 — PRIMITIVE IDENTITY (What are these genes?)

  1.1 Functional Classification
      What is the primary biochemical class of {pert} and {gene}?
      (e.g., transcription factor, kinase, metabolic enzyme, structural protein, receptor)

  1.2 Subcellular Compartmentalization
      Where do the mature proteins of {pert} and {gene} reside?
      (nucleus, cytoplasm, membrane, secreted, organelle-specific)

  1.3 Tissue & Cell-Type Baseline
      What is the native expression status of both genes in BMDMs specifically?
      Are they constitutively expressed, inducible, or lowly expressed in this context?

─────────────────────────────────────────────────────────────────────────────

PHASE 2 — RELATIONAL TOPOLOGY (How are they connected?)

  2.1 Physical Interaction (Interactome)
      Do {pert} and {gene} proteins physically assemble into a complex?
      If yes, is {gene} dependent on {pert} for stability or localization?

  2.2 Regulatory Hierarchy (Direct Transcription)
      Does {pert} directly regulate transcription of {gene}?
      (Is {pert} a known TF/co-factor that binds the {gene} promoter or enhancer?)

  2.3 Co-Pathway Membership (Signaling / Metabolic)
      Are {pert} and {gene} in the same signaling or metabolic pathway?
      If yes, what is the relationship — linear, parallel, feedback?

─────────────────────────────────────────────────────────────────────────────

PHASE 3 — PERTURBATION MECHANICS (Why would knockdown of {pert} affect {gene}?)

  CATEGORY A — Direct Information Flow Failure (The Command Chain)
      Does {pert} directly activate or repress {gene} expression?
      Knocking down {pert} — does it remove a known activator or a known repressor of {gene}?

  CATEGORY B — Linear Signaling Cascade Disruption (The Telephone Game)
      Is {pert} upstream of {gene} in a defined signaling pathway?
      Does loss of {pert} block a phosphorylation/activation event required to regulate {gene}?

  CATEGORY C — Organelle Homeostasis & Cellular Stress (The Emergency Response)
      Does knockdown of {pert} trigger a secondary stress response
      (ER stress, mitochondrial dysfunction, oxidative stress, inflammation)
      that would indirectly alter {gene} expression as a downstream consequence?

  CATEGORY D — Functional Redundancy & Genetic Compensation (The Back-Up Plan)
      Is there a paralog or redundant gene that could compensate for loss of {pert}?
      Could loss of {pert} lead to upregulation of {gene} as a compensatory mechanism?

  CATEGORY E — Complex Stability & Degradation (The House of Cards)
      Are {pert} and {gene} protein products members of the same complex?
      If {pert} is knocked down, does {gene} protein/mRNA become destabilized or stabilized
      due to loss of a binding partner?

  CATEGORY F — Null Topology (No Functional Link)
      Are {pert} and {gene} in completely separate pathways, compartments, and functions
      with no known crosstalk in the BMDM context?
      Is there any plausible indirect route, or is this a true null relationship?

─────────────────────────────────────────────────────────────────────────────

After working through the relevant categories above, determine which topology best describes the relationship:

  [ 1. Direct Edge ]     — {pert} directly controls {gene}
  [ 2. Indirect Path ]   — {pert} affects {gene} through intermediate steps
  [ 3. Systemic/Global ] — knockdown causes a broad stress/compensation response that reaches {gene}
  [ 4. Null Topology ]   — no meaningful functional link exists

─────────────────────────────────────────────────────────────────────────────

Then provide the final output in a separate final section.
The final output must be exactly one of these three uppercase letters and nothing else:
A
B
C

Reasoning:

Final output:"""

PROMPT_V3 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Think step by step in the reasoning section. Base your prediction strictly on biological mechanisms and systems-level logic.

CRITICAL REASONING GUIDELINES:
1. Null Topology (C): Most random gene pairs in biology do not interact. If there is no plausible biological link between the genes (e.g. they operate in completely unrelated cellular compartments with no cross-talk), confidently predict C.
2. Compensatory Upregulation (A): When a perturbation impairs a specific cellular function or organelle, the cell often triggers compensatory transcriptional upregulation of related genes to overcome the defect.
3. De-repression (A): Loss of a transcriptional repressor or insulator leads to UP-regulation of its targets.
4. Loss of Activator (B): Loss of a positive transcriptional regulator or required upstream signaling kinase leads to DOWN-regulation.
5. Systemic Stress Responses: Explicitly consider broad pathways like ER stress, nucleolar stress, and DNA damage response.

REAL-WORLD PERTURB-SEQ EXAMPLES IN MACROPHAGES:

--- Example 1 (Loss of Activator) ---
Perturbation: Spi1
Gene of interest: Tlr4
Predict the effect of CRISPR knockout of Spi1 on Tlr4:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Spi1 encodes the master transcription factor PU.1, which is essential for macrophage lineage determination and activation. Tlr4 is the primary receptor for LPS and a core component of the macrophage inflammatory response. PU.1 is known to directly bind and positively regulate the transcription of Tlr4 and the broader NF-kB signaling cascade. Knocking out the Spi1 (PU.1) master activator removes the positive transcriptional drive for these genes. Therefore, without its required activator, Tlr4 will be down-regulated.
Final output:
B

--- Example 2 (Loss of Pathway Regulator) ---
Perturbation: Gsk3b
Gene of interest: Ciita
Predict the effect of CRISPR knockout of Gsk3b on Ciita:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Gsk3b encodes Glycogen synthase kinase-3 beta, a central kinase involved in multiple signaling pathways including macrophage activation. Ciita is the master transactivator for MHC class II genes. In macrophages, the GSK3b pathway is required to positively regulate the expression of Ciita in response to inflammatory stimuli like IFN-g. Knocking out Gsk3b disrupts this essential upstream signaling cascade, preventing the proper activation of Ciita. Therefore, Ciita will be down-regulated.
Final output:
B

--- Example 3 (Null Topology) ---
Perturbation: Mmp9
Gene of interest: Polr2a
Predict the effect of CRISPR knockout of Mmp9 on Polr2a:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Mmp9 encodes Matrix metalloproteinase-9, an enzyme secreted into the extracellular matrix to degrade structural proteins during tissue remodeling and inflammation. Polr2a encodes the central catalytic subunit of RNA polymerase II, which resides in the nucleus and is responsible for all mRNA transcription. These two genes operate in entirely different subcellular compartments (extracellular vs. nucleus) and biological modules. Knocking out a secreted protease will have no direct or significant indirect effect on the basal transcription of the core RNA polymerase II subunit. Without a clear mechanism, this is a Null Topology.
Final output:
C

--- Example 4 (Compensatory Upregulation / Stress) ---
Perturbation: Atg5
Gene of interest: Sqstm1
Predict the effect of CRISPR knockout of Atg5 on Sqstm1:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.
Reasoning:
Atg5 is an essential core component of the autophagy machinery. Sqstm1 (p62) is an autophagy receptor that targets cargo for degradation and is itself degraded by autophagy. Knocking out Atg5 completely blocks autophagy, leading to the massive accumulation of undegraded proteins and cellular stress. In response to this profound autophagic stress, the cell activates compensatory transcriptional pathways (such as Nrf2) which heavily up-regulate the transcription of Sqstm1 to attempt to overcome the defect. Therefore, Sqstm1 will be up-regulated.
Final output:
A
----------------

Now, answer the following:

Perturbation: {pert}
Gene of interest: {gene}
Predict the effect of CRISPR knockout of {pert} on {gene}:
  A) up-regulated.
  B) down-regulated.
  C) no significant effect.

Reasoning:

Final output:"""


SOLUTION_GENERATION_V0 = """You are an expert computational biologist tasked with explaining the empirical results of a CRISPR knockout screen.

### Biological Context
* **Cell Type:** Primary mouse bone marrow-derived macrophages (BMDMs) stimulated with LPS for 9 hours (active inflammatory state).
* **Perturbation Mechanism:** CRISPR knockout — the perturbed gene's protein is completely absent.
* **Measurement:** Differential expression is computed using ebnm-shrunken log2 fold-changes. A gene is labelled 'up' or 'down' only if it passes FDR < 5% AND |shrunken log2FC| >= log2(1.5). Shrinkage pulls weak or indirect effects toward zero. Therefore, 'none' does NOT always mean there is no biological connection — it means the effect was too weak, too indirect, or too noisy to survive the statistical threshold.
* **Dataset construction:** 'none' target genes are NOT randomly selected — they are specifically nearby genes that showed sub-threshold effects. Expect a plausible but weak/indirect connection.

### Task
You are given the Perturbed Gene, a Target Gene, and the GROUND TRUTH empirical label from the experiment. Your job is to reverse-engineer the biological mechanism. Write a detailed, step-by-step causal chain that logically justifies WHY this specific outcome occurred in LPS-stimulated mouse macrophages.

### Formatting Constraints
1. **Be Authoritative:** Do NOT use conversational meta-language like "We need to explain why..." or "Let's discuss". Write in the third person like a textbook.
2. **Be Direct:** State the facts of the genes, link the mechanistic pathway, and conclude logically.
3. **Mandatory Conclusion:** Your reasoning trace MUST end with the exact wording indicating the final label. (e.g. "Therefore, {gene} is up-regulated.")

### Ground Truth Event
* Perturbation (Knockout): {pert}
* Target Gene: {gene}
* True Empirical Outcome: {true_label}

Explain the mechanistic pathway that leads exactly to this outcome.

Reasoning:"""


PROMPT_V4 = """You are an expert molecular biologist who studies how genes are related using Perturb-seq.

Context: Mouse bone marrow-derived macrophages (BMDMs) are primary immune cells differentiated from bone marrow precursors using M-CSF.

The following question is about a CRISPR knockout experiment in mouse bone marrow-derived macrophages (BMDMs).

Perturbation: {pert}
Gene of interest: {gene}

Predict the effect of CRISPR knockout of {pert} on {gene} from the following options:
  no significant effect.
  up-regulated.
  down-regulated.

Think step by step in the reasoning section.

Then provide the final output in a separate final section.

The final output must be exactly one of these three and nothing else:

none
up
down
"""

PROMPT_V5 = """You are an expert molecular biologist specializing in mouse bone‑marrow‑derived macrophages (BMDMs) and Perturb‑seq analysis.  
For each query you are given:

* **pert** – the gene knocked down with CRISPR‑i.  
* **gene** – the downstream gene whose expression change you must predict.

Your answer must contain two sections:

1. **reasoning** – 1–3 short sentences per logical step.  
2. **label** – exactly one token: `none`, `up`, or `down`.

### Decision‑making workflow

1. **Identify the primary molecular function of *pert***  
   - Classify it (TF, co‑factor, chromatin remodeler, RNA‑binding protein, ribosomal/translation factor, export receptor, chaperone, proteasome subunit, ER‑AD component, endosomal trafficking protein, ubiquitin‑ligase scaffold or substrate‑receptor, kinase/phosphatase, metabolic enzyme, scaffold for signaling complexes, etc.).  
   - **If the gene has multiple reported roles, list the most relevant one for signaling or transcription in macrophages** (e.g., a metabolic enzyme that generates a lipid second messenger, a trafficking subunit that controls receptor recycling, an actin‑regulatory protein that scaffolds MyD88/TLR signaling).  
   - Use a curated database (UniProt, Gene Ontology, BioGRID) to verify the annotation; do **not** rely on a single memory of the protein.

2. **Immediate cellular consequence of loss**  
   Apply the appropriate consequence based on the functional class:  

   * Enzymatic loss → substrate accumulation or depletion.  
   * Export‑receptor loss → nuclear retention of NES‑containing TFs or pre‑miRNAs.  
   * Ribosome‑biogenesis loss → nucleolar stress → release of RPL5/11 → p53 stabilisation.  
   * DNA‑damage/replication stress → GCN2/PKR → eIF2α‑P → ATF4 activation.  
   * Chaperone/ER‑AD loss → UPR (ATF6, XBP1‑s, PERK‑ATF4).  
   * Negative‑regulator loss → hyper‑activation of its pathway.  
   * Endosomal‑trafficking loss → prolonged receptor signalling (e.g., TLR4, cytokine receptors).  
   * Metabolic‑enzyme loss → change in a lipid/second‑messenger that normally dampens or promotes a kinase cascade (e.g., ceramide‑PP2A, malate/α‑KG carrier).  
   * Scaffold‑for‑signaling‑complex loss → disruption of complex assembly, leading to altered downstream kinase or adaptor activity (e.g., actin‑WRC, LUBAC, Ragulator).  

   **New principle:** loss of a scaffold or trafficking protein can *enhance* upstream signalling (by preventing termination) or *dampen* it (by preventing proper complex formation). Evaluate both possibilities.

3. **Map the consequence to transcription‑factor activity**  
   Identify which TF(s) become **activated** (or **de‑repressed**) by the consequence in BMDMs:  

   * **p53** – nucleolar/DNA‑damage stress.  
   * **ATF4** – integrated stress response via eIF2α‑P (GCN2, PERK).  
   * **NRF2** – oxidative stress (KEAP1 loss, ROS).  
   * **ATF6 / XBP1‑s** – classic UPR.  
   * **NF‑κB (p65/RelA)** – LPS/TLR4, also boosted by prolonged receptor residence or loss of IκBα turnover.  
   * **STAT1/STAT3, IRF1/IRF3** – type‑I/II IFN signalling.  
   * **Myc‑Max, C/EBPβ, AP‑1** – metabolic or cytokine‑responsive programmes.  
   * **TFEB/TFE3** – mTORC1 inhibition or Ragulator loss.  

   Include indirect activation: e.g., loss of a negative regulator of NF‑κB (TANK, ATF3) → sustained NF‑κB; loss of a metabolic enzyme that removes an inhibitor of NF‑κB → hyper‑activation.

4. **Search for direct or indirect links between *pert* and transcription‑factor regulation**  

   a. **Known client / substrate proteins** – If *pert* is a chaperone, proteasome subunit, ubiquitin‑ligase, spliceosomal factor, metabolic enzyme, or signaling scaffold, list documented client proteins that are (i) TF repressors, (ii) TF activators, or (iii) adapters controlling TF activity.  

   b. **Effect of client destabilisation** –  
      * Loss of a chaperone that folds a TF repressor → degradation of the repressor → **derepression** of TF‑activated targets (`up`).  
      * Loss of an E3 that normally degrades a TF → **stabilisation** of that TF (`up` for TF‑activated targets, `down` for TF‑repressed targets).  
      * Loss of a spliceosomal factor that causes intron‑retention in transcripts encoding TF inhibitors (e.g., *IκBα*) → reduced inhibitor protein → **enhanced TF activity** (`up`).  

   c. **Protein‑protein interaction shortcuts** – If curated databases list *pert* as directly interacting with a TF (as scaffold, adaptor, or regulator), treat that interaction as a mechanistic bridge.  

   d. **Secondary pathway effects** – Consider well‑documented secondary activities (e.g., a metabolic enzyme that supplies a lipid second messenger, a trafficking subunit that controls receptor recycling, a Ragulator subunit that regulates TFEB). Use these to link *pert* loss to TF activation even if no direct client is known.

5. **Check TF‑target relationship for *gene***  

   a. **Direct evidence** – ChIP‑seq, reporter assay, or documented promoter motif showing the TF binds the *gene* promoter.  

   b. **Curated TF‑target list** – If the *gene* belongs to one of the core stress‑TF families below, treat it as a bona‑fide target of that TF.  

   c. **Composite promoter logic** – If the *gene* promoter contains binding sites for **multiple** TFs that are each predicted to be activated by the perturbation (e.g., NF‑κB + p53, NF‑κB + ATF4, NF‑κB + TFEB), the combined activation can produce a **synergistic up‑regulation** even when one pathway alone is near saturation. In such cases, retain the `up` prediction.  

   d. **Repressor‑TF scenario** – If the TF is a known transcriptional repressor of the *gene* and is activated, predict `down`.  

   e. **m6A‑mediated decay rule** – Loss of an m6A writer (e.g., VIRMA) reduces m6A on the *gene* transcript, **decreases** YTHDF2‑mediated decay, and therefore **stabilises** the mRNA → predict `up` when the gene’s expression change is driven primarily at the RNA‑stability level.  

   f. **Splicing‑sensitivity rule** – For genes with weak 5′ splice sites or known splicing‑dependent regulation, loss of a spliceosomal component can cause intron retention → predict `down`. For genes with strong canonical splice sites and strong transcriptional activation (e.g., NF‑κB‑driven), the effect is often buffered → default to `none` unless other evidence exists.  

   g. **Chromatin‑remodeler rule** – Loss of a complex that deposits an activating histone variant (e.g., H2A.Z via SRCAP) generally **opens** chromatin, facilitating binding of stimulus‑dependent TFs → predict `up` for TF‑target genes if the TF is active. Conversely, loss of a complex that maintains repressive marks can **derepress** genes → predict `up`.  

6. **Pathway‑saturation and synergy assessment**  

   *Determine whether the relevant TF‑branch is already near‑maximal in LPS‑stimulated BMDMs.*  

   - If the only activated TF is known to be saturated **and** no synergistic promoter composition (step 5c) or direct chromatin‑opening event (step 5e‑g) is present, downgrade the prediction to `none`.  
   - If multiple TFs are activated, or the perturbation creates a new TF‑activating mechanism (e.g., stabilising NRF2 while also enhancing NF‑κB), retain the `up`/`down` call because synergistic amplification can overcome apparent saturation.  

7. **Redundancy / buffering consideration**  

   - If *pert* belongs to a family with known functional redundancy (multiple ER‑AD E3s, export receptors, Sec‑complex subunits, paralogous chaperonins), loss is often buffered; default to `none` **unless** strong non‑redundant evidence exists (client destabilisation, direct TF interaction, unique scaffold role).  

8. **Finalize**  

   - If a clear mechanistic chain survives the above filters (perturbation → TF activation/inhibition → target gene regulation), output `up` or `down`.  
   - Otherwise output `none`.

### Example template

**reasoning**
1. X encodes … (function, note any secondary signaling role).  
2. Knock‑down causes … (stress, TF activation, loss of inhibition, client destabilisation, or signaling scaffold disruption).  
3. TF Y is activated (or a repressor is lost) and directly/curated‑list‑wise regulates target Z (or Z is derepressed).  
4. Pathway‑saturation / synergy / redundancy assessment → … (retain, downgrade, or default).  
5. Therefore Z is expected to be ….

**label**
up

### Query

Perturbation: {pert}
Target Gene: {gene}

Analyze the mechanism and provide your reasoning and label as instructed.
"""
