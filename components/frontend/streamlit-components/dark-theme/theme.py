"""Reusable dark theme for Streamlit applications."""

import streamlit as st

# Color palettes
ONYX_DARK = {
    "bg_primary": "#1a1a1a",
    "bg_secondary": "#2d2d2d",
    "bg_tertiary": "#3a3a3a",
    "text_primary": "#e5e5e5",
    "text_secondary": "#a0a0a0",
    "accent_blue": "#3b82f6",
    "accent_green": "#10b981",
    "accent_red": "#ef4444",
    "accent_yellow": "#f59e0b",
    "border_color": "#404040",
    "sidebar_bg": "#0f0f0f",
    "code_bg": "#1e1e1e",
}

NORD_DARK = {
    "bg_primary": "#2e3440",
    "bg_secondary": "#3b4252",
    "bg_tertiary": "#434c5e",
    "text_primary": "#eceff4",
    "text_secondary": "#d8dee9",
    "accent_blue": "#5e81ac",
    "accent_green": "#a3be8c",
    "accent_red": "#bf616a",
    "accent_yellow": "#ebcb8b",
    "border_color": "#4c566a",
    "sidebar_bg": "#2e3440",
    "code_bg": "#3b4252",
}

DRACULA = {
    "bg_primary": "#282a36",
    "bg_secondary": "#44475a",
    "bg_tertiary": "#6272a4",
    "text_primary": "#f8f8f2",
    "text_secondary": "#e5e5e5",
    "accent_blue": "#8be9fd",
    "accent_green": "#50fa7b",
    "accent_red": "#ff5555",
    "accent_yellow": "#f1fa8c",
    "border_color": "#44475a",
    "sidebar_bg": "#21222c",
    "code_bg": "#282a36",
}


