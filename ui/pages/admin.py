import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import utils.components as components
#add a clock
components.add_live_clock()


st.set_page_config(page_title="Restaurant Billing Software - Admin", layout="wide")
st.markdown("<h1 style='text-align: center;'>Admin Panel</h1>", unsafe_allow_html=True)

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

# Check if user is logged in and is admin
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.error("Please login to access this page")
    st.switch_page("login.py")
elif st.session_state.get('user_role') != 'admin':
    st.error("Access denied. Admin privileges required.")
    st.switch_page("login.py")

# Sidebar Navigation
with st.sidebar:
    st.markdown(f"<h2 style='text-align: center;'>🔧 Admin Menu</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center;'>Welcome, {st.session_state.get('username', 'Admin')}</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Navigation buttons
    if st.button("📊 Reports", use_container_width=True):
        st.switch_page("pages/admin_reports.py")
    
    if st.button("⚙️ Settings", use_container_width=True):
        st.switch_page("pages/admin_setting.py")
    
    st.markdown("---")
    
    # Logout button
    if st.button("🚪 Logout", use_container_width=True):
        # Clear session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("login.py")

# Main Admin Content
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("### 📁 File Upload")
    st.markdown("Upload files to manage your restaurant data")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose a file to upload",
        type=['csv', 'xlsx', 'txt', 'json'],
        help="Supported formats: CSV, Excel, Text, JSON"
    )
    
    if uploaded_file is not None:
        # Display file details
        st.success(f"File uploaded: {uploaded_file.name}")
        st.info(f"File size: {uploaded_file.size} bytes")
        st.info(f"File type: {uploaded_file.type}")
        
        # Preview file content based on type
        if uploaded_file.type == "text/csv":
            try:
                df = pd.read_csv(uploaded_file)
                st.markdown("#### File Preview (First 5 rows):")
                st.dataframe(df.head())
                
                # Option to save the file
                if st.button("💾 Save to Data Folder"):
                    # Get project root directory
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.dirname(os.path.dirname(current_dir))
                    data_folder = os.path.join(project_root, "data")
                    
                    # Create data folder if it doesn't exist
                    os.makedirs(data_folder, exist_ok=True)
                    
                    # Save file
                    file_path = os.path.join(data_folder, uploaded_file.name)
                    df.to_csv(file_path, index=False)
                    st.success(f"File saved to: {file_path}")
                    
            except Exception as e:
                st.error(f"Error reading CSV file: {str(e)}")
        
        elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/vnd.ms-excel"]:
            try:
                df = pd.read_excel(uploaded_file)
                st.markdown("#### File Preview (First 5 rows):")
                st.dataframe(df.head())
                
                # Option to save the file
                if st.button("💾 Save to Data Folder"):
                    # Get project root directory
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.dirname(os.path.dirname(current_dir))
                    data_folder = os.path.join(project_root, "data")
                    
                    # Create data folder if it doesn't exist
                    os.makedirs(data_folder, exist_ok=True)
                    
                    # Save as CSV
                    file_path = os.path.join(data_folder, uploaded_file.name.replace('.xlsx', '.csv').replace('.xls', '.csv'))
                    df.to_csv(file_path, index=False)
                    st.success(f"File converted and saved to: {file_path}")
                    
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
        
        else:
            st.markdown("#### File Content:")
            try:
                # For text files, show content
                content = uploaded_file.read().decode('utf-8')
                st.text_area("File Content", content, height=200)
                
                # Option to save the file
                if st.button("💾 Save to Data Folder"):
                    # Get project root directory
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.dirname(os.path.dirname(current_dir))
                    data_folder = os.path.join(project_root, "data")
                    
                    # Create data folder if it doesn't exist
                    os.makedirs(data_folder, exist_ok=True)
                    
                    # Save file
                    file_path = os.path.join(data_folder, uploaded_file.name)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    st.success(f"File saved to: {file_path}")
                    
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")

# Admin Dashboard Stats
st.markdown("---")
st.markdown("### 📈 Quick Stats")

# Fetch stats from the database
import sqlite3
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
db_path = os.path.join(project_root, "db", "restaurant.db")
conn = sqlite3.connect(db_path)

# Total Orders Today & Revenue Today
try:
    sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
    sales_df['Timestamp'] = pd.to_datetime(sales_df['Timestamp'], errors='coerce')
    today = pd.Timestamp.now().normalize()
    tomorrow = today + pd.Timedelta(days=1)
    mask_today = (sales_df['Timestamp'] >= today) & (sales_df['Timestamp'] < tomorrow)
    total_orders_today = mask_today.sum()
    revenue_today = float(sales_df.loc[mask_today, 'Total_Amount'].sum())
except Exception:
    total_orders_today = 0
    revenue_today = 0.0

# Active Tables (unique Table_Number for today, only for Dine-in)
try:
    active_tables = sales_df.loc[mask_today & (sales_df['Order_Type'] == 'Dine-in'), 'Table_Number'].nunique()
except Exception:
    active_tables = 0

# Menu Items
try:
    menu_df = pd.read_sql_query("SELECT * FROM menu", conn)
    menu_items_count = len(menu_df)
except Exception:
    menu_items_count = 0

conn.close()

# Create columns for stats
stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Total Orders Today", total_orders_today)

with stat_col2:
    st.metric("Revenue Today", f"₹{revenue_today:.2f}")

with stat_col3:
    st.metric("Active Tables", active_tables)

with stat_col4:
    st.metric("Menu Items", menu_items_count)
