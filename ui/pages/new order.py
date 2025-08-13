import streamlit as st
import time

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import utils.components as components
#add a clock
components.add_live_clock()


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

# Sidebar content
with st.sidebar:
    st.markdown("### 👨‍💼 Staff Info")
    st.write("**Name:** Vinayak Mishra")
    st.write("**Role:** Cashier")
    st.markdown("---")

    if st.button("Reports"):
        st.session_state.page = "reports"
        st.switch_page("pages/reports.py")
    if st.button("Log Out"):
        st.session_state.page = "logout"
        st.switch_page("login.py")
    if st.button("Settings"):
        st.switch_page("pages/user_settings.py")

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
elif page == "settings":
    st.switch_page("pages/user_settings.py")
elif page == "logout":
    # Clear session state and redirect to login
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.switch_page("login.py")


