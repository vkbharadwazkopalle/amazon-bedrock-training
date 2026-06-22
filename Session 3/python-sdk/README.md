# Session 3 Python SDK Reference

This directory contains Bedrock prompt engineering samples that demonstrate zero-shot, one-shot, chain-of-thought, and parameter-tuning patterns using the Python SDK.

## Prerequisites

- Python 3.9+
- `boto3`
- AWS credentials configured for Amazon Bedrock access
- A Bedrock-enabled region such as `us-east-1`

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Script documentation

### 1. chain_of_thought.py

- Purpose: demonstrates chain-of-thought prompting by asking the model to explain its reasoning before answering.
- Technique: instructs the model to reason step-by-step for a complex question.
- Model: `google.gemma-3-12b-it`
- API used: `invoke_model`
- Input shape: a system message plus a user prompt encoded as JSON.
- Output handling: parses the Bedrock response from either `outputText` or the `body` payload.

Run:

```bash
python chain_of_thought.py
```

### 2. one_shot.py

- Purpose: shows how a single example can guide the model toward the desired output format or style.
- Technique: provides one completed example followed by a new request to be solved in the same pattern.
- Model: `google.gemma-3-12b-it`
- API used: `invoke_model`
- Input shape: a system instruction, one demonstration pair, and a new user prompt.
- Output handling: reads the response content from the Bedrock JSON payload.

Run:

```bash
python one_shot.py
```

### 3. parameter_tuning.py

- Purpose: compares how different inference parameters change response behavior.
- Technique: evaluates the effect of temperature and top-p settings on determinism and creativity.
- Model: `google.gemma-3-12b-it`
- API used: `converse`
- Input shape: a prompt plus inference configuration such as `maxTokens`, `temperature`, and `topP`.
- Output handling: prints two responses generated with different parameter settings.

Run:

```bash
python parameter_tuning.py
```

### 4. zero_shot.py

- Purpose: demonstrates zero-shot prompting with no examples, relying on the model's pretrained reasoning ability.
- Technique: gives a direct instruction and expects the model to infer the task from the prompt alone.
- Model: `google.gemma-3-12b-it`
- API used: `invoke_model`
- Input shape: a system message and a single user instruction.
- Output handling: parses the Bedrock response and prints the resulting generated text.

Run:

```bash
python zero_shot.py
```

## Notes

- These samples are intended for learning and experimentation rather than production deployment.
- Update the model ID and region if your account or environment uses a different Bedrock model or endpoint.
- For best results, ensure your AWS credentials and IAM permissions allow Bedrock runtime access.
