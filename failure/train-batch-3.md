Batch 3 overall first:

```text
rows: 50
correct: 20
incorrect: 30
accuracy: 0.400
macro_f1: 0.421

true counts: up 17, down 17, none 16
pred counts: up 16, down 17, none 17
```

So label distribution is balanced. No obvious class overprediction.

Rows 1-5 analysis:

|   # | id             | true | pred |  ok | reasoning pattern                                                                                                                                                          |
| --: | -------------- | ---: | ---: | --: | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   1 | `Adnp_Glrx`    | down | down | yes | ADNP supports Nrf2/oxidative-stress genes, so loss lowers Glrx. Plausible but still assumes ADNP is a positive activator.                                                  |
|   2 | `Arpc3_Fmnl2`  | none |   up |  no | **False compensation story**: Arp2/3 loss -> formin compensation -> MRTF/SRF -> Fmnl2 up. This is speculative pathway compensation treated as real transcriptional effect. |
|   3 | `Bloc1s1_Eif5` | none | none | yes | Correctly rejects weak trafficking-to-translation link. Good “no direct/strong indirect connection” reasoning.                                                             |
|   4 | `Cct5_Tuba1c`  |   up |   up | yes | CCT loss impairs tubulin folding -> tubulin mRNA autoregulation -> Tuba1c up. This is a specific compensatory mechanism, more grounded than generic stress.                |
|   5 | `Cct7_Fcgr2b`  | down | none |  no | **False none from no direct link**: says CCT7 has no specific link to Fcgr2b, ignores possible chaperone/signaling dependency causing down.                                |

Pattern from first 5:

```text
The model flips between two extremes:
1. It overaccepts compensatory pathway stories when they sound specific.
2. It overrejects indirect effects when it cannot name a direct regulator.
```

This is exactly the same broader issue from earlier batches:

```text
The model lacks a calibrated threshold for indirect mechanisms.
```

Rows 1-5 give two important prompt clues, but we should keep reading more chunks before editing:

```text
- Compensation should not be predicted unless it is a known robust transcript-level feedback, not just a plausible cellular adaptation.
- “No direct link” is not enough for none when the perturbation hits a global machinery node that can affect immune receptors, proteostasis, trafficking, or signaling.
```

Rows 6-10:

|   # | id             | true | pred |  ok | reasoning pattern                                                                                                                                                            |
| --: | -------------- | ---: | ---: | --: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   6 | `Cnot2_Akr1a1` | none |   up |  no | **False post-transcriptional derepression**: CNOT2 loss -> less deadenylation -> Akr1a1 mRNA stabilizes. It even claims Perturb-seq precedent. Very confident but wrong.     |
|   7 | `Dda1_Cfb`     | down |   up |  no | **Wrong direction via NF-kB stabilization story**: DDA1/CRL4 loss -> p65 less degraded -> NF-kB higher -> Cfb up. True is down, so it picked the wrong dominant CRL4 effect. |
|   8 | `Ddx6_Csf3r`   | none |   up |  no | **False mRNA stability rule**: DDX6 loss -> less decay/miRNA repression -> Csf3r up. Again plausible post-transcriptional derepression, but no actual effect.                |
|   9 | `Dnajc8_Ctsh`  | none | none | yes | Correctly rejects weak co-chaperone -> lysosomal protease link. Good use of “indirect weak under basal BMDM” reasoning.                                                      |
|  10 | `Dph3_Bst1`    | none | none | yes | Correctly rejects translation-fidelity stress -> inflammatory marker link as too weak/non-specific.                                                                          |

Strong pattern in rows 6-10:

```text
The model is overusing “loss of RNA/protein degradation machinery causes target mRNA/protein to increase.”
```

Specifically:

```text
CNOT2 loss -> target mRNA stabilized -> up
DDX6 loss -> target mRNA stabilized -> up
DDA1 loss -> p65 stabilized -> NF-kB target up
```

All three are wrong here.

So a candidate stable rule is emerging:

```text
Do not predict up just because a perturbation weakens degradation, deadenylation, miRNA silencing, ubiquitination, or proteasomal turnover. That only supports up if the target itself or a specific regulator of the target is known to be directly stabilized in BMDMs.
```

