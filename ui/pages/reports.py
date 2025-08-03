import streamlit as st
import pandas as pd
import os


st.set_page_config(page_title="Restaurant Billing Software", layout="wide")
st.markdown("<h1 style='text-align: center;'>📊 Sales Reports</h1>", unsafe_allow_html=True)

# Hide the hamburger menu and default sidebar page list
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

# Sidebar content (same as main_ui.py)
with st.sidebar:
    st.markdown("### 👨‍💼 Staff Info")
    st.write("**Name:** Vinayak Mishra")
    st.write("**Role:** Cashier")
    st.markdown("---")
    st.markdown("### Navigation")

    if st.button("New Order"):
        st.session_state.page = "home"
        st.switch_page("main_ui.py")
    if st.button("Order History"):
        st.session_state.page = "history"
        st.switch_page("main_ui.py")
    if st.button("Log Out"):
        st.session_state.page = "logout"
        st.switch_page("main_ui.py")

st.markdown("---")

# Load and display sales report
try:
    # Get path to sales report
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    sales_report_path = os.path.join(project_root, "data", "sales_report.csv")
    
    if os.path.exists(sales_report_path) and os.path.getsize(sales_report_path) > 0:
        # Read the CSV file
        sales_df = pd.read_csv(sales_report_path)
        
        if not sales_df.empty:
            # Display summary statistics
            st.markdown("## 📈 Sales Summary")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                total_orders = len(sales_df)
                st.metric("Total Orders", total_orders)
            
            with col2:
                total_revenue = sales_df['Total_Amount'].sum()
                st.metric("Total Revenue", f"₹{total_revenue:.2f}")
            
            with col3:
                avg_order_value = sales_df['Total_Amount'].mean()
                st.metric("Average Order Value", f"₹{avg_order_value:.2f}")
            
            with col4:
                total_items_sold = sales_df['Total_Items'].sum()
                st.metric("Total Items Sold", int(total_items_sold))
            
            st.markdown("---")
            
            # Display the full data table
            st.markdown("## 📋 All Orders")
            
            # Format the dataframe for better display
            display_df = sales_df.copy()
            display_df['Total_Amount'] = display_df['Total_Amount'].apply(lambda x: f"₹{x:.2f}")
            
            # Display with search and sorting
            st.dataframe(
                display_df, 
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Order_Number": "Order #",
                    "Order_Type": "Type",
                    "Table_Number": "Table",
                    "Total_Amount": "Amount",
                    "Total_Items": "Items",
                    "Items_Detail": "Order Details",
                    "Timestamp": "Date & Time"
                }
            )
            
            # Additional analytics
            st.markdown("---")
            st.markdown("## 📊 Analytics")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Order type distribution
                st.markdown("### Order Type Distribution")
                order_type_counts = sales_df['Order_Type'].value_counts()
                st.bar_chart(order_type_counts)
            
            with col2:
                # Revenue by order type
                st.markdown("### Revenue by Order Type")
                revenue_by_type = sales_df.groupby('Order_Type')['Total_Amount'].sum()
                st.bar_chart(revenue_by_type)
            
        else:
            st.info("📄 Sales report file exists but contains no data yet.")
            st.write("Start taking orders to see sales data here!")
    
    else:
        st.info("📄 No sales data found.")
        st.write("The sales report will be created automatically when you process your first order.")
        
        # Show sample format
        st.markdown("### Expected Data Format:")
        sample_data = {
            'Order_Number': ['ORD12345', 'ORD12346'],
            'Order_Type': ['Dine-in', 'Take-away'],
            'Table_Number': ['5', '0'],
            'Total_Amount': ['₹349.00', '₹150.00'],
            'Total_Items': [3, 1],
            'Items_Detail': ['Pizza x 2 = ₹299.00 | Coffee x 1 = ₹50.00', 'Burger x 1 = ₹150.00'],
            'Timestamp': ['2025-08-03 14:30:15', '2025-08-03 15:45:30']
        }
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"❌ Error loading sales report: {str(e)}")
    st.write("Please check if the data folder exists and is accessible.")
