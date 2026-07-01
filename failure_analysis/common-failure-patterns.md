# Common Failure Pattern Analysis

## Executive Summary

Across the analyzed failure notes, the biggest problem is not a stable overprediction of one label. The repeated problem is **reasoning calibration**: the model often turns a plausible biological story into a confident `up`, `down`, or `none` without checking whether the mechanism is specific, active in BMDMs, and strong enough to pass the perturbation-expression threshold.

The highest-value prompt optimization target is therefore:

```text
Make the model distinguish strong, target-specific mechanisms from generic pathway stories.
```

## Ranked Failure Patterns

| Rank | Failure pattern | Evidence strength | Why it matters |
|---:|---|---|---|
| 1 | Generic pathway overreach | Very high | Appears across all batches and causes false `up`, false `down`, and false `none`. |
| 2 | Bad threshold for indirect machinery-node effects | Very high | The model alternates between overaccepting and overdismissing effects from chromatin, RNA, proteostasis, trafficking, ER, ribosome, and cytoskeleton machinery. |
| 3 | False post-transcriptional/degradation derepression | High | Repeatedly assumes loss of RNA decay, ubiquitin ligase, or degradation machinery increases a target. |
| 4 | Canonical loss-of-activator shortcut | High | Predicts `down` from canonical pathway weakening while missing feedback, derepression, or alternative dominant branches. |
| 5 | Housekeeping/core-gene buffering assumption | Medium-high | Predicts `none` for core genes or machinery targets that can still shift directionally. |
| 6 | Stimulus/state mismatch | Medium | Assumes LPS/IFN/M1/M2/ER-stress programs are active enough without evidence. |

## Structured Failure Index

This table indexes the wrong rows used for the pattern ranking. Label distribution alone was not used as evidence; each category is based on the reasoning mechanism described in the failure notes.

