# Session 4 - Bedrock Knowledge Bases (KB) - Data Ingestion & Retrieval Strategies
- Understanding the architecture of Bedrock KBs – Vector indexing, Similarity Search.
- Data Preparation for Bedrock KB – Cleaning and structuring your data.
- Hands-on: Importing data into a Bedrock KB – Demonstrating different ingestion methods (JSON, CSV).
- Querying the KB using semantic search and evaluating response relevance.

## local setup

### create virtual env
`python -m venv .venv/`
### activate it
`source .venv/bin/activate`
### install requirements
`pip install -r requirements.txt`
### check the installed packages
- go to `Session 4/.venv/lib`
- check if you see the `python3.xx/site-packages`
- if yes, then you are good to go
- if not proceed to activate step and follow through

## auth
- install aws cli
- using aws console or cli, create new iam user with appr privileges
- generate access key
- run the command `aws configure`
- provide the access keys & secret keys as inputs

## environment variables

Create a `.env` file in `Session 4/` with the following keys:

| Variable | Used by | Description |
| --- | --- | --- |
| `SELF_MNG_KB_ID` | `kb_retrieval.py` | Knowledge base ID queried with `retrieve_and_generate`. |
| `MNG_KB_ID` | `kb_retrieval.py` | Knowledge base ID queried with `retrieve`. |
| `MODEL_ARN` | `kb_retrieval.py` | ARN of the on-demand model Bedrock uses to generate the answer. |
| `API_URL` | `client.py` | Base URL of the FastAPI backend. Defaults to `http://127.0.0.1:8000`. |

## Examples

The session ships a small end-to-end app: a retrieval layer (`kb_retrieval.py`),
a FastAPI backend (`app.py`) that exposes it over HTTP, and a Streamlit chat UI
(`client.py`) that talks to the backend.

### kb_retrieval.py

Wraps the Bedrock Agent Runtime client and exposes two retrieval strategies:

- `query_self_managed_kb(query)` — calls `retrieve_and_generate` against
  `SELF_MNG_KB_ID` using `MODEL_ARN`, letting Bedrock both retrieve passages and
  generate a natural-language answer. Returns the generated text.
- `query_managed_kb(query)` — calls `retrieve` against `MNG_KB_ID` with a
  `managedSearchConfiguration` of up to 5 results, then joins the raw retrieved
  passages (no generation). Returns the passages separated by `---`.

### app.py

A FastAPI service that exposes the retrieval functions over HTTP.

- `GET /` — health check, returns a running message.
- `POST /infer` — accepts `{ "prompt": str, "kb_type": "managed" | "self_managed" }`.
  Routes `self_managed` to `query_self_managed_kb` and anything else to
  `query_managed_kb` (default), returning `{ prompt, kb_type, prediction }`.
  Errors surface as HTTP 500 with the exception detail.

Run it with:

`uvicorn app:app --reload`

### client.py

A Streamlit chat front end for the `/infer` endpoint.

- Sidebar lets you pick the knowledge base (`managed` vs `self_managed`).
- Sends each message to `POST {API_URL}/infer` (60s timeout) and renders the
  prediction in a simple chat transcript.
- Gracefully reports connection, HTTP, and request errors in the chat window.

Run it (with the FastAPI backend already running) with:

`streamlit run client.py`

