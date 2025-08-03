import streamlit as st

st.markdown("<h1 style='text-align: center;'>Dine In</h1>", unsafe_allow_html=True)

# Hide the hamburger menu and default sidebar page list only
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

#input feild for table number
table_number = st.text_input("Enter Table Number", placeholder="e.g. 5")
#after enter, show the menu
if table_number:
    st.markdown(f"<h2 style='text-align: center;'>Table {table_number} Menu</h2>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### 👨‍💼 Staff Info")
    st.write("**Name:** Vinayak Mishra")
    st.write("**Role:** Cashier")
    st.markdown("---")
    st.markdown("### Navigation")

    if st.button("New Order"):
        st.switch_page("./main_ui.py")
    if st.button("Order History"):
        st.session_state.page = "history"
    if st.button("Reports"):
        st.session_state.page = "reports"
    if st.button("Log Out"):
        st.session_state.page = "logout"
