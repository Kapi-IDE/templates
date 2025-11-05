import io
import os
from typing import Optional

import requests
import streamlit as st

from components.llm_selector import render_llm_selector

API_URL = os.getenv("DEEP_DOC_API_URL", "http://localhost:8000")


st.set_page_config(page_title="Deep Document Analysis", layout="wide")
st.title("🔍 Deep Document Analysis Workbench")

provider = render_llm_selector()
model = st.sidebar.text_input("Custom model (optional)", value=provider.default_model)
temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
collection = st.sidebar.text_input("Collection", value="default")

st.sidebar.markdown("---")
st.sidebar.subheader("Ingest Documents")

uploaded_file = st.sidebar.file_uploader("Upload PDF/Text", type=["pdf", "txt", "md"])
if uploaded_file:
    with st.sidebar.form("upload-form"):
        st.write(f"Selected: {uploaded_file.name}")
        submitted = st.form_submit_button("Ingest file")
        if submitted:
            files = {"upload": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            params = {"collection": collection}
            resp = requests.post(f"{API_URL}/ingest/file", files=files, params=params, timeout=120)
            if resp.ok:
                st.sidebar.success(f"Indexed {resp.json()['chunks_indexed']} chunks")
            else:
                st.sidebar.error(resp.text)

with st.sidebar.form("url-form"):
    url = st.text_input("Ingest from URL")
    if st.form_submit_button("Fetch & Ingest") and url:
        payload = {"url": url, "collection": collection}
        resp = requests.post(f"{API_URL}/ingest/url", json=payload, timeout=120)
        if resp.ok:
            st.sidebar.success(f"Indexed {resp.json()['chunks_indexed']} chunks from URL")
        else:
            st.sidebar.error(resp.text)

with st.sidebar.form("text-form"):
    text_title = st.text_input("Manual title", key="text-title")
    text_body = st.text_area("Paste text")
    if st.form_submit_button("Add text") and text_body:
        payload = {"title": text_title or "manual-entry", "text": text_body, "collection": collection}
        resp = requests.post(f"{API_URL}/ingest/text", json=payload, timeout=120)
        if resp.ok:
            st.sidebar.success(f"Indexed {resp.json()['chunks_indexed']} chunks")
        else:
            st.sidebar.error(resp.text)

st.markdown("## Ask a question")
question = st.text_area("Enter a question about your documents", height=120)
if st.button("Run deep analysis") and question:
    payload = {
        "question": question,
        "provider": provider.value,
        "model": model or None,
        "temperature": float(temperature),
        "collection": collection,
    }
    with st.spinner("Thinking..."):
        resp = requests.post(f"{API_URL}/query", json=payload, timeout=120)
    if resp.ok:
        data = resp.json()
        st.success(data["answer"])
        st.caption(f"Provider: {data['provider']} | Model: {data['model']} | Pricing: {data.get('price_estimate', 'n/a')}")
        with st.expander("Context Chunks"):
            for idx, chunk in enumerate(data["context"], start=1):
                st.markdown(f"**Chunk {idx}**\n\n{chunk}")
    else:
        st.error(resp.text)