Also, rows 9-10 show what the model does well:

```text
When it says “weak generic stress is not gene-specific enough,” it often gets none right.
```

So the prompt should preserve that skepticism, but apply it more consistently to RNA decay / ubiquitin / post-transcriptional mechanisms.

Rows 11-15:

|   # | id              | true | pred |  ok | reasoning pattern                                                                                                                                                 |
| --: | --------------- | ---: | ---: | --: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  11 | `Dusp1_Hspa1b`  | none |   up |  no | **False stress/MAPK induction**: DUSP1 loss -> MAPK high -> HSF1/Hsp70 up. Plausible but too stimulus/stress-dependent.                                           |
|  12 | `Dync1h1_Gpnmb` |   up | down |  no | **Wrong dominant mechanism**: dynein loss blunts STAT6/NF-kB trafficking -> Gpnmb down. It misses possible lysosomal/trafficking stress induction.                |
|  13 | `Emc7_Gpnmb`    | none | none | yes | Correctly rejects mild ER stress -> Gpnmb as not strong enough. Good skepticism.                                                                                  |
|  14 | `Emc7_Procr`    | down | none |  no | **False none from no direct transcriptional link**: ignores that EMC/ER membrane protein biogenesis perturbation can reduce membrane receptor transcript/program. |
|  15 | `Fbxo11_Cd9`    | down |   up |  no | **False E3-ligase derepression/storytelling**: FBXO11 loss -> BCL6/TGF-beta/M2 program -> CD9 up. Very elaborate, wrong direction.                                |

This chunk repeats two major patterns:

1. **False up from “loss of negative regulator”**
   - `Dusp1_Hspa1b`: remove MAPK brake -> stress gene up.
   - `Fbxo11_Cd9`: remove ubiquitin ligase -> BCL6/TGF-beta -> CD9 up.

2. **False none from “not a transcription factor / no direct link”**
   - `Emc7_Procr`: model says EMC is not transcriptional, so none, but true is down.

Important nuance:

The model got `Emc7_Gpnmb` right with the same style of reasoning that made `Emc7_Procr` wrong. So we cannot simply say “don’t use no-direct-link.” The better rule is:

```text
For ER/protein-insertion/trafficking machinery, do not dismiss membrane or secretory target genes as none only because the perturbation is not a TF. But require target-specific vulnerability, not generic ER stress.
```

Stable pattern now across chunks:

```text
The model needs better machinery-node rules:
RNA decay, ubiquitin ligases, chaperones, ER insertion, trafficking, cytoskeleton, proteasome.
```

It keeps treating those as either:

```text
generic no direct link -> none
```

or:

```text
generic pathway compensation/derepression -> up/down
```

The correct behavior is more selective.

Rows 16-20:

|   # | id              | true | pred |  ok | reasoning pattern                                                                                                                                                                         |
| --: | --------------- | ---: | ---: | --: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  16 | `Gins4_Ccnd1`   |   up | down |  no | **False cell-cycle checkpoint logic**: replication factor loss -> p53/p21/S-phase arrest -> Cyclin D1 down. It ignores possible compensatory/proliferative-state transcript response.     |
|  17 | `Ikbkb_Bcl2a1d` | down | down | yes | Good direct pathway: IKKβ -> NF-kB -> Bcl2a1d. This is a strong, specific target dependency.                                                                                              |
|  18 | `Ints1_Ms4a4c`  | down | down | yes | Integrator supports enhancer/RNAPII transcription; target treated as macrophage enhancer-dependent. Plausible machinery-node down logic.                                                  |
|  19 | `Jak1_Akr1a1`   | none | none | yes | Good skepticism: Akr1a1 is Nrf2/metabolic, not canonical JAK-STAT; indirect cytokine cross-talk too weak.                                                                                 |
|  20 | `Kras_Ccrl2`    |   up | down |  no | **False canonical signaling-loss rule**: KRAS loss -> weaker MAPK/NF-kB/AP-1 -> chemokine receptor down. True is up, so it missed negative feedback/derepression/compensatory activation. |

