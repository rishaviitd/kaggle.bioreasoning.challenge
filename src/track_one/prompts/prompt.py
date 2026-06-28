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

