import streamlit as st
import time

if 'page' not in st.session_state:
    st.session_state.page = 'home'

st.set_page_config(page_title="Restaurant Billing Software", layout="wide")

# Hide the default Streamlit page menu (sidebar page list)
hide_default_page_menu = """
    <style>
    /* Hide the hamburger menu */
    #MainMenu {visibility: hidden;}
    /* Hide default sidebar navigation */
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
remove_sidebar_padding = """
    <style>
    /* Remove padding/margin from sidebar main container */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }

    /* Remove padding/margin from sidebar content container */
    [data-testid="stSidebar"] > div:first-child > div {
        padding-top: 0 !important;
        margin-top: 0 !important;
    }
    </style>
"""
st.markdown(remove_sidebar_padding, unsafe_allow_html=True)
st.markdown(hide_default_page_menu, unsafe_allow_html=True)

# Sidebar content (only cashier info and custom nav)
with st.sidebar:
    st.markdown("### 👨‍💼 Staff Info")
    st.write("**Name:** Vinayak Mishra")
    st.write("**Role:** Cashier")
    st.markdown("---")

    if st.button("Reports"):
        st.session_state.page = "reports"
    if st.button("Log Out"):
        st.session_state.page = "logout"
    if st.button("Settings"):
        st.session_state.page = "settings"

# Main UI: Dine In and Take Away buttons only here
st.title("🍽️ Add a New order!!")
st.markdown("### Please select an option:")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Dine In", use_container_width=True):
        st.switch_page("pages/dine_in.py")   # Note: no ".py" and no "pages/"
    if st.button("Take Away", use_container_width=True):
        st.switch_page("pages/take_away.py")

# Simple page render on sidebar nav buttons
page = st.session_state.get("page", "home")



if page == "reports":
    st.switch_page("pages/reports.py")
    # Your Reports UI here
elif page == "settings":
    st.subheader("⚙️ Settings")
    # Your Settings UI here
elif page == "logout":
    st.subheader("🚪 Logged Out")
    st.write("You have been logged out. Close the app or log in again.")