This chunk gives a clean contrast:

**When model is right**

```text
Ikbkb_Bcl2a1d:
specific pathway node + specific downstream NF-kB target = down

Jak1_Akr1a1:
pathway mismatch + weak indirect cross-talk = none
```

**When model is wrong**

```text
Gins4_Ccnd1:
generic checkpoint/cell-cycle logic overrules actual up

Kras_Ccrl2:
canonical loss-of-activator logic overrules possible derepression/feedback

```

Stable rule emerging:

```text
Canonical pathway direction is not enough.
Before predicting down from loss of an activator, check whether the perturbation can trigger feedback activation, stress compensation, or removal of repression that may flip direction to up.
```

But also:

```text
Do not apply that flip rule everywhere. For direct target dependencies like IKKβ -> NF-kB -> Bcl2a1d, down is correct.
```

So the prompt needs a **specificity threshold**:

```text
Direct strong dependency: use canonical direction.
Broad pathway membership: be skeptical.
Feedback/derepression possible: explicitly evaluate before final label.
```

Rows 21-25:

|   # | id               | true |    pred |  ok | reasoning pattern                                                                                                                                                              |
| --: | ---------------- | ---: | ------: | --: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|  21 | `Mbtps2_Manf`    | down |    down | yes | Strong direct pathway: Mbtps2/S2P required for ATF6 cleavage -> Manf down. This is good because the target is directly in the ATF6/UPR output.                                 |
|  22 | `Mcm4_Zfp263`    | none |    none | yes | Good cell-type filter: BMDMs mostly post-mitotic, replication stress weak, no direct link.                                                                                     |
|  23 | `Mideas_Bcl2a1d` | down | invalid |  no | Format/extraction failure. Need inspect separately if content empty or parser failed.                                                                                          |
|  24 | `Mnt_Crip1`      | down |      up |  no | **False derepression rule**: MNT is repressor, so knockdown releases Myc/Max and target goes up. True is down, so it assumed repressor logic without target-specific evidence. |
|  25 | `Mtor_Saa3`      | none |    down |  no | **False hub-down rule**: mTOR supports inflammatory/NF-kB/IL-6/Saa3, so mTOR loss down. True none, so it over-applies global signaling hub logic.                              |

Important patterns:

1. **Good use of direct pathway specificity**

   ```text
   Mbtps2 -> ATF6 cleavage -> Manf
   ```

   This kind of direct mechanistic target relationship works.

2. **Good cell-type/activity gating**

   ```text
   Mcm4 replication stress in mostly post-mitotic BMDMs -> weak/no effect
   ```

   This is exactly the kind of reasoning we want preserved.

3. **Bad repressor/derepression shortcut**

   ```text
   Mnt is repressor -> knockdown causes up
   ```

   This is not safe unless target is specifically known to be MNT-repressed.

4. **Bad global hub shortcut**
   ```text
   mTOR supports inflammatory output -> Saa3 down
   ```
   Again, too broad. It does not ask whether basal/experimental conditions make that edge active enough.

Rule candidate becoming clearer:

```text
Only use activator/repressor logic when the target is specifically controlled by that factor/pathway in BMDMs. Do not infer up/down from generic hub roles, generic repression, or broad inflammatory/metabolic programs.
```

Rows 26-30:

|   # | id                     | true |    pred |  ok | reasoning pattern                                                                                                                         |
| --: | ---------------------- | ---: | ------: | --: | ----------------------------------------------------------------------------------------------------------------------------------------- |
|  26 | `Ncor2_Pf4`            |   up |      up | yes | Corepressor loss -> inflammatory chemokine derepression. Correct here, but same logic can be risky when target-specific evidence is weak. |
|  27 | `Nelfa_Pf4`            |   up |      up | yes | NELF loss releases Pol II pausing -> chemokine Pf4 up. This is a specific transcriptional mechanism and works here.                       |
|  28 | `Pafah1b1_Pilra`       | down | invalid |  no | Format/extraction failure. Needs separate inspection.                                                                                     |
|  29 | `Pafah1b1_Pmp22`       | none |    none | yes | Good cell-type expression filter: Pmp22 is Schwann/myelin, not BMDM-relevant, so none.                                                    |
|  30 | `Pdcd10_2500002B13Rik` | none | invalid |  no | Format/extraction failure. Needs separate inspection.                                                                                     |

