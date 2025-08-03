import streamlit as st
import pandas as pd
import os
import random
import datetime

st.set_page_config(page_title="Restaurant Billing Software", layout="wide")
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

with st.sidebar:
    st.markdown(f"<h1 style='text-align: center;'>🛒 Cart </h1>", unsafe_allow_html=True)

    # Display cart items
    if 'cart' in st.session_state and st.session_state.cart:
        cart_has_items = False
        total_items = 0
        total_price = 0
        
        for item_key, item_data in st.session_state.cart.items():
            if item_data['quantity'] > 0:
                cart_has_items = True
                st.write(f"**{item_data['name']}** X {item_data['quantity']}")
                total_items += item_data['quantity']
                total_price += item_data['quantity'] * item_data['price']
        
        if cart_has_items:
            st.markdown("---")
            st.write(f"**Total Items:** {total_items}")
            st.write(f"**Total Price:** ₹{total_price:.2f}")
            
            # Checkout button with functionality
            if st.button("🛒 Checkout", type="primary", use_container_width=True):
                # Generate random order number
                order_number = f"ORD{random.randint(10000, 99999)}"
                
                # Get current timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Prepare order data
                order_data = {
                    'order_number': order_number,
                    'order_type': 'Dine-in',
                    'table_number': table_number,
                    'total_amount': total_price,
                    'total_items': total_items,
                    'timestamp': timestamp,
                    'items_detail': []
                }
                
                # Add item details
                for item_key, item_data in st.session_state.cart.items():
                    if item_data['quantity'] > 0:
                        item_detail = f"{item_data['name']} x {item_data['quantity']} = ₹{item_data['quantity'] * item_data['price']:.2f}"
                        order_data['items_detail'].append(item_detail)
                
                # Convert items list to string for CSV storage
                items_string = " | ".join(order_data['items_detail'])
                
                # Prepare data for CSV
                csv_data = {
                    'Order_Number': [order_number],
                    'Order_Type': ['Dine-in'],
                    'Table_Number': [table_number],
                    'Total_Amount': [total_price],
                    'Total_Items': [total_items],
                    'Items_Detail': [items_string],
                    'Timestamp': [timestamp]
                }
                
                # Create DataFrame
                new_order_df = pd.DataFrame(csv_data)
                
                # Save to CSV
                try:
                    # Get path to data folder
                    current_dir = os.path.dirname(os.path.abspath(__file__))
                    project_root = os.path.dirname(os.path.dirname(current_dir))
                    sales_report_path = os.path.join(project_root, "data", "sales_report.csv")
                    
                    # Check if file exists and has content
                    if os.path.exists(sales_report_path) and os.path.getsize(sales_report_path) > 0:
                        try:
                            # Try to read existing file
                            existing_df = pd.read_csv(sales_report_path)
                            updated_df = pd.concat([existing_df, new_order_df], ignore_index=True)
                            updated_df.to_csv(sales_report_path, index=False)
                        except pd.errors.EmptyDataError:
                            # File exists but is empty, create with headers
                            new_order_df.to_csv(sales_report_path, index=False)
                    else:
                        # File doesn't exist or is empty, create new file with headers
                        new_order_df.to_csv(sales_report_path, index=False)
                    
                    # Show success message with order details
                    st.success(f"✅ Order {order_number} placed successfully!")
                    st.info(f"📋 **Order Summary:**\n\n"
                           f"🏷️ Order Number: {order_number}\n\n"
                           f"🍽️ Table: {table_number}\n\n"
                           f"💰 Total: ₹{total_price:.2f}\n\n"
                           f"📦 Items: {total_items}\n\n"
                           f"🕒 Time: {timestamp}")
                    
                    # Clear the cart after successful order
                    st.session_state.cart = {}
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error saving order: {str(e)}")
        else:
            st.write("Cart is empty")
    else:
        st.write("Cart is empty")


