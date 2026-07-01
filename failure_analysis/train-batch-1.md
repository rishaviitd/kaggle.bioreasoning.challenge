Here is the clean picture.

| Group          | Count |
| -------------- | ----: |
| True up        |     6 |
| True down      |     6 |
| True none      |     6 |
| Predicted up   |     3 |
| Predicted down |    11 |
| Predicted none |     4 |
| Invalid        |     1 |

So the model is **overpredicting `down` heavily**.

Confusion matrix:

```text
labels = [up, down, none]

true up:    up=2, down=3, none=1
true down:  up=1, down=4, none=1
true none:  up=0, down=4, none=2
```

Main pattern:

```text
It predicts down for 11/18 rows.
```

Wrong rows:

| id             | true | predicted |
| -------------- | ---: | --------: |
| Pfn1_Ccr5      |   up |      down |
| Stag2_Gclm     |   up |      down |
| Actl6a_Ifi27   |   up |      down |
| Sec13_Gbf1     |   up |      none |
| Il10ra_Saa3    | down |        up |
| Tcp1_St3gal5   | down |      none |
| Atf4_Ifih1     | none |      down |
| Tbc1d10b_Creg1 | none |   invalid |
| Junb_Spryd7    | none |      down |
| Wdr3_Mthfd1    | none |      down |
| Ly96_Cfp       | none |      down |

What this says:

```text
1. Base prompt is too willing to infer loss-of-function -> target decreases.
2. It overuses “knockdown reduces pathway activity, therefore downstream gene down.”
3. It underuses “none” when the relation is indirect/speculative.
4. It misses up cases where knockdown causes derepression or compensatory stress activation.
```

For manual prompt optimization, the first useful rule should probably target this exact bias:

```text
Do not predict down just because the perturbed gene is broadly required for transcription, signaling, chromatin, ribosome, or cell state. Predict down only when there is a specific causal path showing the target depends on the perturbed gene’s positive activity. If the path is generic or speculative, prefer none.
```

And for up cases:

```text
Before predicting down from loss of function, check whether the perturbation removes a repressor, activates stress compensation, or derepresses inflammatory/interferon/lysosomal programs.
```

Yes, now the reasoning patterns are much clearer.

The main problem is not random. The model has a **strong mechanistic overreach bias**: it invents a plausible pathway and then treats that pathway as enough evidence for a directional label.

**Core Failure Patterns**

1. **“Loss of positive regulator -> target down” is overused**

This is the biggest one.

Examples:

| Row            | True | Pred | Model’s reasoning mistake                                  |
| -------------- | ---: | ---: | ---------------------------------------------------------- |
| `Pfn1_Ccr5`    |   up | down | Pfn1 loss weakens actin/TLR/NF-kB, so Ccr5 down            |
| `Stag2_Gclm`   |   up | down | cohesin loss weakens enhancer-promoter loops, so Gclm down |
| `Actl6a_Ifi27` |   up | down | BAF loss reduces ISG promoter accessibility, so Ifi27 down |
| `Atf4_Ifih1`   | none | down | ATF4 supports IFN/ISG signaling, so Ifih1 down             |
| `Junb_Spryd7`  | none | down | JunB activates AP-1 targets, so Spryd7 down                |
| `Ly96_Cfp`     | none | down | Ly96 loss weakens TLR4/NF-kB, so Cfp down                  |

This is why predicted labels were:

```text
down = 11 / 18
```

The model often assumes: if perturbation gene helps a pathway, knockdown lowers target. That is too aggressive.

2. **It treats broad pathway plausibility as sufficient evidence**

The model says things like:

```text
actin dynamics are required for TLR signaling
cohesin supports enhancer-promoter contacts
BAF opens chromatin for ISGs
TLR4 activates NF-kB inflammatory genes
ribosome biogenesis drives one-carbon metabolism
```

These are biologically plausible, but too generic. It does not ask:

```text
Is this specific target actually dependent enough to move in this dataset?
Is the pathway active in basal BMDMs?
Is the effect direct enough?
Would this pass significance threshold?
```

This causes many false `down`.

3. **It underuses `none` for indirect/speculative links**

For rows truly `none`, it often still predicts a direction:

| Row           | True | Pred | Reasoning                                  |
| ------------- | ---: | ---: | ------------------------------------------ |
| `Atf4_Ifih1`  | none | down | ATF4 -> IFN-beta -> ISG                    |
| `Junb_Spryd7` | none | down | JunB/AP-1 direct activation claim          |
| `Wdr3_Mthfd1` | none | down | ribosome stress -> lower nucleotide demand |
| `Ly96_Cfp`    | none | down | TLR4/NF-kB -> complement gene              |

So the base prompt lacks a strong rule like:

```text
If the mechanism is indirect, generic, stimulus-dependent, or based only on pathway membership, prefer none.
```

4. **It hallucinates evidence with high confidence**

Most obvious:

```text
Junb_Spryd7
```

It claims public ChIP-seq promoter peaks and published knockdown evidence. That may sound strong, but the label is `none`, so this kind of “specific evidence” can be fabricated or irrelevant.

This is dangerous because the reasoning looks authoritative even when wrong.

5. **Some correct rows may still be fragile**

Correct examples:

| Row              | True | Pred | Why maybe fragile                                                                                             |
| ---------------- | ---: | ---: | ------------------------------------------------------------------------------------------------------------- |
| `Traf2_Ctsk`     |   up |   up | Uses a nuanced TRAF2 negative-regulator/RANK argument. Good if true, but very specific.                       |
| `Stag2_Cpe`      | down | down | Same broad cohesin-loss logic that failed for `Stag2_Gclm`. Correct here, but the rule is not generally safe. |
| `Actr6_Glrx`     | down | down | Actin/ROS/Nrf2 chain, plausible but indirect.                                                                 |
| `Atp6ap2_Ms4a6b` | down | down | V-ATPase/TLR/NF-kB logic, plausible but could overgeneralize.                                                 |

So even correct predictions are often produced by the same broad “pathway dependency” reasoning that creates wrong answers elsewhere.

**Prompt Clue**
The first manual prompt improvement should not add more biology. It should add a **decision discipline rule**:

```text
Do not predict down merely because knockdown weakens a broad pathway, chromatin complex, translation/ribosome process, cytoskeleton process, or immune signaling adaptor.

Only predict down when the target is specifically and strongly dependent on that perturbation’s positive activity in BMDMs.

If the argument is indirect, stimulus-dependent, generic stress/pathway membership, or lacks target-specific evidence, choose none.
```

And a second rule for missed `up`:

```text
Before predicting down from loss of function, check for compensatory activation, derepression, stress-response induction, or loss of a negative regulator.
```

That directly attacks what the model is doing wrong here.
