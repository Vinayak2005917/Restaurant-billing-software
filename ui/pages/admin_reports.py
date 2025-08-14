import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import utils.components as components
#add a clock
components.add_live_clock()



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

# Sidebar content (same as pages/new order.py)
with st.sidebar:
    st.markdown("### Navigation")

    if st.button("Admin Dashboard"):
        st.session_state.page = "home"
        st.switch_page("pages/admin.py")
    if st.button("Settings"):
        st.switch_page("pages/admin_setting.py")
    if st.button("Log Out"):
        st.session_state.page = "logout"
        st.switch_page("pages/new order.py")

st.markdown("---")

# Load and display sales report
try:
    import sqlite3
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    db_path = os.path.join(project_root, "db", "restaurant.db")
    conn = sqlite3.connect(db_path)
    sales_df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()
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
            
            # Most Sold Item Section
            st.markdown("---")
            st.markdown("## 🏆 Most Popular Item")
            
            # Calculate most sold item
            def get_most_sold_item(sales_df):
                item_counts = {}
                for _, row in sales_df.iterrows():
                    items_detail = row.get('Items_Detail', '')
                    if pd.notna(items_detail) and items_detail:
                        # Parse items like "Pizza x 2 = ₹299.00 | Coffee x 1 = ₹50.00"
                        items = items_detail.split(' | ')
                        for item in items:
                            try:
                                # Extract item name and quantity
                                if ' x ' in item and ' = ' in item:
                                    name_qty = item.split(' = ')[0]  # Get "Pizza x 2" part
                                    name, qty_str = name_qty.rsplit(' x ', 1)
                                    qty = int(qty_str.strip())
                                    name = name.strip()
                                    item_counts[name] = item_counts.get(name, 0) + qty
                            except:
                                continue
                return max(item_counts.items(), key=lambda x: x[1]) if item_counts else ("No items", 0)
            
            most_sold_item, most_sold_count = get_most_sold_item(sales_df)
            
            col_center = st.columns([1, 2, 1])[1]
            with col_center:
                st.metric("🥇 Most Sold Item", most_sold_item, f"Sold {most_sold_count} times")
            
                        # Period-based sales (Today, This Week, This Month)
            try:
                # Ensure Timestamp is datetime for filtering
                if 'Timestamp' in sales_df.columns:
                    sales_df['Timestamp'] = pd.to_datetime(sales_df['Timestamp'], errors='coerce')
                now = pd.Timestamp.now()
                ts = sales_df['Timestamp']
                valid_ts = ts.notna()

                # Today
                start_of_day = now.normalize()
                end_of_day = start_of_day + pd.Timedelta(days=1)
                mask_today = valid_ts & (ts >= start_of_day) & (ts < end_of_day)

                # This week (Mon-Sun)
                start_of_week = start_of_day - pd.Timedelta(days=start_of_day.weekday())
                end_of_week = start_of_week + pd.Timedelta(days=7)
                mask_week = valid_ts & (ts >= start_of_week) & (ts < end_of_week)

                # This month
                start_of_month = start_of_day.replace(day=1)
                next_month_start = start_of_month + pd.DateOffset(months=1)
                mask_month = valid_ts & (ts >= start_of_month) & (ts < next_month_start)

                today_revenue = float(sales_df.loc[mask_today, 'Total_Amount'].sum())
                week_revenue = float(sales_df.loc[mask_week, 'Total_Amount'].sum())
                month_revenue = float(sales_df.loc[mask_month, 'Total_Amount'].sum())

                today_orders = int(mask_today.sum())
                week_orders = int(mask_week.sum())
                month_orders = int(mask_month.sum())

                st.markdown("---")
                st.markdown("## 🗓️ Period Sales")
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.metric("Today Revenue", f"₹{today_revenue:.2f}")
                    st.caption(f"Orders: {today_orders}")
                with c2:
                    st.metric("This Week Revenue", f"₹{week_revenue:.2f}")
                    st.caption(f"Orders: {week_orders}")
                with c3:
                    st.metric("This Month Revenue", f"₹{month_revenue:.2f}")
                    st.caption(f"Orders: {month_orders}")
            except Exception as _:
                # Fail silently to not break the page if date parsing fails
                pass
            
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


            # --- Centered Metrics CSV Export ---
            metrics_data = {
                "Metric": ["Total Orders", "Total Revenue", "Average Order Value", "Total Items Sold",
                           "Most Sold Item", "Most Sold Item Count", "Today Revenue", "Today Orders",
                           "This Week Revenue", "This Week Orders", "This Month Revenue", "This Month Orders"],
                "Value": [
                    total_orders,
                    total_revenue,
                    avg_order_value,
                    total_items_sold,
                    most_sold_item,
                    most_sold_count,
                    today_revenue,
                    today_orders,
                    week_revenue,
                    week_orders,
                    month_revenue,
                    month_orders
                ]
            }

            metrics_df = pd.DataFrame(metrics_data)
            csv_data = metrics_df.to_csv(index=False).encode('utf-8')

            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("### ⬇️ Download Metrics Data (CSV)")
                st.download_button(
                    label="📥 Download Metrics CSV",
                    data=csv_data,
                    file_name="sales_metrics.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
    else:
        st.info("📄 No sales data found.")
        st.write("The sales report will be created automatically when you process your first order.")
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