This chunk mostly shows good reasoning, but with an important caution.

**Good patterns**

```text
- NELF / transcriptional pause release on inducible chemokine genes can produce up.
- NCOR2/corepressor loss can derepress inflammatory genes.
- Cell-type expression filter works for Pmp22.
```

**New issue**

```text
3 invalid predictions so far in the 50-row batch:
Mideas_Bcl2a1d
Pafah1b1_Pilra
Pdcd10_2500002B13Rik
```

We need to inspect invalids later. They may not be actual model failures; they may be parser failures or empty/content oddities. If parser failure, that affects metrics unfairly.

Reasoning takeaway from this chunk:

```text
Derepression logic is sometimes correct, especially for known transcriptional repressors / pausing machinery / inducible immune genes.
```

So we cannot add a blanket rule like “avoid derepression.” The better version is:

```text
Use derepression only when the perturbation is an actual transcriptional repressor/pausing factor/corepressor and the target is plausibly in that regulon. Do not use derepression for generic degradation/ubiquitin/RNA-decay stories unless target-specific evidence is strong.
```

Rows 31-40:

|   # | id               | true | pred |  ok | reasoning pattern                                                                                                                                               |
| --: | ---------------- | ---: | ---: | --: | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|  31 | `Polr2i_Polr2a`  |   up | none |  no | **False housekeeping stability**: says Polr2a is buffered, no effect. Misses possible complex subunit compensation/upregulation.                                |
|  32 | `Psmg4_Sqstm1`   |   up |   up | yes | Good proteasome stress/Nrf2/Sqstm1 mechanism. This specific stress target works.                                                                                |
|  33 | `Ptpn11_Alox5ap` | down |   up |  no | **Wrong dominant pathway**: SHP2 loss removes NF-kB brake -> Alox5ap up. True down, so it picked one role of SHP2 and ignored positive MAPK/AP-1 dependency.    |
|  34 | `Rps19_Cd9`      | down | none |  no | **False none from broad ribosomal stress**: says no specific link, broad modest shift. True down, so broad machinery perturbation did matter.                   |
|  35 | `Sec13_Tnc`      | none | down |  no | **False secretory-load suppression**: Sec13 loss -> ER stress -> suppress secreted ECM genes. Too generic.                                                      |
|  36 | `Setd2_Pf4`      |   up | down |  no | **False positive-chromatin-regulator rule**: SETD2 supports transcription/elongation -> Pf4 down. True up, likely missed derepression/immune-state shift.       |
|  37 | `Sptssa_Rgs16`   |   up | down |  no | No reasoning visible, just answer. Need inspect full raw later if truncated or model gave only answer.                                                          |
|  38 | `Srsf7_Saa3`     | down | down | yes | Splicing factor loss dampens TLR/NF-kB/STAT3 inflammatory program -> Saa3 down. Plausible and correct here.                                                     |
|  39 | `Suz12_Vma21`    | down | none |  no | **False housekeeping/PRC2 target filter**: says Vma21 housekeeping not PRC2 target, so none. True down.                                                         |
|  40 | `Tardbp_Grina`   |   up | down |  no | **False RNA-binding stability claim**: TDP43 stabilizes Grina mRNA -> knockdown down. True up, so direct-looking post-transcriptional claim is wrong direction. |

This is a rough chunk. Main repeated failures:

1. **Housekeeping/buffered gene assumption is dangerous**

   ```text
   Polr2a, Vma21, Cd9-ish machinery response
   ```

   The model says “housekeeping/core gene, no effect,” but labels can be directional.

2. **Generic machinery-node direction is unreliable**

   ```text
   SETD2 loss -> target down
   SEC13 loss -> secretory genes down
   ribosomal loss -> no specific effect
   PRC2 loss -> only PRC2 targets affected
   ```

   These broad rules are often wrong.

