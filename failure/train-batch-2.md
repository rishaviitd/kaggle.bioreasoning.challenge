Batch 2 confirms the first batch was noisy.

**Batch 2 Summary**

```text
correct: 10/18
accuracy: 0.556
macro_f1: 0.609
```

Predictions are balanced:

```text
pred up:   6
pred down: 5
pred none: 7
```

So no global `down` bias here.

**Confusion Matrix**

```text
labels = [up, down, none]

true up:    up=4, down=1, none=1
true down:  up=1, down=3, none=2
true none:  up=1, down=1, none=4
```

**Wrong Rows**

| id              | true |    pred |
| --------------- | ---: | ------: |
| `Psmd4_Smpdl3a` |   up |    down |
| `Tsc2_Syngr1`   |   up |    none |
| `Ctdspl2_Xylt2` | down |      up |
| `Virma_Psma6`   | down |    none |
| `Arpc3_Vma21`   | down |    none |
| `Nolc1_Cfp`     | none |    down |
| `Ddb1_Snhg1`    | none | invalid |
| `Dcaf7_Glrx`    | none |      up |

**Reasoning Patterns**

The repeated issue is still not “too much down.” It is broader:

```text
The model over-trusts plausible biology when it sees a named pathway,
but also over-rejects links when it decides the target is housekeeping/constitutive.
```

Two recurring failure modes:

1. **False directional prediction from speculative pathway**
   - `Dcaf7_Glrx`: DCAF7 -> Nrf2 stabilization -> Glrx up.
   - `Nolc1_Cfp`: NOLC1 -> NF-kB coactivation -> Cfp down.
   - `Ctdspl2_Xylt2`: CTDSP2 loss -> TGF-beta derepression -> Xylt2 up.

2. **False none from “no direct link / housekeeping” reasoning**
   - `Arpc3_Vma21`: actin/trafficking effect treated as post-translational only, predicted none.
   - `Virma_Psma6`: PSMA6 treated as housekeeping/proteasome core, predicted none.
   - `Tsc2_Syngr1`: Syngr1 treated as neuronal/irrelevant, predicted none.

So the stable lesson across batches is:

```text
The model needs a better threshold for when indirect mechanisms count.
```

Not simply “predict less down.” More like:

```text
- Do not turn weak/speculative pathway links into directional labels.
- But also do not dismiss housekeeping/organelle/proteostasis genes as none when perturbing global RNA, proteostasis, trafficking, or chromatin machinery can shift them.
```

We should run at least one more batch before writing prompt rules.
