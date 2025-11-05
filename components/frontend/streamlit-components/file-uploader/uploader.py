"""Reusable Streamlit file uploader component."""

import streamlit as st
from typing import Optional, List, Callable
from pathlib import Path

def file_uploader(
    label: str = "Upload files",
    allowed_types: List[str] = None,
    max_size_mb: int = 10,
    help_text: str = None,
    key: str = "file_uploader"
) -> Optional[object]:
    """Render file uploader with validation.

    Args:
        label: Uploader label text
        allowed_types: List of allowed file extensions (e.g., ['pdf', 'txt'])
        max_size_mb: Maximum file size in MB
        help_text: Help text to display
        key: Streamlit widget key

    Returns:
        Uploaded file object or None
    """
    if allowed_types is None:
        allowed_types = ["pdf", "txt", "docx", "csv"]

    help_msg = help_text or f"Allowed: {', '.join(allowed_types.upper())}. Max size: {max_size_mb}MB"

    uploaded_file = st.file_uploader(
        label,
        type=allowed_types,
        help=help_msg,
        key=key,
        label_visibility="collapsed"
    )

    # Validate file size
    if uploaded_file and uploaded_file.size > max_size_mb * 1024 * 1024:
        st.error(f"File too large! Max size: {max_size_mb}MB")
        return None

    return uploaded_file


def upload_with_progress(
    uploaded_file: object,
    upload_function: Callable,
    success_callback: Callable = None
) -> bool:
    """Upload file with progress indicator.

    Args:
        uploaded_file: Streamlit uploaded file object
        upload_function: Function to call for upload (should accept file)
        success_callback: Optional callback on successful upload

    Returns:
        True if upload successful, False otherwise
    """
    if not uploaded_file:
        return False

    with st.spinner(f"Uploading {uploaded_file.name}..."):
        try:
            result = upload_function(uploaded_file)

            if result:
                st.success(f"✅ Uploaded: {uploaded_file.name}")
                if success_callback:
                    success_callback(uploaded_file.name)
                return True
            else:
                st.error("Upload failed")
                return False

        except Exception as e:
            st.error(f"Upload error: {str(e)}")
            return False


def render_uploaded_files_list(files: List[str]):
    """Display list of uploaded files.

    Args:
        files: List of uploaded file names
    """
    if not files:
        st.info("No files uploaded yet")
        return

    st.markdown("#### 📚 Uploaded Files")
    for file in files:
        col1, col2 = st.columns([0.9, 0.1])
        with col1:
            st.markdown(f"• {file}")
        with col2:
            if st.button("🗑️", key=f"delete_{file}", help=f"Delete {file}"):
                return file  # Return file to delete

    return None


def validate_file_type(file_name: str, allowed_types: List[str]) -> bool:
    """Validate file extension.

    Args:
        file_name: Name of the file
        allowed_types: List of allowed extensions

    Returns:
        True if valid, False otherwise
    """
    ext = Path(file_name).suffix.lower().lstrip('.')
    return ext in [t.lower() for t in allowed_types]


# Example usage
if __name__ == "__main__":
    st.set_page_config(page_title="File Uploader Demo")

    st.title("📄 File Uploader Component")

    # Initialize session state
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    # File uploader
    uploaded_file = file_uploader(
        label="Choose a file",
        allowed_types=["pdf", "txt"],
        max_size_mb=10
    )

    # Upload button
    if uploaded_file:
        if st.button("📤 Upload"):
            # Mock upload function
            def mock_upload(file):
                return True  # Simulate successful upload

            def on_success(filename):
                if filename not in st.session_state.uploaded_files:
                    st.session_state.uploaded_files.append(filename)

            upload_with_progress(uploaded_file, mock_upload, on_success)
            st.rerun()

    # Display uploaded files
    st.markdown("---")
    file_to_delete = render_uploaded_files_list(st.session_state.uploaded_files)

    if file_to_delete:
        st.session_state.uploaded_files.remove(file_to_delete)
        st.rerun()
