import streamlit as st
import requests
import hashlib
from typing import Optional, Dict

# Backend login endpoint
LOGIN_URL = "http://127.0.0.1:8000/login"


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def authenticate(username: str, password: str) -> Optional[Dict]:
    """
    Authenticate user credentials against the backend API.
    
    Args:
        username: The username to authenticate
        password: The password to verify (will be hashed before sending)
        
    Returns:
        User dictionary if authentication successful, None otherwise
    """
    try:
        # Hash the password before sending to backend
        hashed_password = hash_password(password)
        
        # Send login request to backend
        payload = {
            "username": username,
            "password": hashed_password
        }
        
        response = requests.post(LOGIN_URL, json=payload, timeout=5)
        data = response.json()
        
        # Check if login was successful
        if data.get("success"):
            user_data = data.get("user", {})
            role = data.get("role", user_data.get("role", "user"))
            
            # Map role to display name
            role_names = {
                "admin": "System Administrator",
                "director": "Course Director",
                "wellbeing_officer": "Wellbeing Officer"
            }
            
            return {
                "username": username,
                "role": role,
                "name": role_names.get(role, role.replace("_", " ").title()),
                "user_data": user_data
            }
        else:
            # Login failed
            print(f"[Login] Failed: {data.get('message', 'Unknown error')}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[Login] Connection error: {e}")
        st.error("Unable to connect to authentication server. Please check if the backend is running.")
        return None
    except Exception as e:
        print(f"[Login] Error: {e}")
        return None


def init_session_state():
    """Initialize session state variables for authentication."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "login_attempts" not in st.session_state:
        st.session_state.login_attempts = 0


def logout():
    """Clear session state and log out the user."""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.login_attempts = 0
    st.rerun()


def render_login_form():
    """Render the login form UI."""
    st.markdown("""
        <style>
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 2rem;
        }
        .login-title {
            text-align: center;
            color: #1f77b4;
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }
        .login-subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown('<h1 class="login-title">🎓 UniSystem</h1>', unsafe_allow_html=True)
        st.markdown('<p class="login-subtitle">Dashboard Login</p>', unsafe_allow_html=True)
        
        # Check for too many failed attempts
        if st.session_state.login_attempts >= 5:
            st.error("⚠️ Too many failed login attempts. Please contact support.")
            if st.button("Reset Login Attempts"):
                st.session_state.login_attempts = 0
                st.rerun()
            return
        
        # Login form
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_a, col_b = st.columns(2)
            with col_a:
                submit = st.form_submit_button("🔐 Login", use_container_width=True)
            with col_b:
                demo_creds = st.form_submit_button("ℹ️ Demo Credentials", use_container_width=True)
            
            if submit:
                if not username or not password:
                    st.warning("⚠️ Please enter both username and password.")
                else:
                    user = authenticate(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        st.session_state.login_attempts = 0
                        st.success(f"✅ Welcome, {user['name']}!")
                        st.rerun()
                    else:
                        st.session_state.login_attempts += 1
                        remaining = 5 - st.session_state.login_attempts
                        st.error(f"❌ Invalid username or password. {remaining} attempts remaining.")
            
            if demo_creds:
                st.info("""
                **Login Information:**
                
                Enter your username and password provided by your administrator.
                
                Contact support if you need assistance accessing your account.
                """)
        
        st.markdown('</div>', unsafe_allow_html=True)


def render_user_info():
    """Render logged-in user information in the sidebar."""
    if st.session_state.authenticated and st.session_state.user:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 👤 Logged In")
            st.write(f"**Name:** {st.session_state.user['name']}")
            st.write(f"**Role:** {st.session_state.user['role'].replace('_', ' ').title()}")
            st.write(f"**Username:** {st.session_state.user['username']}")
            
            if st.button("🚪 Logout", use_container_width=True):
                logout()


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)


def get_current_user() -> Optional[Dict]:
    """Get current logged-in user."""
    return st.session_state.get("user")


def require_auth():
    """
    Decorator-like function to require authentication.
    Call this at the start of protected pages.
    """
    init_session_state()
    
    if not is_authenticated():
        render_login_form()
        st.stop()
    else:
        render_user_info()


def render():
    """Render the login page (standalone)."""
    init_session_state()
    
    if is_authenticated():
        st.success(f"✅ You are logged in as {st.session_state.user['name']}")
        st.info("Please navigate to other pages using the sidebar.")
        render_user_info()
    else:
        render_login_form()
