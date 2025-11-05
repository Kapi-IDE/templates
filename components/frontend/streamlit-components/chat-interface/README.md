# Streamlit Chat Interface

Drop-in chat UI for Streamlit apps with streaming responses and citation support.

## Install
```bash
pip install streamlit
```

## Usage
```python
import streamlit as st
from chat_interface import render_chat

conversation = render_chat(messages=[], title="Legal Assistant")
```
