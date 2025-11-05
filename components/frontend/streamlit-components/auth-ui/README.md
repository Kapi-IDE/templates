# Streamlit Auth UI

Reusable login/signup/logout component for Streamlit apps.

## Install
```bash
pip install streamlit
```

## Usage
```python
import streamlit as st
from auth import render_auth_ui

session = render_auth_ui(st.session_state)
if session.is_authenticated:
    st.write(f"Welcome {session.user['email']}")
```
