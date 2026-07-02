# Session 5: A Simple Coding Agent on Amazon Bedrock

A small, readable coding agent that runs on Amazon Bedrock with a Streamlit UI.
Both features are **stateful chats** - the agent remembers the conversation, so
you can iterate turn by turn.

It can:
- **Generate a project from scratch** from a natural-language prompt, with clean
  code and a sensible architecture, and write it to disk. Follow up with changes
  ("add tests", "use SQLite instead") and it rewrites the project each turn.
- **Review a code file** and return detailed, constructive comments, then answer
  follow-up questions with the file and prior answers still in context.

## Architecture

```
app.py            Streamlit client - two stateful chat tabs
bedrock_agent.py  Agent core - Bedrock Converse calls + safe project writer
prompts.py        System prompts for generation and review
```

The agent uses the boto3 `bedrock-runtime` **Converse** API, which gives one
model-agnostic request shape. Converse is stateless, so each chat keeps its full
message history in Streamlit's session state and replays it on every turn. The
UI calls the agent module directly - no separate backend service to run.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env      # then edit AWS_REGION / BEDROCK_MODEL_ID
```

Make sure the model in `BEDROCK_MODEL_ID` is enabled under
**Bedrock > Model access** in your AWS account, and that your AWS credentials
are available (env vars, `~/.aws/credentials`, or an attached role).

## Run

```bash
streamlit run app.py
```

- **Generate project:** describe what you want, pick an output folder, and the
  agent scaffolds the files to disk.
- **Review code:** point at a local file path (or upload a file) to get feedback.
