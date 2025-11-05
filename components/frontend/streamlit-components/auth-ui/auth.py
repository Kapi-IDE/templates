"""Reusable Streamlit authentication UI component."""

import streamlit as st
from typing import Optional, Callable, Dict

def login_form(
    on_login: Callable[[str, str], Optional[str]],
    title: str = "🔐 Login",
    key_prefix: str = "login"
) -> None:
    """Render login form.

    Args:
        on_login: Callback function that accepts (email, password) and returns token or None
        title: Form title
        key_prefix: Prefix for widget keys
    """
    st.markdown(f"#### {title}")

    email = st.text_input(
        "Email",
        key=f"{key_prefix}_email",
        placeholder="user@example.com"
    )

    password = st.text_input(
        "Password",
        type="password",
        key=f"{key_prefix}_password"
    )

    if st.button("Login", key=f"{key_prefix}_btn", type="primary", use_container_width=True):
        if not email or not password:
            st.error("Please enter both email and password")
            return

        token = on_login(email, password)

        if token:
            st.session_state.access_token = token
            st.session_state.user_email = email
            st.success("✅ Logged in successfully!")
            st.rerun()
        else:
            st.error("❌ Login failed. Check your credentials.")


def logout_button(
    on_logout: Callable = None,
    key: str = "logout_btn"
) -> None:
    """Render logout button.

    Args:
        on_logout: Optional callback function to call on logout
        key: Widget key
    """
    if st.button("🚪 Logout", key=key, use_container_width=True):
        # Clear session
        if "access_token" in st.session_state:
            del st.session_state.access_token
        if "user_email" in st.session_state:
            del st.session_state.user_email

        if on_logout:
            on_logout()

        st.success("Logged out successfully")
        st.rerun()


def display_user_info(email: Optional[str] = None):
    """Display logged-in user information.

    Args:
        email: User email to display
    """
    if email:
        st.success(f"✅ Logged in as: {email}")
    elif "user_email" in st.session_state:
        st.success(f"✅ Logged in as: {st.session_state.user_email}")


def require_auth(redirect_message: str = "Please login to continue") -> bool:
    """Check if user is authenticated.

    Args:
        redirect_message: Message to show if not authenticated

    Returns:
        True if authenticated, False otherwise
    """
    if "access_token" not in st.session_state:
        st.warning(redirect_message)
        return False
    return True


def get_auth_headers() -> Dict[str, str]:
    """Get authorization headers for API requests.

    Returns:
        Dictionary with Authorization header
    """
    token = st.session_state.get("access_token")
    if not token:
        return {}

    return {"Authorization": f"Bearer {token}"}


def signup_form(
    on_signup: Callable[[str, str, str], bool],
    title: str = "📝 Sign Up",
    key_prefix: str = "signup"
) -> None:
    """Render signup form.

    Args:
        on_signup: Callback function that accepts (email, password, full_name) and returns success bool
        title: Form title
        key_prefix: Prefix for widget keys
    """
    st.markdown(f"#### {title}")

    email = st.text_input(
        "Email",
        key=f"{key_prefix}_email",
        placeholder="user@example.com"
    )

    full_name = st.text_input(
        "Full Name",
        key=f"{key_prefix}_name",
        placeholder="John Doe"
    )

    password = st.text_input(
        "Password",
        type="password",
        key=f"{key_prefix}_password",
        help="Minimum 8 characters"
    )

    password_confirm = st.text_input(
        "Confirm Password",
        type="password",
        key=f"{key_prefix}_password_confirm"
    )

    if st.button("Sign Up", key=f"{key_prefix}_btn", type="primary", use_container_width=True):
        # Validation
        if not email or not password or not full_name:
            st.error("Please fill in all fields")
            return

        if len(password) < 8:
            st.error("Password must be at least 8 characters")
            return

        if password != password_confirm:
            st.error("Passwords don't match")
            return

        # Call signup callback
        success = on_signup(email, password, full_name)

        if success:
            st.success("✅ Account created! Please login.")
            st.balloons()
        else:
            st.error("❌ Signup failed. Email may already be registered.")


# Example usage
if __name__ == "__main__":
    st.set_page_config(page_title="Auth Component Demo")

    st.title("🔐 Authentication Component")

    # Mock login function
    def mock_login(email: str, password: str) -> Optional[str]:
        if email == "demo@example.com" and password == "password":
            return "mock_token_12345"
        return None

    # Mock signup function
    def mock_signup(email: str, password: str, full_name: str) -> bool:
        return True  # Always succeed for demo

    # Check auth state
    if not st.session_state.get("access_token"):
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            login_form(on_login=mock_login)
            st.info("Demo credentials: demo@example.com / password")

        with tab2:
            signup_form(on_signup=mock_signup)
    else:
        display_user_info()
        st.markdown("---")
        st.success("You are authenticated!")
        st.markdown(f"**Token:** {st.session_state.access_token[:20]}...")
        st.markdown("---")
        logout_button()