3. **Post-transcriptional specificity is often hallucinated**

   ```text
   Tardbp_Grina: claims CLIP/RNA stability evidence and predicts down, but true up.
   ```

   This matches earlier CNOT2/DDX6/DDA1 failures.

4. **Correct rows have stronger target-program fit**
   ```text
   Psmg4 -> Sqstm1 via proteasome/Nrf2
   Srsf7 -> Saa3 via inflammatory RNA processing/TLR signaling
   ```

The strongest global clue so far:

```text
The model is overconfident in mechanistic stories that sound specific but are often not dataset-valid.
```

So prompt edits should probably force an explicit uncertainty check:

```text
If the proposed mechanism relies on generic machinery effects, inferred mRNA stability, inferred chromatin dependence, or unstated literature evidence, downgrade confidence and consider none unless the target is a canonical output of that perturbation class.
```

Rows 41-50:

|   # | id               | true | pred |  ok | reasoning pattern                                                                                                                                   |
| --: | ---------------- | ---: | ---: | --: | --------------------------------------------------------------------------------------------------------------------------------------------------- |
|  41 | `Tcp1_Ddit3`     | none |   up |  no | **False proteotoxic stress -> Ddit3**: CCT loss -> ISR/ATF4 -> CHOP up. Plausible, but too generic here.                                            |
|  42 | `Telo2_Klhl24`   |   up | none |  no | **False none from no known link**: TTT/PIKK perturbation dismissed as not KLHL24-specific. Misses stress/ubiquitin pathway induction.               |
|  43 | `Tmem258_Dnajc3` |   up |   up | yes | Good canonical ER stress: OST/glycosylation loss -> UPR -> DNAJC3 up. Strong target-program match.                                                  |
|  44 | `Traf2_Ctsk`     |   up | down |  no | **Canonical-only error**: TRAF2 loss blunts canonical NF-kB -> Ctsk down. Misses TRAF2 negative/noncanonical/RANK-like effects.                     |
|  45 | `Tsc2_Creg1`     |   up | down |  no | **Wrong mTOR polarization story**: TSC2 loss -> mTORC1/M1 -> anti-inflammatory Creg1 down. True up.                                                 |
|  46 | `Txnl4a_Lgals3`  |   up | down |  no | **Generic splicing-loss rule**: spliceosome knockdown -> mature mRNA down. True up, likely misses stress/compensatory activation.                   |
|  47 | `Tyk2_Ms4a4c`    | down | down | yes | Good cytokine pathway dependency: TYK2 -> IL-10/STAT3 -> Ms4a4c.                                                                                    |
|  48 | `Vhl_Mgarp`      |   up |   up | yes | Good direct degradation-axis logic: VHL loss -> HIF stabilization -> Mgarp up. Strong canonical target.                                             |
|  49 | `Wdr3_H3f3b`     | none | none | yes | Good rejection: ribosome/nucleolar stress not enough for stable H3.3 gene in BMDMs.                                                                 |
|  50 | `Zfp36_Ifrd1`    | down |   up |  no | **False RNA-decay derepression**: TTP loss -> Ifrd1 mRNA stabilized/up. True down. Another post-transcriptional hallucination/wrong-dominance case. |

Final chunk reinforces the main pattern very strongly:

**What works**

```text
Direct canonical target relationships:
- Tmem258 -> ER stress/UPR -> Dnajc3 up
- Vhl -> HIF stabilization -> Mgarp up
- Tyk2 -> cytokine/STAT dependency -> Ms4a4c down
```

**What fails**

```text
Broad machinery rules:
- CCT/proteotoxic stress -> Ddit3 up
- spliceosome loss -> target mRNA down
- TRAF2 canonical NF-kB loss -> Ctsk down
- TSC2/mTOR polarization story -> Creg1 down
```

**Most repeated failure across all chunks**

```text
The model overuses confident “dominant mechanism” stories.
```

Especially:

```text
RNA decay / mRNA stability / ubiquitin degradation stories
generic stress-response stories
generic chromatin/transcription machinery stories
canonical pathway direction without checking feedback/derepression
```

This gives us a pretty clear basis for prompt rules, but your approach is right: these should be summarized from multiple batches rather than one noisy sample.