| Batch | Row | True | Pred | Direction | Reasoning mechanism | Short category |
|---|---|---:|---:|---|---|---|
| 1 | `Pfn1_Ccr5` | up | down | up -> down | Actin/TLR/NF-kB weakening used to force Ccr5 down. | Canonical loss-of-activator shortcut |
| 1 | `Stag2_Gclm` | up | down | up -> down | Cohesin loss weakens enhancer-promoter loops. | Canonical loss-of-activator shortcut |
| 1 | `Actl6a_Ifi27` | up | down | up -> down | BAF loss reduces ISG promoter accessibility. | Canonical loss-of-activator shortcut |
| 1 | `Sec13_Gbf1` | up | none | up -> none | Indirect COPII/trafficking effect treated as too weak. | False none from indirect machinery |
| 1 | `Il10ra_Saa3` | down | up | down -> up | Loss of IL10 anti-inflammatory signaling inferred to increase inflammatory Saa3. | False derepression/up |
| 1 | `Tcp1_St3gal5` | down | none | down -> none | Chaperonin/proteostasis connection treated as non-specific. | False none from machinery threshold |
| 1 | `Atf4_Ifih1` | none | down | none -> down | ATF4 support for IFN/ISG signaling treated as decisive. | Generic pathway overreach |
| 1 | `Tbc1d10b_Creg1` | none | invalid | none -> invalid | Output could not be parsed. | Invalid/parser |
| 1 | `Junb_Spryd7` | none | down | none -> down | JunB/AP-1 target claim treated as direct enough. | Generic pathway overreach |
| 1 | `Wdr3_Mthfd1` | none | down | none -> down | Ribosome stress/lower nucleotide demand used as directional evidence. | Generic machinery overreach |
| 1 | `Ly96_Cfp` | none | down | none -> down | Ly96/TLR4/NF-kB pathway used to force complement gene down. | Generic pathway overreach |
| 2 | `Psmd4_Smpdl3a` | up | down | up -> down | Proteasome/regulatory-subunit logic picked the wrong direction. | Canonical machinery shortcut |
| 2 | `Tsc2_Syngr1` | up | none | up -> none | Syngr1 treated as neuronal/irrelevant. | False none from cell-type filter |
| 2 | `Ctdspl2_Xylt2` | down | up | down -> up | CTDSP2 loss derepresses TGF-beta/Smad, so Xylt2 up. | False derepression/up |
| 2 | `Virma_Psma6` | down | none | down -> none | PSMA6 treated as housekeeping/proteasome core and buffered. | Housekeeping/core-gene assumption |
| 2 | `Arpc3_Vma21` | down | none | down -> none | Actin/trafficking treated as post-translational only. | False none from indirect machinery |
| 2 | `Nolc1_Cfp` | none | down | none -> down | NOLC1/NF-kB coactivation story used to force Cfp down. | Generic pathway overreach |
| 2 | `Ddb1_Snhg1` | none | invalid | none -> invalid | Output could not be parsed. | Invalid/parser |
| 2 | `Dcaf7_Glrx` | none | up | none -> up | DCAF7 loss stabilizes Nrf2, so Glrx up. | False degradation derepression |
| 3 | `Arpc3_Fmnl2` | none | up | none -> up | Arp2/3 loss causes formin/MRTF/SRF compensation. | Generic compensation overreach |
| 3 | `Cct7_Fcgr2b` | down | none | down -> none | No specific CCT7-to-Fcgr2b link, so none. | False none from machinery threshold |
| 3 | `Cnot2_Akr1a1` | none | up | none -> up | CCR4-NOT loss stabilizes Akr1a1 mRNA. | False RNA-decay derepression |
| 3 | `Dda1_Cfb` | down | up | down -> up | CRL4 loss stabilizes p65/NF-kB, so Cfb up. | False degradation derepression |
| 3 | `Ddx6_Csf3r` | none | up | none -> up | DDX6 loss relieves miRNA/decay repression. | False RNA-decay derepression |
| 3 | `Dusp1_Hspa1b` | none | up | none -> up | MAPK/HSF1 stress-response induction assumed active. | Stimulus/state mismatch |
| 3 | `Dync1h1_Gpnmb` | up | down | up -> down | Dynein loss blunts STAT6/NF-kB trafficking. | Canonical loss-of-activator shortcut |
| 3 | `Emc7_Procr` | down | none | down -> none | EMC is not transcriptional, so Procr no effect. | False none from indirect machinery |
| 3 | `Fbxo11_Cd9` | down | up | down -> up | FBXO11 loss stabilizes BCL6/TGF-beta/M2 program. | False degradation derepression |
| 3 | `Gins4_Ccnd1` | up | down | up -> down | Replication factor loss causes checkpoint and Cyclin D1 down. | Canonical machinery shortcut |
| 3 | `Kras_Ccrl2` | up | down | up -> down | KRAS loss weakens MAPK/NF-kB/AP-1. | Canonical loss-of-activator shortcut |
| 3 | `Mideas_Bcl2a1d` | down | invalid | down -> invalid | Output could not be parsed. | Invalid/parser |
| 3 | `Mnt_Crip1` | down | up | down -> up | MNT repressor loss derepresses Myc/Crip1. | False derepression/up |
| 3 | `Mtor_Saa3` | none | down | none -> down | mTOR support for NF-kB/IL-6/Saa3 treated as decisive. | Generic pathway overreach |
| 3 | `Pafah1b1_Pilra` | down | invalid | down -> invalid | Output could not be parsed. | Invalid/parser |
| 3 | `Pdcd10_2500002B13Rik` | none | invalid | none -> invalid | Output could not be parsed. | Invalid/parser |
| 3 | `Polr2i_Polr2a` | up | none | up -> none | Polr2a treated as buffered housekeeping transcript. | Housekeeping/core-gene assumption |
| 3 | `Ptpn11_Alox5ap` | down | up | down -> up | SHP2 loss removes NF-kB brake; positive MAPK role missed. | Wrong dominant pathway |
| 3 | `Rps19_Cd9` | down | none | down -> none | Ribosomal perturbation treated as broad/non-specific. | Housekeeping/core-gene assumption |
| 3 | `Sec13_Tnc` | none | down | none -> down | COPII loss suppresses secreted ECM genes. | Generic machinery overreach |
| 3 | `Setd2_Pf4` | up | down | up -> down | SETD2 supports transcription/elongation, so Pf4 down. | Canonical loss-of-activator shortcut |
| 3 | `Sptssa_Rgs16` | up | down | up -> down | Reasoning not visible in notes. | Insufficient reasoning evidence |
| 3 | `Suz12_Vma21` | down | none | down -> none | Vma21 treated as housekeeping and not PRC2 target. | Housekeeping/core-gene assumption |
| 3 | `Tardbp_Grina` | up | down | up -> down | TDP43 stabilizes Grina mRNA; loss lowers it. | False RNA-binding stability |
| 3 | `Tcp1_Ddit3` | none | up | none -> up | CCT loss causes ISR/ATF4/CHOP activation. | Stimulus/state mismatch |
| 3 | `Telo2_Klhl24` | up | none | up -> none | TTT/PIKK link dismissed as not KLHL24-specific. | False none from machinery threshold |
| 3 | `Traf2_Ctsk` | up | down | up -> down | TRAF2 loss blunts canonical NF-kB. | Canonical loss-of-activator shortcut |
| 3 | `Tsc2_Creg1` | up | down | up -> down | TSC2 loss/mTORC1 shifts away from Creg1. | Wrong dominant pathway |
| 3 | `Txnl4a_Lgals3` | up | down | up -> down | Generic spliceosome loss implies mature target mRNA down. | Generic machinery overreach |
| 3 | `Zfp36_Ifrd1` | down | up | down -> up | TTP loss stabilizes ARE mRNA, so Ifrd1 up. | False RNA-decay derepression |

