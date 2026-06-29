import os

import requests
import streamlit as st
import html

# Base URL of the FastAPI backend (override with API_URL env var if needed)
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! Ask me anything."}
        ]


def get_response(user_message: str, kb_type: str) -> str:
    """Call the FastAPI /infer endpoint and return the prediction."""
    try:
        resp = requests.post(
            f"{API_URL}/infer",
            json={"prompt": user_message, "kb_type": kb_type},
            timeout=60,
        )
        resp.raise_for_status()
        return resp.json()["prediction"]
    except requests.exceptions.ConnectionError:
        return f"⚠️ Could not reach the backend at {API_URL}. Is the FastAPI server running?"
    except requests.exceptions.HTTPError as e:
        try:
            detail = resp.json().get("detail", "")
        except Exception:
            detail = resp.text
        return f"⚠️ Backend error ({resp.status_code}): {detail or e}"
    except requests.exceptions.RequestException as e:
        return f"⚠️ Request failed: {e}"


def main():
    st.set_page_config(page_title="Bedrock KB Chat", page_icon="💬")
    init_state()

    st.title("Bedrock Knowledge Base Chat")
    st.write("Type a message below and send it to query the knowledge base.")

    with st.sidebar:
        st.header("Settings")
        kb_type = st.selectbox(
            "Knowledge base",
            options=["managed", "self_managed"],
            help="`managed` uses retrieve; `self_managed` uses retrieve_and_generate.",
        )
        st.caption(f"Backend: {API_URL}")

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Your message", "")
        submit = st.form_submit_button("Send")

    if submit and user_input.strip():
        st.session_state.messages.insert(0, {"role": "user", "content": user_input.strip()})
        with st.spinner("Querying the knowledge base..."):
            response = get_response(user_input.strip(), kb_type)
        st.session_state.messages.insert(1, {"role": "assistant", "content": response})

    for message in st.session_state.messages:
        content = html.escape(message["content"])
        if message["role"] == "user":
            bubble = (
                f"<div style=\"background-color:#E6F7FF;padding:10px;border-radius:8px;margin:10px 0;\">"
                f"<strong>You:</strong> {content}"
                "</div>"
            )
        else:
            bubble = (
                f"<div style=\"background-color:#F1F8F9;padding:10px;border-radius:8px;margin:10px 0;\">"
                f"<strong>Assistant:</strong> {content}"
                "</div>"
            )
        st.markdown(bubble, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
