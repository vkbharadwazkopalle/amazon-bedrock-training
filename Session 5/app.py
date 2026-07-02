"""Streamlit client for the Bedrock coding agent.

Two stateful chats:
  * Generate project - describe what you want, then iterate ("add tests",
    "use SQLite instead"); the agent remembers the conversation and rewrites
    the project to disk each turn.
  * Review code      - load a file, get a review, then ask follow-up questions
    about it - the file and prior answers stay in context.

Bedrock's Converse API is stateless, so each chat keeps its full history in
st.session_state and replays it on every turn.

Run with:  streamlit run app.py
"""

import os
from pathlib import Path

import streamlit as st

from bedrock_agent import (
    MODEL_ID,
    _extract_json,
    chat,
    format_file_for_review,
    write_project,
)
from prompts import GENERATE_SYSTEM_PROMPT, REVIEW_SYSTEM_PROMPT


def render_project(project: dict, written: list[str], output_dir: str):
    """Render a generated project (summary + files) inside a chat bubble."""
    st.markdown(f"**{project.get('project_name', 'project')}** - "
                f"{project.get('summary', '')}")
    if project.get("run_instructions"):
        st.markdown("**How to run:**")
        st.code(project["run_instructions"])
    for file in project.get("files", []):
        with st.expander(file["path"]):
            st.code(file["content"])
    if written:
        st.caption(f"Wrote {len(written)} files to `{output_dir}/`")


def generate_tab():
    st.subheader("Generate a project from a prompt")
    col1, col2 = st.columns([3, 1])
    output_dir = col1.text_input("Output folder", value="generated_project")
    if col2.button("Clear chat", key="clear_gen"):
        st.session_state.gen_msgs = []

    st.session_state.setdefault("gen_msgs", [])

    # Replay the conversation so far.
    for msg in st.session_state.gen_msgs:
        with st.chat_message(msg["role"]):
            if msg.get("project"):
                render_project(msg["project"], msg.get("written", []), output_dir)
            else:
                st.markdown(msg["content"])

    prompt = st.chat_input("Describe the project, or ask for a change...")
    if not prompt:
        return

    st.session_state.gen_msgs.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Designing and writing the project..."):
                reply = chat(st.session_state.gen_msgs, GENERATE_SYSTEM_PROMPT)
                project = _extract_json(reply)
                written = write_project(project, output_dir)
        except Exception as e:  # surface Bedrock / parsing / write errors
            error = f"Generation failed: {e}"
            print(e)
            st.error(error)
            st.session_state.gen_msgs.append({"role": "assistant", "content": error})
            return
        render_project(project, written, output_dir)

    # Store the raw reply for model context, plus parsed data for re-rendering.
    st.session_state.gen_msgs.append(
        {"role": "assistant", "content": reply, "project": project, "written": written}
    )


def review_tab():
    st.subheader("Review a code file")
    st.session_state.setdefault("rev_msgs", [])
    st.session_state.setdefault("rev_file", None)  # (filename, content)

    col1, col2 = st.columns([3, 1])
    path = col1.text_input("Path to a file", placeholder="e.g. ./bedrock_agent.py")
    uploaded = col1.file_uploader("...or upload a file")
    if col2.button("Clear chat", key="clear_rev"):
        st.session_state.rev_msgs = []
        st.session_state.rev_file = None

    # Load the file to review (path takes priority over upload).
    if path.strip():
        if Path(path.strip()).is_file():
            content = Path(path.strip()).read_text(encoding="utf-8", errors="replace")
            st.session_state.rev_file = (Path(path.strip()).name, content)
        else:
            st.warning(f"No file found at `{path.strip()}`.")
    elif uploaded is not None:
        content = uploaded.getvalue().decode("utf-8", errors="replace")
        st.session_state.rev_file = (uploaded.name, content)

    if st.session_state.rev_file:
        st.caption(f"Reviewing: `{st.session_state.rev_file[0]}`")

    for msg in st.session_state.rev_msgs:
        with st.chat_message(msg["role"]):
            st.markdown(msg["display"])

    prompt = st.chat_input("Ask for a review, or a follow-up question...")
    if not prompt:
        return
    if st.session_state.rev_file is None:
        st.warning("Load a file (path or upload) before starting the review.")
        return

    # On the first turn, attach the file contents to the message the model sees.
    if not st.session_state.rev_msgs:
        filename, content = st.session_state.rev_file
        model_text = format_file_for_review(content, filename) + f"\n\n{prompt}"
    else:
        model_text = prompt

    st.session_state.rev_msgs.append(
        {"role": "user", "content": model_text, "display": prompt}
    )
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Reviewing..."):
                feedback = chat(st.session_state.rev_msgs, REVIEW_SYSTEM_PROMPT, 4096)
        except Exception as e:
            feedback = f"Review failed: {e}"
            st.error(feedback)
        else:
            st.markdown(feedback)
    st.session_state.rev_msgs.append(
        {"role": "assistant", "content": feedback, "display": feedback}
    )


def main():
    st.set_page_config(page_title="Bedrock Coding Agent", page_icon="🤖")
    st.title("🤖 Bedrock Coding Agent")
    st.caption(f"Model: `{MODEL_ID}`  ·  Region: `{os.getenv('AWS_REGION', 'us-east-1')}`")

    generate, review = st.tabs(["Generate project", "Review code"])
    with generate:
        generate_tab()
    with review:
        review_tab()


if __name__ == "__main__":
    main()
