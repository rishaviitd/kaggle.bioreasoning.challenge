# PROMPT_V1 None Overprediction Analysis

## Source

- Artifact: `src/track_one/metrics/prompt_diagnostics/v1_train50_balanced_batch04_openrouter.json`
- Prompt: `PROMPT_V1`
- Sample: 50 balanced train rows
- True labels: 17 `up`, 17 `down`, 16 `none`

## Main Finding

`PROMPT_V1` fixed some generic pathway overreach, but it overcorrected into an overly strict evidence filter.

The core failure is:

```text
The model now treats "no direct target-specific causal bridge" as almost equivalent to "none".
```

This is too strict for Perturb-seq, where many real effects are indirect, module-level, pathway-output, or state-shift effects rather than direct TF-to-target relationships.

## Quantification

```text
true up/down rows:      34
true up/down -> none:  30
rate:                  88.2%

up -> none:            16/17
down -> none:          14/17
```

Prediction distribution:

```text
true: up=17, down=17, none=16
pred: up=1,  down=4,  none=45
```

Overall:

```text
accuracy:  0.34
macro_f1:  0.254
```

## Rows Affected

| Row | True | Pred | Analyzable reasoning? |
|---|---:|---:|---|
| `Adnp_Alox5ap` | down | none | yes |
| `Atp6ap2_Il7r` | up | none | yes |
| `Bloc1s1_Sqstm1` | up | none | yes |
| `Cct7_Ifit3` | up | none | yes |
| `Dido1_Prkcg` | up | none | no, answer only |
| `E4f1_C3` | down | none | yes |
| `Emc7_Procr` | down | none | no, answer only |
| `Fbxo11_Bcl6` | down | none | yes |
| `Gins2_Fcgr2b` | down | none | yes |
| `Gpn2_Ctsh` | up | none | yes |
| `Kat5_Alox5ap` | down | none | yes |
| `Mapkapk2_Lrp1` | down | none | yes |
| `Mau2_Cd63` | up | none | yes |
| `Mbtps2_Chchd10` | up | none | no, answer only |
| `Mcm4_AW554918` | down | none | no, answer only |
| `Mideas_Bcl2a1d` | down | none | yes |
| `Myc_Ftl1-ps1` | down | none | no, answer only |
| `Nolc1_Cd69` | up | none | no, answer only |
| `Pfn1_Hp` | down | none | yes |
| `Rbm14_Fzd1` | up | none | yes |
| `Rps26_Gpr84` | down | none | no, answer only |
| `Setd2_Pf4` | up | none | yes |
| `Ticam2_Anxa3` | up | none | yes |
| `Tpr_H2-Ab1` | up | none | yes |
| `Ubr4_Lgals3` | up | none | yes |
| `Urm1_Blvrb` | down | none | yes |
| `Usp9x_Ccrl2` | up | none | yes |
| `Vps18_Creg1` | up | none | yes |
| `Vps18_Lgals3` | up | none | yes |
| `Wdr61_Saa3` | down | none | yes |

## Reasoning Pattern Counts

Among the 30 `up/down -> none` failures:

| Reasoning pattern | Count |
|---|---:|
| Requires BMDM/macrophage-specific validation too strongly | 23/30 |
| Rejects because no direct regulator-target link | 21/30 |
| Rejects because not a canonical output | 17/30 |
| Rejects generic or broad stress response | 16/30 |
| Gates too hard on basal/stimulus context | 16/30 |
| Rejects because perturbation is not a TF/signaling node | 16/30 |
| Discounts housekeeping/core machinery effects | 8/30 |
| Discounts post-transcriptional/protein-level mechanism | 3/30 |

## What The Prompt Caused The Model To Do

### 1. Direct-evidence requirement became too strong

The model repeatedly searched for a direct link such as promoter binding, ChIP-seq, direct TF regulation, or published BMDM perturbation evidence. When it could not find that direct evidence, it chose `none`.

Examples:

- `Adnp_Alox5ap`: rejected ADNP -> inflammatory signaling -> Alox5ap because no direct ADNP promoter/enhancer evidence.
- `Gins2_Fcgr2b`: rejected replication stress or cell-cycle effects because Fcgr2b is not a known direct DNA-replication-stress target.
- `Tpr_H2-Ab1`: rejected nuclear pore / mRNA export stress because no direct Tpr -> CIITA/RFX/H2-Ab1 bridge.

Why this is bad:

