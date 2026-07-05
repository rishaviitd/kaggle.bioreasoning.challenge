import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

sys_msg = """Your input fields are:
1. `pert` (str): The knocked-out perturbation gene
2. `gene` (str): The target gene to predict
Your output fields are:
1. `reasoning` (str): Step-by-step biological reasoning
2. `label` (str): Final label: exactly 'up', 'down', or 'none'
All interactions will be structured in the following way, with the appropriate values filled in.

[[ ## pert ## ]]
{pert}

[[ ## gene ## ]]
{gene}

[[ ## reasoning ## ]]
{reasoning}

[[ ## label ## ]]
{label}

[[ ## completed ## ]]
In adhering to this structure, your objective is: 
        You are an expert molecular biologist who studies how genes are related using Perturb-seq."""

user_msg = """[[ ## pert ## ]]
Spi1

[[ ## gene ## ]]
Tlr4

Respond with the corresponding output fields, starting with the field `[[ ## reasoning ## ]]`, then `[[ ## label ## ]]`, and then ending with the marker for `[[ ## completed ## ]]`."""

resp = client.chat.completions.create(
    model="qwen/qwen3.5-9b",
    messages=[{"role": "system", "content": sys_msg}, {"role": "user", "content": user_msg}],
    temperature=0.0,
    max_tokens=2048,
    logprobs=True,
    top_logprobs=15
)
print(json.dumps(resp.model_dump(), indent=2))