## 1. Generic Pathway Overreach

**Pattern:** The model sees a plausible named pathway and treats it as decisive, even when the link is indirect, stimulus-dependent, or not target-specific.

**Evidence rows**

| Batch | Row | True -> Pred | Reasoning mechanism |
|---|---|---:|---|
| 1 | `Pfn1_Ccr5` | up -> down | Pfn1 loss weakens actin/TLR/NF-kB, so Ccr5 down. |
| 1 | `Junb_Spryd7` | none -> down | JunB/AP-1 activation claim treated as direct enough. |
| 1 | `Ly96_Cfp` | none -> down | Ly96/TLR4/NF-kB pathway used to force Cfp down. |
| 2 | `Ctdspl2_Xylt2` | down -> up | CTDSP2 loss derepresses TGF-beta/Smad, so Xylt2 up. |
| 2 | `Nolc1_Cfp` | none -> down | NOLC1/NF-kB coactivation story used to force Cfp down. |
| 3 | `Arpc3_Fmnl2` | none -> up | Arp2/3 loss causes formin compensation through MRTF/SRF. |
| 3 | `Dusp1_Hspa1b` | none -> up | DUSP1 loss increases MAPK/HSF1 stress response. |
| 3 | `Sec13_Tnc` | none -> down | COPII loss suppresses secreted ECM genes. |
| 3 | `Mtor_Saa3` | none -> down | mTOR supports NF-kB/IL-6/Saa3, so mTOR loss down. |
| 3 | `Tcp1_Ddit3` | none -> up | CCT loss causes ISR/ATF4/CHOP activation. |

**Why likely real, not noise**

This appears in all batches, across all failure directions. It is not tied to one class or one local sample. The same reasoning style also appears in some correct rows, which means the model is using a broad heuristic that sometimes works and often fails.

**Prompt-rule implication**

```text
Before making a directional prediction from an indirect pathway, require a target-specific causal bridge. If the mechanism is generic pathway membership, broad stress, or unstated activation state, downgrade confidence and consider none.
```

## 2. Bad Threshold For Machinery-Node Effects

**Pattern:** For global machinery perturbations, the model flips between two bad extremes:

```text
generic machinery story -> directional label
no direct TF link -> none
```

**Evidence rows**

| Batch | Row | True -> Pred | Reasoning mechanism |
|---|---|---:|---|
| 2 | `Arpc3_Vma21` | down -> none | Actin/trafficking treated as post-translational only. |
| 2 | `Virma_Psma6` | down -> none | PSMA6 treated as housekeeping/proteasome core, so no effect. |
| 3 | `Cct7_Fcgr2b` | down -> none | CCT7 has no specific link to Fcgr2b. |
| 3 | `Emc7_Procr` | down -> none | EMC is not transcriptional, so Procr no effect. |
| 3 | `Polr2i_Polr2a` | up -> none | Polr2a is housekeeping/buffered. |
| 3 | `Rps19_Cd9` | down -> none | Ribosomal stress considered broad/non-specific. |
| 3 | `Suz12_Vma21` | down -> none | Vma21 not PRC2 target, so no effect. |
| 3 | `Telo2_Klhl24` | up -> none | TTT/PIKK perturbation dismissed as not KLHL24-specific. |
| 3 | `Txnl4a_Lgals3` | up -> down | Generic spliceosome loss implies target mRNA down. |

