import os
import json

from flask import Flask, request, jsonify
import boto3
from botocore.exceptions import BotoCoreError, ClientError

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization,Access-Control-Allow-Origin,Access-Allow-Control-Origin,access-allow-control-origin"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

DEFAULT_MODEL_ID = os.environ.get("BEDROCK_MODEL_ID", "mistral.mistral-large-2402-v1:0")
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")


def build_prompt(messages):
    prompt_parts = []
    for message in messages:
        role = message.get("role", "user").lower()
        content = message.get("content", "")
        if role == "system":
            prompt_parts.append(f"System: {content}")
        elif role == "assistant":
            prompt_parts.append(f"Assistant: {content}")
        else:
            prompt_parts.append(f"User: {content}")
    prompt_parts.append("Assistant:")
    return "\n".join(prompt_parts)


@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return ('', 204)
    payload = request.get_json(force=True, silent=True)
    if payload is None:
        return jsonify(error="Invalid JSON payload"), 400

    messages = payload.get("messages")
    if not isinstance(messages, list):
        return jsonify(error="messages must be a list"), 400

    model_id = payload.get("model_id") or DEFAULT_MODEL_ID
    if not model_id:
        return jsonify(error="Model ID not configured"), 400

    prompt = build_prompt(messages)
    if not prompt.strip():
        return jsonify(error="messages cannot be empty"), 400

    # Try several common payload formats if the model rejects the first one with a validation error.
    payload_variants = [
        {"inputText": prompt},
        {"input": prompt},
        {"text": prompt},
        {"messages": [{"role": "user", "content": prompt}]},
        prompt,
    ]

    last_validation_error = None
    for variant in payload_variants:
        if isinstance(variant, str):
            body = variant.encode("utf-8")
            content_type = "text/plain"
        else:
            body = json.dumps(variant).encode("utf-8")
            content_type = "application/json"

        try:
            response = bedrock_client.invoke_model(
                modelId=model_id,
                contentType=content_type,
                accept="application/json",
                body=body,
            )

            response_body = response["body"].read()
            response_text = response_body.decode("utf-8")
            try:
                result = json.loads(response_text)
            except ValueError:
                result = response_text

            if isinstance(result, dict):
                model_output = result.get("outputText") or result.get("generatedText") or result.get("body") or result
            else:
                model_output = result

            return jsonify(model_id=model_id, output=model_output, used_payload=variant), 200

        except ClientError as err:
            # If it's a validation error, try the next payload variant.
            err_code = None
            try:
                err_code = err.response.get("Error", {}).get("Code")
            except Exception:
                err_code = None

            if err_code == "ValidationException" or "Validation" in str(err):
                last_validation_error = err
                continue
            return jsonify(error=str(err)), 500

        except BotoCoreError as err:
            return jsonify(error=str(err)), 500

    # If we exhausted variants, return the last validation error.
    if last_validation_error:
        return jsonify(error=str(last_validation_error)), 400
    return jsonify(error="Unable to invoke model"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")), debug=True)
