import streamlit as st
from components.layout import top_header
from pages import director, wellbeing, data_management, login

st.set_page_config(page_title="UniSystem  ", page_icon="🎓", layout="wide")

# Hide default Streamlit page navigation
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize authentication
login.init_session_state()

# If not authenticated, show login page
if not login.is_authenticated():
    login.render_login_form()
    st.stop()

# User is authenticated - show the dashboard
top_header()

# Get current user role
current_user = login.get_current_user()
user_role = current_user.get("role", "") if current_user else ""

# Define pages based on user role
ALL_PAGES = {
    "Director": director,
    "Wellbeing": wellbeing,
    "Data Management": data_management,
}

# Role-based access control
if user_role == "director":
    # Director can access Director and Data Management
    PAGES = {
        "Director": director
                }
elif user_role == "wellbeing" or user_role == "wellbeing_officer":
    # Wellbeing officer can only access Wellbeing dashboard
    PAGES = {
        "Wellbeing": wellbeing,
    }
elif user_role == "admin":
    # Admin can access everything
    PAGES = {
        "Data Management": data_management
    }
else:
    # Default: access to all pages (fallback)
    PAGES = ALL_PAGES

selected = st.sidebar.radio("Navigate", list(PAGES.keys()), index=0)
page = PAGES[selected]

# Show user info in sidebar
login.render_user_info()

# Each page exposes a `render()` function
page.render()