**Why likely real, not noise**

This pattern appears repeatedly in batch 2 and batch 3 and spans ER insertion, RNA polymerase, ribosome, chromatin, splicing, trafficking, cytoskeleton, and proteasome-related nodes.

**Prompt-rule implication**

```text
For global machinery genes, do not rely on "not a TF" or "housekeeping" alone. Evaluate whether the target belongs to a vulnerable output program of that machinery perturbation. Also avoid generic machinery-direction rules unless the target is a canonical output.
```

## 3. False Post-Transcriptional Or Degradation Derepression

**Pattern:** The model often assumes that loss of RNA decay, ubiquitin, degradation, or repressor machinery stabilizes a target or its upstream activator, causing `up`. These stories are often highly confident and sometimes hallucinate evidence.

**Evidence rows**

| Batch | Row | True -> Pred | Reasoning mechanism |
|---|---|---:|---|
| 2 | `Dcaf7_Glrx` | none -> up | DCAF7 loss stabilizes Nrf2, so Glrx up. |
| 3 | `Cnot2_Akr1a1` | none -> up | CCR4-NOT loss stabilizes Akr1a1 mRNA. |
| 3 | `Dda1_Cfb` | down -> up | CRL4 loss stabilizes p65/NF-kB, so Cfb up. |
| 3 | `Ddx6_Csf3r` | none -> up | DDX6 loss relieves miRNA/decay repression. |
| 3 | `Fbxo11_Cd9` | down -> up | FBXO11 loss stabilizes BCL6/TGF-beta program, so Cd9 up. |
| 3 | `Tardbp_Grina` | up -> down | TDP43 stabilizes Grina mRNA; loss lowers it. |
| 3 | `Zfp36_Ifrd1` | down -> up | TTP loss stabilizes ARE mRNA, so Ifrd1 up. |
| 3 | `Mnt_Crip1` | down -> up | MNT repressor loss derepresses Myc/Crip1. |

**Why likely real, not noise**

This is frequent in batch 3 and also appears in batch 2. It affects `none`, `down`, and `up` true labels. The model frequently makes very specific claims about direct stabilization or binding without reliable evidence.

**Prompt-rule implication**

```text
Do not predict up merely because degradation, RNA decay, ubiquitination, miRNA silencing, or repression is weakened. Use this only when the target itself or a specific regulator of the target is a well-established direct substrate in BMDMs.
```

## 4. Canonical Loss-Of-Activator Shortcut

**Pattern:** The model predicts `down` because the perturbation is a positive pathway component, without checking feedback loops, alternative branches, derepression, or compensatory activation.

**Evidence rows**

| Batch | Row | True -> Pred | Reasoning mechanism |
|---|---|---:|---|
| 1 | `Actl6a_Ifi27` | up -> down | BAF loss reduces ISG promoter accessibility. |
| 1 | `Stag2_Gclm` | up -> down | Cohesin loss weakens enhancer-promoter loops. |
| 1 | `Pfn1_Ccr5` | up -> down | Actin/TLR/NF-kB weakened. |
| 3 | `Kras_Ccrl2` | up -> down | KRAS loss weakens MAPK/NF-kB/AP-1. |
| 3 | `Gins4_Ccnd1` | up -> down | Replication stress/checkpoint lowers cyclin. |
| 3 | `Traf2_Ctsk` | up -> down | TRAF2 loss blunts canonical NF-kB. |
| 3 | `Tsc2_Creg1` | up -> down | TSC2 loss/mTORC1 shifts away from Creg1. |
| 3 | `Setd2_Pf4` | up -> down | SETD2 supports elongation, so Pf4 down. |
| 3 | `Ptpn11_Alox5ap` | down -> up | Chooses SHP2 negative NF-kB regulation over positive MAPK dependency. |

**Why likely real, not noise**

This appears in batch 1 and batch 3 and includes multiple pathway classes: chromatin, cytoskeleton, MAPK, NF-kB, mTOR, replication, and transcription elongation.