def apply_dark_theme(theme: str = "onyx"):
    """Apply dark theme CSS to Streamlit app.

    Args:
        theme: Theme name ('onyx', 'nord', 'dracula')
    """
    # Select color palette
    if theme == "nord":
        colors = NORD_DARK
    elif theme == "dracula":
        colors = DRACULA
    else:
        colors = ONYX_DARK

    css = f"""
    <style>
        /* CSS Variables */
        :root {{
            --bg-primary: {colors['bg_primary']};
            --bg-secondary: {colors['bg_secondary']};
            --bg-tertiary: {colors['bg_tertiary']};
            --text-primary: {colors['text_primary']};
            --text-secondary: {colors['text_secondary']};
            --accent-blue: {colors['accent_blue']};
            --accent-green: {colors['accent_green']};
            --accent-red: {colors['accent_red']};
            --accent-yellow: {colors['accent_yellow']};
            --border-color: {colors['border_color']};
            --sidebar-bg: {colors['sidebar_bg']};
            --code-bg: {colors['code_bg']};
        }}

        /* Global background */
        .stApp {{
            background-color: var(--bg-primary);
            color: var(--text-primary);
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: var(--sidebar-bg);
            border-right: 1px solid var(--border-color);
        }}

        [data-testid="stSidebar"] .stMarkdown {{
            color: var(--text-primary);
        }}

        /* Chat messages */
        .stChatMessage {{
            background-color: var(--bg-secondary);
            border-radius: 8px;
            padding: 12px;
            margin: 8px 0;
            border: 1px solid var(--border-color);
        }}

        [data-testid="stChatMessageContent"] {{
            background-color: transparent;
        }}

        /* Code blocks */
        .stCodeBlock {{
            background-color: var(--code-bg) !important;
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}

        code {{
            background-color: var(--code-bg);
            color: var(--text-primary);
            padding: 2px 6px;
            border-radius: 4px;
        }}

        /* Input boxes */
        .stTextInput > div > div > input {{
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
        }}

        .stTextArea > div > div > textarea {{
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: var(--accent-blue);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: 500;
            transition: background-color 0.2s;
        }}

        .stButton > button:hover {{
            background-color: #2563eb;
            border: none;
        }}

        /* File uploader */
        [data-testid="stFileUploader"] {{
            background-color: var(--bg-secondary);
            border: 1px dashed var(--border-color);
            border-radius: 8px;
            padding: 16px;
        }}

        /* Success/error/warning/info messages */
        .stSuccess {{
            background-color: rgba(16, 185, 129, 0.1);
            border: 1px solid var(--accent-green);
            color: var(--accent-green);
            border-radius: 6px;
        }}

        .stError {{
            background-color: rgba(239, 68, 68, 0.1);
            border: 1px solid var(--accent-red);
            color: var(--accent-red);
            border-radius: 6px;
        }}

        .stWarning {{
            background-color: rgba(245, 158, 11, 0.1);
            border: 1px solid var(--accent-yellow);
            color: var(--accent-yellow);
            border-radius: 6px;
        }}

        .stInfo {{
            background-color: rgba(59, 130, 246, 0.1);
            border: 1px solid var(--accent-blue);
            color: var(--accent-blue);
            border-radius: 6px;
        }}

        /* Expander */
        .streamlit-expanderHeader {{
            background-color: var(--bg-secondary);
            border-radius: 6px;
            border: 1px solid var(--border-color);
        }}

        /* Divider */
        hr {{
            border-color: var(--border-color);
        }}

        /* Headers */
        h1, h2, h3, h4, h5, h6 {{
            color: var(--text-primary);
        }}

        /* Links */
        a {{
            color: var(--accent-blue);
        }}

        a:hover {{
            color: #60a5fa;
        }}

        /* Selectbox */
        .stSelectbox > div > div {{
            background-color: var(--bg-secondary);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }}

        /* Slider */
        .stSlider > div > div > div {{
            background-color: var(--accent-blue);
        }}

        /* Checkbox */
        .stCheckbox > label {{
            color: var(--text-primary);
        }}

        /* Radio */
        .stRadio > label {{
            color: var(--text-primary);
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: var(--bg-secondary);
            border-radius: 6px;
        }}

        .stTabs [data-baseweb="tab"] {{
            color: var(--text-secondary);
        }}

        .stTabs [aria-selected="true"] {{
            background-color: var(--bg-tertiary);
            color: var(--text-primary);
        }}

        /* Metric */
        [data-testid="stMetricValue"] {{
            color: var(--text-primary);
        }}

        /* DataFrame */
        .dataframe {{
            background-color: var(--bg-secondary);
            color: var(--text-primary);
        }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)


def get_theme_colors(theme: str = "onyx") -> dict:
    """Get theme color palette.

    Args:
        theme: Theme name ('onyx', 'nord', 'dracula')

    Returns:
        Dictionary of color values
    """
    if theme == "nord":
        return NORD_DARK
    elif theme == "dracula":
        return DRACULA
    else:
        return ONYX_DARK


# Example usage
if __name__ == "__main__":
    st.set_page_config(page_title="Dark Theme Demo", layout="wide")

    # Theme selector
    theme = st.sidebar.selectbox(
        "Choose Theme",
        ["onyx", "nord", "dracula"],
        index=0
    )

    # Apply theme
    apply_dark_theme(theme)

    st.title("🎨 Dark Theme Component")
    st.markdown("This demonstrates the dark theme styling across various Streamlit components.")

    # Demo components
    st.header("Text Inputs")
    st.text_input("Text Input", placeholder="Type here...")
    st.text_area("Text Area", placeholder="Type more here...")

    st.header("Buttons & Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Primary Button")
    with col2:
        st.download_button("Download", data="test", file_name="test.txt")
    with col3:
        st.file_uploader("Upload File")

    st.header("Messages")
    st.success("Success message")
    st.error("Error message")
    st.warning("Warning message")
    st.info("Info message")

    st.header("Code Block")
    st.code("""
def hello_world():
    print("Hello, World!")
    return True
    """, language="python")

    st.header("Chat Messages")
    with st.chat_message("user"):
        st.markdown("This is a user message")
    with st.chat_message("assistant"):
        st.markdown("This is an assistant response with **markdown** and `code`")

    st.header("Other Components")
    st.slider("Slider", 0, 100, 50)
    st.checkbox("Checkbox option")
    st.selectbox("Select option", ["Option 1", "Option 2", "Option 3"])

    with st.expander("Expandable section"):
        st.markdown("Hidden content goes here")
