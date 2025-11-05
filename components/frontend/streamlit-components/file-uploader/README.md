# Streamlit File Uploader

Reusable uploader with validation, progress tracking, and file list display.

## Install
```bash
pip install streamlit
```

## Usage
```python
import streamlit as st
from file_uploader import render_uploader

uploaded_files = render_uploader(accept=['pdf', 'docx'], max_files=3)
for file in uploaded_files:
    st.write(file.name, file.size)
```
