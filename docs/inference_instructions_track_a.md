# Track A Inference Instructions

These rules are for Track A only. Follow them strictly so local/OpenRouter
inference stays as close as possible to the repository's intended Kaggle setup.

## Target Kaggle/Repo Setup

Track A uses the fixed model:

```text
openai/gpt-oss-120b
```

The repository serves it locally with vLLM as:

```bash
uv run --extra serve vllm serve openai/gpt-oss-120b \
    --port 8000 \
    --enforce-eager \
    --no-enable-prefix-caching
```

The README states that this model is approximately 120B parameters with
`mxfp4` quantization, around 60 GB of weights.

## Required Track A Decoding Rules

Always use:

```text
temperature = 1.0
top_p = 1.0
seeds = 42, 43, 44
```

Use exactly one prompt per row. Do not use tools. Do not fine-tune. Keep the
prompt within the Track A limit of 4,096 prompt tokens.

Final predictions must be the average of the three seed-level predictions:

```text
prediction_up = mean(prediction_up_seed42, prediction_up_seed43, prediction_up_seed44)
prediction_down = mean(prediction_down_seed42, prediction_down_seed43, prediction_down_seed44)
```

## Reasoning Model Parameters

GPT-OSS-120B is a reasoning model. Use:

```text
max_completion_tokens
reasoning_effort
```

Do not use legacy `max_tokens` for serious Track A runs. The README warns that
`max_tokens` can cause reasoning models to spend the whole budget on reasoning
without producing visible answer text.

Default reasoning effort should match the current prompt-only script:

```text
reasoning_effort = "medium"
```

## OpenRouter Mimic Setup

Use the paid OpenRouter model:

```text
openai/gpt-oss-120b
```

Do not use:

```text
openai/gpt-oss-120b:free
```

The free variant does not advertise `logprobs` and `top_logprobs` support.

To mimic the repo's `mxfp4` quantized vLLM setup, prefer OpenRouter providers
that support logprobs and use fp4-like quantization:

```text
1. WandB     tag=wandb/fp4
2. Novita    tag=novita/fp4
3. Parasail  tag=parasail/fp4
```

Use WandB first unless testing shows it fails or returns unusable logprobs.

## Required OpenRouter Provider Controls

When requesting logprobs, always require parameter support and pin the provider:

```json
{
  "provider": {
    "order": ["WandB"],
    "allow_fallbacks": false,
    "require_parameters": true
  }
}
```

`require_parameters=true` is mandatory. Without it, OpenRouter may route to a
provider that ignores unsupported fields, which could silently remove logprobs.

`allow_fallbacks=false` is mandatory for controlled evaluation. If a provider
fails, test another pinned provider explicitly instead of allowing hidden
provider changes.

## OpenRouter Request Shape

For Track A logprob inference, the request should follow this shape:

```json
{
  "model": "openai/gpt-oss-120b",
  "messages": [
    {
      "role": "user",
      "content": "<prompt>"
    }
  ],
  "temperature": 1.0,
  "top_p": 1.0,
  "seed": 42,
  "max_completion_tokens": 65536,
  "reasoning_effort": "medium",
  "logprobs": true,
  "top_logprobs": 20,
  "provider": {
    "order": ["WandB"],
    "allow_fallbacks": false,
    "require_parameters": true
  }
}
```

Repeat with seeds `42`, `43`, and `44`.

## Current Codebase Notes

`examples/track_a_prompt_only.py` already uses the important reasoning-model
fields:

```text
max_completion_tokens
reasoning_effort
temperature=1.0
top_p=1.0
seed=42/43/44
```

`examples/track_a_logprobs.py` currently needs adjustment before serious
OpenRouter/Kaggle-style use because it uses:

```text
max_tokens
```

and does not send:

```text
reasoning_effort
```

Before using `examples/track_a_logprobs.py` for real runs, update it to use the
same core request parameters as `examples/track_a_prompt_only.py`, plus
OpenRouter provider controls.

## Logprob Interpretation

The logprob path should use the generated final answer token inside:

```text
<answer>A</answer>
<answer>B</answer>
<answer>C</answer>
```

Map classes as:

```text
A -> prediction_up
B -> prediction_down
C -> none, implicit as 1 - prediction_up - prediction_down
```

Use `top_logprobs` at the final answer token to derive soft class probabilities.
If logprobs are missing, invalid, or do not include A/B/C at the answer token,
the run should be treated as failed for logprob inference rather than silently
accepted.

## Provider Sanity Checks

Before running all test rows, send a tiny request to the pinned provider and
confirm:

```text
1. The response has visible answer content.
2. The response includes a non-empty logprobs object.
3. The answer-token top_logprobs include A, B, and C or token variants that the
   parser recognizes.
4. OpenRouter metadata shows the intended provider.
```

Only then run the full Track A inference.
