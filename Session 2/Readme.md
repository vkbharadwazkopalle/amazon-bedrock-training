# Session 2: Working with the Bedrock API – Foundations 

## Introduction to the Bedrock SDKs for various languages (Python, Node.js,....).
## Authentication and Authorization Methods.
## Core API Endpoints - Model Invocation, Parameter Configuration, Response Handling.
## Hands-on: Simple model invocation – Sending a prompt and receiving a response using the Python SDK.

# Code examples

# /client
Bearbones Html & JS application for LLM chat.

# /python-sdk

# app.py — Flask Bedrock Chat Proxy

## Overview

`app.py` is a small Flask application that proxies chat-style requests to an Amazon Bedrock model via the `boto3` `bedrock-runtime` client. It exposes a health endpoint and a `/chat` endpoint which accepts a list of chat messages, builds a prompt, and invokes the configured model.

## Key behaviors

- Adds permissive CORS headers to every response.
- Builds a single text prompt from a list of `messages` (system, user, assistant roles).
- Attempts several common payload shapes when invoking the Bedrock model to handle validation differences across models.
- Decodes model responses and returns a JSON envelope with the chosen model ID, output, and the payload used.

## Endpoints

- `GET /health`
  - Returns `{ "status": "ok" }` (200).

- `POST /chat`
  - Accepts JSON body with at least the `messages` key.
  - `messages` must be a list of message objects: `{ "role": "user|assistant|system", "content": "..." }`.
  - Optional `model_id` field overrides the default model.
  - Returns JSON `{ "model_id": ..., "output": ..., "used_payload": ... }` on success.
  - Returns appropriate error codes and messages for invalid payloads and invocation errors.

## Prompt construction

The `build_prompt(messages)` function converts the list into a single plaintext prompt where each message is prefixed by its role label:

- `system` → `System: ...`
- `assistant` → `Assistant: ...`
- other (or `user`) → `User: ...`

The prompt ends with `Assistant:` to elicit a generated assistant response.

## Model invocation details

- The app uses `boto3.client("bedrock-runtime", region_name="us-east-1")` to call `invoke_model`.
- Default model id: read from `BEDROCK_MODEL_ID` environment variable; fallback: `mistral.mistral-large-2402-v1:0`.
- The code tries multiple payload shapes (e.g. `{"inputText": prompt}`, `{"input": prompt}`, `{"text": prompt}`, `{"messages": [...]}`, and raw string) and switches content-type between `application/json` and `text/plain` as appropriate.
- If the model returns JSON, the app looks for common fields like `outputText`, `generatedText`, or `body` and falls back to the whole result.

## Environment variables

- `BEDROCK_MODEL_ID` — optional default model identifier used if `model_id` isn't provided in the request.
- `PORT` — optional; Flask port (default `8080`).
- AWS credentials and config must be available to `boto3` (environment, profile, or IAM role). Ensure region and credentials allow Bedrock invocation.

## Running locally

Install dependencies (example using pip):

```bash
pip install -r requirements.txt
```

Run the app:

```bash
python app.py
```

Or set `PORT` and a model id and run:

```bash
export BEDROCK_MODEL_ID="mistral.mistral-large-2402-v1:0"
export PORT=8080
python app.py
```

## Example requests

Example `messages` payload (curl):

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain the difference between HTTP and HTTPS."}
    ]
  }'
```

Successful response sample:

```json
{
  "model_id": "mistral.mistral-large-2402-v1:0",
  "output": "HTTPS is HTTP over TLS/SSL...",
  "used_payload": {"inputText": "System: You are a helpful assistant.\nUser: Explain the difference between HTTP and HTTPS.\nAssistant:"}
}
```

## Error handling & troubleshooting

- If `messages` is missing or not a list, the endpoint returns `400` with a helpful message.
- If the model returns a validation error, the app iterates payload variants and may return `400` with the last validation error.
- Boto/Client errors return `500` (or `400` for exhausted validation attempts).
- Check AWS credentials and region configuration if you see authentication or permission errors.

## Notes and possible improvements

- Add stricter validation on message content and length limits to avoid very long prompts.
- Consider streaming responses if using models that can stream partial outputs.
- Make `region_name` configurable via environment variable.
- Add structured logging and request IDs for better observability.

---

Generated from `Session 2/python-sdk/app.py`.

## `chat_cli.py` — Interactive CLI for Bedrock Conversation API

### Overview

`chat_cli.py` is a minimal command-line chat client that demonstrates using the Bedrock `converse` API via `boto3` to run a multi-turn conversation with the Mistral model.

### How it works

- Creates a `boto3` client for `bedrock-runtime` (region `us-east-1` hardcoded).
- Uses a `conversation` list of message objects where each entry is `{ "role": "user|assistant", "content": [{"text": "..."}] }` to maintain context across turns.
- Calls `client.converse(modelId=model_id, messages=conversation, inferenceConfig={...})` and extracts the assistant reply from `response["output"]["message"]["content"][0]["text"]`.

### Configuration

- `model_id` is currently hardcoded to `mistral.mistral-large-2402-v1:0` inside the script. Replace with your preferred model id or make it configurable via environment variable/CLI flag.
- `region_name` is set to `us-east-1`; ensure your AWS credentials and region allow Bedrock access.

### Running

1. Ensure AWS credentials are available (environment variables, AWS profile, or IAM role).
2. Run the script with Python 3:

```bash
python Session\ 2/python-sdk/chat_cli.py
```

Type messages at the prompt. Enter `exit` to quit.

### Example session

You: Hello

Mistral AI: Hi — how can I help today?