```text
Perturb-seq labels can reflect indirect but reproducible cell-state/module effects.
Direct promoter evidence should be strong evidence, not a hard requirement.
```

### 2. "Generic stress" became an automatic rejection

The added rule said generic stress is insufficient. The model interpreted this as:

```text
lysosomal stress, proteostasis stress, transcriptional stress, nuclear export stress, oxidative stress, replication stress -> none
```

Examples:

- `Bloc1s1_Sqstm1`: rejected lysosomal trafficking stress -> TFEB/Nrf2/NF-kB -> Sqstm1.
- `Cct7_Ifit3`: rejected proteostasis stress or misfolded signaling components -> ISG response.
- `Vps18_Lgals3`: rejected lysosomal dysfunction / NF-kB stress -> Lgals3.
- `Urm1_Blvrb`: rejected oxidative stress / translation stress -> Blvrb.

Why this is bad:

```text
Some stress responses are generic in wording but still produce specific canonical outputs.
The prompt needs to distinguish weak generic stress from canonical module-output stress.
```

### 3. "Not a transcription factor" became too decisive

The model repeatedly used `not a TF`, `not a signaling molecule`, or `post-translational only` as a reason to predict `none`.

Examples:

- `Bloc1s1_Sqstm1`: BLOC-1 is trafficking, not transcriptional.
- `Cct7_Ifit3`: CCT/TRiC is housekeeping, not signaling.
- `Fbxo11_Bcl6`: FBXO11 affects BCL6 protein degradation, not Bcl6 mRNA directly.
- `Mapkapk2_Lrp1`: MK2 mainly controls mRNA stability, not direct transcription.
- `Wdr61_Saa3`: PAF1/SKI-exosome component, structural/auxiliary, not DNA-binding.

Why this is bad:

```text
The perturbation gene does not need to be a TF to change target mRNA.
Perturbing trafficking, proteostasis, chromatin, RNA processing, and signaling-adjacent machinery can shift expression programs.
```

### 4. BMDM-specific evidence gate became unrealistic

The model often rejected a mechanism because it was not specifically demonstrated in primary mouse BMDMs.

Examples:

- `Kat5_Alox5ap`: accepted Kat5 can modulate NF-kB but rejected it because not well-characterized in primary BMDMs.
- `Pfn1_Hp`: accepted Pfn1 can affect actin/NF-kB but rejected BMDM-specific evidence.
- `Setd2_Pf4`: accepted Setd2 can alter inflammatory cytokine expression but rejected Pf4 because not documented as a SETD2-dependent BMDM gene.

Why this is bad:

```text
The model will rarely know exact BMDM perturbation evidence for each pair.
It should use BMDM specificity as a weighting factor, not as a strict veto.
```

### 5. Basal/stimulus gating became too conservative

The model often said a target is stimulus-induced, low under basal BMDM conditions, or context-dependent, then chose `none`.

Examples:

- `Adnp_Alox5ap`: inflammatory stimulus required.
- `Atp6ap2_Il7r`: Il7r low/absent in mature macrophages.
- `Cct7_Ifit3`: Ifit3 requires type-I IFN/IRF activation.
- `Ticam2_Anxa3`: Anxa3 not a canonical IRF3 output and MyD88 remains intact.
- `Usp9x_Ccrl2`: basal NF-kB activity minimal.

Why this is partly good and partly bad:

```text
Cell-state gating is useful, but V1 uses it as another reason to default to none.
The model needs to ask whether knockdown itself can create the relevant state shift.
```

## Important Nuance

The V1 rule did exactly what it was designed to do:

```text
It stopped the model from turning every plausible pathway story into a direction.
```

But it overdid it:

```text
It changed "be skeptical of generic pathways" into "predict none unless direct evidence is very strong".
```

That is the current prompt bug.

## Prompt Design Implication

The next edit should keep the anti-overreach rule but add a balanced exception:

```text
Do not require direct TF/promoter evidence. Indirect mechanisms can be directional when the perturbation affects a core module and the target is a plausible canonical output of that module or cell-state shift in BMDMs.
```

The prompt should distinguish three evidence levels:

```text
Strong direction:
- direct regulator-target relationship
- canonical pathway/module output
- known stress/state-response target affected by the perturbed module

Weak direction:
- generic pathway membership
- broad stress with no target-class match
- not active in BMDMs

None:
- no direct link AND no plausible canonical module/state output
```

The critical correction is:

```text
"No direct link" should not automatically mean "none".
```