# Only show Clear Cart button if there are items in the cart
if 'cart' in st.session_state and st.session_state.cart:
    # Check if there's at least one item with quantity > 0
    has_items = any(item['quantity'] > 0 for item in st.session_state.cart.values())
    if has_items:
        if st.sidebar.button("🧹 Clear Cart"):
            # Clear the cart only
            st.session_state.cart = {}
            st.rerun()  # Refresh to show updated cart

if st.sidebar.button("Trash current order"):
    # Clear the cart
    if 'cart' in st.session_state:
        st.session_state.cart = {}
    st.switch_page("./main_ui.py")

if table_number:
    st.markdown(f"<h2 style='text-align: center;'>Menu</h2>", unsafe_allow_html=True)
    
    # Search option
    search_query = st.text_input("🔍 Search menu items...", placeholder="Search by name or description")
    
    # Menu
    try:
        # Acessing the Menu file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        menu_path = os.path.join(project_root, "data", "menu.csv")
        
        menu_df = pd.read_csv(menu_path)

        # Initialize session state for cart
        if 'cart' not in st.session_state:
            st.session_state.cart = {}

        # Display the menu
        # Add CSS styling once at the beginning
        st.markdown("""
            <style>
            .menu-item {
                border: none;
                border-radius: 0px;
                padding: 10px 0;
                margin: 10px 0;
                background-color: transparent;
            }
            </style>
        """, unsafe_allow_html=True)
        
        for index, item in menu_df.iterrows():
            # Filter items based on search query
            if search_query:
                item_name = item.get('item_name', '').lower()
                description = item.get('short_description', '').lower()
                if search_query.lower() not in item_name and search_query.lower() not in description:
                    continue  # Skip this item if it doesn't match search
            
            # Create the styled container for each menu item
            st.markdown('<div class="menu-item">', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 3, 2])
            
            with col1:
                # Image placeholder (you can replace with actual image path)
                if 'image' in item and pd.notna(item['image']):
                    st.image(item['image'], width=100)
                else:
                    st.markdown("<div style='text-align: center; font-size: 60px;'>🍽️</div>", unsafe_allow_html=True)
            
            with col2:
                # Item name and description
                item_name = item.get('item_name', f'Item {index+1}')
                st.markdown(f"**{item_name}**")
                
                if 'short_description' in item and pd.notna(item['short_description']):
                    st.markdown(f"<small>{item['short_description']}</small>", unsafe_allow_html=True)
                
                # Since there's no price column, show stock instead
                if 'stock' in item and pd.notna(item['stock']):
                    st.markdown(f"**Stock: {item['stock']} available**")
                
                # Use actual price if available, otherwise default
                item_price = item.get('price', 100)  # Default price for demo
                st.markdown(f"**Price: ₹{item_price}**")
            
            with col3:
                # Quantity controls
                item_key = f"item_{index}_{item_name}"
                
                # Initialize quantity for this item
                if item_key not in st.session_state.cart:
                    st.session_state.cart[item_key] = {
                        'quantity': 0,
                        'name': item_name,
                        'price': item.get('price', 100)  # Use actual price or default
                    }
                
                # Create columns for minus, quantity, plus
                minus_col, qty_col, plus_col = st.columns([1, 1, 1])
                
                with minus_col:
                    if st.button("➖", key=f"minus_{item_key}"):
                        if st.session_state.cart[item_key]['quantity'] > 0:
                            st.session_state.cart[item_key]['quantity'] -= 1
                            st.rerun()  # Force immediate rerun
                
                with qty_col:
                    st.markdown(f"<div style='text-align: center; font-size: 18px; font-weight: bold;'>{st.session_state.cart[item_key]['quantity']}</div>", unsafe_allow_html=True)
                
                with plus_col:
                    if st.button("➕", key=f"plus_{item_key}"):
                        st.session_state.cart[item_key]['quantity'] += 1
                        st.rerun()  # Force immediate rerun
            
            # Close the menu-item div
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")  # Separator between items

    except FileNotFoundError:
        st.error("Menu file not found. Please make sure 'data/menu.csv' exists.")
    except Exception as e:
        st.error(f"Error loading menu: {str(e)}")


