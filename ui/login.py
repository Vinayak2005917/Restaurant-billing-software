import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import utils.components as components
#add a clock
components.add_live_clock()


st.set_page_config(page_title="Restaurant Billing Software - Login", layout="centered")

# Hide the hamburger menu and default sidebar page list
hide_default_page_menu = """
    <style>
    /* Hide the hamburger menu */
    #MainMenu {visibility: hidden;}
    /* Hide default sidebar navigation */
    [data-testid="stSidebarNav"] {display: none;}
    /* Hide sidebar completely for login page */
    [data-testid="stSidebar"] {display: none;}
    </style>
"""
st.markdown(hide_default_page_menu, unsafe_allow_html=True)

# Custom CSS for login page styling
st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        background-color: #f8f9fa;
        margin-top: 5rem;
    }
    .login-title {
        text-align: center;
        color: #333;
        margin-bottom: 2rem;
        font-size: 2rem;
        font-weight: bold;
    }
    .stButton > button {
        width: 100% !important;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 0.5rem;
        font-size: 1.1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
        padding: 0.5rem;
        border-radius: 5px;
        border: 1px solid #ddd;
    }
    </style>
""", unsafe_allow_html=True)

# Center the login form
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    
    # Restaurant logo/title
    st.markdown('<h1 class="login-title">🍽️ Restaurant Billing</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 2rem;">Please login to continue</p>', unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="Enter your password", type="password")
        
        # Login button
        login_button = st.form_submit_button("🔐 Login")
        
        if login_button:
            if not username or not password:
                st.error("Please enter both username and password")
            else:
                # Admin shortcut
                if username == "admin" and password == "admin":
                    st.success("Admin login successful! Redirecting to admin panel...")
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = "admin"
                    st.switch_page("pages/admin.py")
                else:
                    # Validate against SQLite database (restaurant.db)
                    import sqlite3
                    try:
                        current_dir = os.path.dirname(os.path.abspath(__file__))
                        project_root = os.path.dirname(current_dir)
                        db_path = os.path.join(project_root, "db", "restaurant.db")
                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()
                        # Try common table names
                        for table in ["cashiers", "users"]:
                            try:
                                cursor.execute(f"SELECT username, full_name, password FROM {table} WHERE username=?", (username,))
                                row = cursor.fetchone()
                                if row:
                                    db_username, db_full_name, db_password = row
                                    if str(db_password) == str(password):
                                        st.success("Login successful! Redirecting to new order...")
                                        st.session_state.logged_in = True
                                        st.session_state.username = str(db_username)
                                        st.session_state.full_name = str(db_full_name)
                                        st.session_state.user_role = "cashier"
                                        st.switch_page("pages/new order.py")
                                        conn.close()
                                        break
                                    else:
                                        st.error("Invalid username or password.")
                                        conn.close()
                                        break
                            except Exception:
                                continue
                        else:
                            st.error("No user records found in database. Please contact admin.")
                            conn.close()
                    except Exception as e:
                        st.error(f"Login failed: {e}")
    
    # Direct access buttons
    st.markdown("---")
    st.markdown('<p style="text-align: center; color: #666; margin-bottom: 1rem;">Dev Tool : Quick Access (No Login Required)</p>', unsafe_allow_html=True)
    
    col_admin, col_cashier = st.columns(2)
    
    with col_admin:
        if st.button("🔧 Admin Panel", use_container_width=True):
            # Set admin session without login
            st.session_state.logged_in = True
            st.session_state.username = "admin"
            st.session_state.user_role = "admin"
            st.switch_page("pages/admin.py")
    
    with col_cashier:
        if st.button("📋 New Order", use_container_width=True):
            # Set cashier session without login
            st.session_state.logged_in = True
            st.session_state.username = "cashier"
            st.session_state.user_role = "cashier"
            st.switch_page("pages/new order.py")
    
    st.markdown('</div>', unsafe_allow_html=True)