**Prompt-rule implication**

```text
Before predicting down from loss of a positive regulator, explicitly check whether the perturbation may remove repression, activate stress compensation, shift cell state, or activate an alternative branch that dominates the target.
```

## 5. Housekeeping / Core-Gene Buffering Assumption

**Pattern:** The model predicts `none` because the target is housekeeping, constitutive, or core machinery, assuming it is buffered. That is sometimes correct, but it repeatedly hides real directional effects.

**Evidence rows**

| Batch | Row | True -> Pred | Reasoning mechanism |
|---|---|---:|---|
| 2 | `Virma_Psma6` | down -> none | Proteasome core/housekeeping transcript treated as buffered. |
| 3 | `Polr2i_Polr2a` | up -> none | Polr2a strong housekeeping promoter, no robust change. |
| 3 | `Rps19_Cd9` | down -> none | Ribosomal perturbation broad/non-specific. |
| 3 | `Suz12_Vma21` | down -> none | Vma21 is housekeeping, not PRC2 target. |
| 3 | `Telo2_Klhl24` | up -> none | KLHL24 not known PIKK/stress target. |

**Why likely real, not noise**

This appears in multiple batches and multiple machinery classes. However, it is not always wrong: the model correctly used a cell-type/core-gene filter for rows like `Pafah1b1_Pmp22`, `Mcm4_Zfp263`, and `Wdr3_H3f3b`.

**Prompt-rule implication**

```text
Housekeeping or core-gene status can support none, but it is not decisive. Check whether the perturbation hits the same complex/module or a stress program that specifically changes that target class.
```

## Correct Reasoning Anchors To Preserve

These are cases where the model's reasoning style appears useful and should not be destroyed by prompt edits.

| Pattern | Example rows | Why preserve |
|---|---|---|
| Direct canonical target dependency | `Ikbkb_Bcl2a1d`, `Mbtps2_Manf`, `Tyk2_Ms4a4c`, `Vhl_Mgarp` | Strong pathway-to-target links were correct. |
| Canonical stress target match | `Psmg4_Sqstm1`, `Tmem258_Dnajc3`, `Ddost_Ddit3` | The target is a known output of the stress program. |
| Cell-type expression filter | `Pafah1b1_Pmp22`, `Mcm4_Zfp263`, `Ppp2r2a_Lix1` | Avoids false directional calls for irrelevant target genes. |
| Weak indirect mechanism rejected | `Bloc1s1_Eif5`, `Dnajc8_Ctsh`, `Dph3_Bst1`, `Jak1_Akr1a1` | Good skepticism for non-specific links. |
| Specific transcriptional derepression | `Ncor2_Pf4`, `Nelfa_Pf4` | Derepression can be valid when perturbation and target regulon match. |

## Rejected Or Downweighted Patterns

| Pattern | Decision | Reason |
|---|---|---|
| Global overprediction of `down` | Reject as primary target | Strong in batch 1, but not in batch 2, batch 3, or val75 prediction counts. |
| Invalid/parser rows | Downweight | Examples: `Tbc1d10b_Creg1`, `Ddb1_Snhg1`, `Mideas_Bcl2a1d`, `Pafah1b1_Pilra`, `Pdcd10_2500002B13Rik`. These may be format/parser issues. |
| Single gene-family quirks | Downweight | Individual biology mistakes should not drive prompt rules unless they repeat as a reasoning pattern. |
| Add more biological facts | Reject for now | The issue is not lack of facts; it is overconfident use of plausible facts. |

## Highest-Value Prompt Optimization Target

The biggest prompt improvement should be a **decision discipline layer**, not a longer biology encyclopedia.

The rule should force the model to classify its proposed mechanism before choosing a label:

```text
1. Is this a direct, target-specific dependency?
2. Is this a canonical stress/pathway target?
3. Is this only generic pathway membership or machinery speculation?
4. Is the pathway likely active in basal BMDMs?
5. Could feedback, derepression, or compensation flip the canonical direction?
6. If evidence is indirect and not target-specific, prefer none.
```

The most important wording should target:

```text
Do not convert plausible biology into a directional label unless the target is a specific output of the perturbed mechanism in BMDMs.
```
