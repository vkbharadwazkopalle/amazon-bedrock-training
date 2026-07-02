"""A small coding agent built on Amazon Bedrock.

Two capabilities:
  * generate_project - scaffold a new project from a natural-language prompt.
  * review_file      - give detailed, constructive review comments on a file.

The agent talks to Bedrock through the boto3 `bedrock-runtime` Converse API,
which gives one model-agnostic request shape for any supported model.
"""

import json
import os
from pathlib import Path

import boto3
import dotenv

from prompts import GENERATE_SYSTEM_PROMPT, REVIEW_SYSTEM_PROMPT

dotenv.load_dotenv()

REGION = os.getenv("AWS_REGION", "us-east-1")
# Bedrock uses inference-profile IDs; override this with whatever model you
# have enabled in your account (see .env.example).
MODEL_ID = os.getenv(
    "BEDROCK_MODEL_ID", "openai.gpt-oss-20b-1:0"
)
# For gpt-oss reasoning models: how much to "think" before answering.
# low | medium | high. Lower leaves more of maxTokens for the actual answer.
REASONING_EFFORT = os.getenv("REASONING_EFFORT", "low")

bedrock_runtime = boto3.client("bedrock-runtime", region_name=REGION)


def chat(history: list[dict], system_prompt: str, max_tokens: int = 8192) -> str:
    """Send a full conversation history to Bedrock and return the reply.

    Bedrock's Converse API is stateless, so callers keep the running history
    (a list of {"role", "content"} dicts) and pass it in each turn. Extra keys
    on a history entry are ignored, so callers can attach their own metadata.
    """
    messages = [
        {"role": m["role"], "content": [{"text": m["content"]}]} for m in history
    ]
    params = {
        "modelId": MODEL_ID,
        "system": [{"text": system_prompt}],
        "messages": messages,
        "inferenceConfig": {"maxTokens": max_tokens, "temperature": 0.2},
    }
    # gpt-oss models take a reasoning_effort knob; other models (e.g. Claude)
    # reject unknown fields, so only send it for openai.* model ids.
    if MODEL_ID.startswith("openai."):
        params["additionalModelRequestFields"] = {"reasoning_effort": REASONING_EFFORT}

    response = bedrock_runtime.converse(**params)
    return _response_text(response)


def _response_text(response: dict) -> str:
    """Pull the final answer out of a Converse reply.

    Reasoning models such as openai.gpt-oss-* return several content blocks: a
    `reasoningContent` block (the chain-of-thought) plus a `text` block (the
    actual answer). We keep only the text blocks. If the reply is all reasoning
    (e.g. it was truncated), fall back to the reasoning text so something shows.
    """

    print("Response from Bedrock:", response)  # Debugging line
    
    blocks = response["output"]["message"]["content"]
    texts = [b["text"] for b in blocks if "text" in b]
    if texts:
        return "\n".join(texts).strip()
    for b in blocks:
        reasoning = (
            b.get("reasoningContent", {}).get("reasoningText", {}).get("text")
        )
        if reasoning:
            return reasoning.strip()
    return ""


def _invoke(system_prompt: str, user_prompt: str, max_tokens: int = 8192) -> str:
    """Send one stateless prompt to Bedrock and return the text reply."""
    history = [{"role": "user", "content": user_prompt}]
    return chat(history, system_prompt, max_tokens)


def _extract_json(text: str) -> dict:
    """Parse a JSON object from the model reply, tolerating markdown fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        # Drop the opening fence (``` or ```json) and the closing fence.
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned
        cleaned = cleaned.rsplit("```", 1)[0]

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Fall back to the outermost { ... } block.
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start == -1 or end == -1:
            raise ValueError("Model did not return valid JSON.")
        return json.loads(cleaned[start : end + 1])


def generate_project(prompt: str) -> dict:
    """Generate a project scaffold from a natural-language description.

    Returns a dict with keys: project_name, summary, files, run_instructions.
    """
    reply = _invoke(GENERATE_SYSTEM_PROMPT, prompt)
    project = _extract_json(reply)

    if not project.get("files"):
        raise ValueError("The model returned no files for this project.")
    return project


def write_project(project: dict, output_dir: str) -> list[str]:
    """Write a generated project to disk under output_dir.

    Returns the list of written paths (relative to output_dir). Guards against
    path traversal so a generated path can't escape the output directory.
    """
    root = Path(output_dir).resolve()
    root.mkdir(parents=True, exist_ok=True)

    written = []
    for file in project["files"]:
        dest = (root / file["path"]).resolve()
        if not dest.is_relative_to(root):
            raise ValueError(f"Unsafe file path rejected: {file['path']}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(file["content"], encoding="utf-8")
        written.append(str(dest.relative_to(root)))
    return written


def review_file(path: str) -> str:
    """Read a file and return detailed, constructive review comments (Markdown)."""
    content = Path(path).read_text(encoding="utf-8")
    return review_code(content, filename=Path(path).name)


def format_file_for_review(content: str, filename: str = "file") -> str:
    """Wrap file content (with line numbers) into a first review message.

    Numbering the lines lets the model reference them precisely. Use this to
    seed a stateful review chat, then send follow-up questions as plain text.
    """
    numbered = "\n".join(
        f"{i:>4} | {line}" for i, line in enumerate(content.splitlines(), start=1)
    )
    return f"Please review `{filename}`:\n\n```\n{numbered}\n```"


def review_code(content: str, filename: str = "file") -> str:
    """Review raw file content (single-shot) and return Markdown."""
    user_prompt = format_file_for_review(content, filename)
    return _invoke(REVIEW_SYSTEM_PROMPT, user_prompt, max_tokens=4096)
