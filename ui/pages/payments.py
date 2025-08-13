import streamlit as st
import pandas as pd
import os
import random
import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import utils.components as components
#add a clock
components.add_live_clock()


# ---- UI SETUP ----
st.set_page_config(page_title="Restaurant Billing Software", layout="wide")
st.set_page_config(page_title="Payment", layout="centered")

hide_sidebar = """
    <style>
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    </style>
"""
hide_menu = """
    <style>
    #MainMenu {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)
st.markdown(hide_menu, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Select a Payment Method</h1>", unsafe_allow_html=True)
st.write("")

# Only show the confirmation button and extra UI for the selected payment mode
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
cart = st.session_state.get("cart", {})
table_number = st.session_state.get("table_number", "")
total_price = st.session_state.get("total_price", 0.0)
total_items = st.session_state.get("total_items", 0)

# Helper: decrement stock in data/menu.csv for items in cart
def decrement_menu_stock(cart_items):
    try:
        menu_path = os.path.join(project_root, "data", "menu.csv")
        if not os.path.exists(menu_path):
            return False, "menu.csv not found"
        df = pd.read_csv(menu_path)
        if 'item_name' not in df.columns or 'stock' not in df.columns:
            return False, "menu.csv missing required columns"
        # Build a quick lookup for current stocks
        for _, item in list(cart_items.items()):
            qty = int(item.get('quantity', 0) or 0)
            if qty <= 0:
                continue
            name = item.get('name')
            if not name:
                continue
            mask = df['item_name'] == name
            if mask.any():
                try:
                    current_stock = int(pd.to_numeric(df.loc[mask, 'stock']).iloc[0])
                except Exception:
                    # If stock not numeric, skip updating that row
                    continue
                new_stock = max(0, current_stock - qty)
                df.loc[mask, 'stock'] = new_stock
        df.to_csv(menu_path, index=False)
        return True, None
    except Exception as e:
        return False, str(e)

# Determine order type based on the source page or table_number format
# If table_number is a number, it's dine-in; if it's text, it's take-away
order_type = "Take-away"
table_label = "Customer"
try:
    # Try to convert to int - if successful, it's a table number (Dine-in)
    int(table_number)
    order_type = "Dine-in"
    table_label = "Table"
except (ValueError, TypeError):
    # If conversion fails, it's a customer name (Take-away)
    order_type = "Take-away"
    table_label = "Customer"

# Check if cart is empty and redirect
if not cart or total_items == 0:
    st.warning("Cart is empty. Redirecting to main page...")
    st.session_state.page = "home"
    st.switch_page("pages/new order.py")


# ---- Show order summary before payment confirmation (above payment mode buttons, plain text) ----
summary_lines = []
if cart:
    for item in cart.values():
        if item["quantity"] > 0:
            summary_lines.append(f"- {item['name']} x {item['quantity']} = ₹{item['quantity'] * item['price']:.2f}")

if summary_lines:
    st.markdown("**Order Summary**", unsafe_allow_html=True)
    st.markdown("\n".join(summary_lines))
    
    # Calculate subtotal, GST, and total
    subtotal = total_price
    gst_rate = 0.05  # 5% GST
    gst_amount = subtotal * gst_rate
    final_total = subtotal + gst_amount
    
    st.markdown("---")
    st.markdown(f"**Subtotal:** ₹{subtotal:.2f}")
    st.markdown(f"**GST (5%):** ₹{gst_amount:.2f}")
    st.markdown(f"**Final Total:** ₹{final_total:.2f}")
    st.markdown(f"**Total Items:** {total_items}")
    
    # Update session state with final total for payment processing
    st.session_state.final_total = final_total
    st.session_state.gst_amount = gst_amount
    st.session_state.subtotal = subtotal

# Ensure payment_mode is always initialized
if 'payment_mode' not in st.session_state:
    st.session_state['payment_mode'] = None

# ---- Payment mode selector ----
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("Discount", use_container_width=True):
        discount_code = st.text_input("Enter discount code", "")
        if st.button("Apply Discount"):
            if discount_code == "1":
                st.session_state.final_total *= 0.8  # Apply 20% discount
                st.success("Discount applied successfully!")
            else:
                st.error("Invalid discount code.")
    st.write("code : 1")
    if st.button("💸 UPI", use_container_width=True, key="btn_upi"):
        st.session_state['payment_mode'] = "UPI"
    if st.button("💵 Cash", use_container_width=True, key="btn_cash"):
        st.session_state['payment_mode'] = "Cash"
    if st.button("💳 Card", use_container_width=True, key="btn_card"):
        st.session_state['payment_mode'] = "Card"

if st.session_state['payment_mode'] == "UPI":
    image_path = os.path.join(project_root, "utils", "Screenshot 2025-08-03 224644.png")
    c1, c2, c3 = st.columns([2, 3, 1])
    with c2:
        st.image(image_path, width=200)
        st.markdown("<div style='text-align: center;'>Scan the QR to complete payment</div>", unsafe_allow_html=True)
    if st.button("✅ Confirm UPI Payment", use_container_width=True, key="confirm_upi"):
        if not cart:
            st.warning("Cart is empty.")
            st.switch_page("pages/new order.py")
        else:
            final_total = st.session_state.get('final_total', total_price)
            order_number = f"ORD{random.randint(10000, 99999)}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order_data = {
                'order_number': order_number,
                'order_type': order_type,
                'table_number': table_number,
                'total_amount': final_total,
                'total_items': total_items,
                'timestamp': timestamp,
                'items_detail': []
            }
            for item_key, item in cart.items():
                if item["quantity"] > 0:
                    detail = f"{item['name']} x {item['quantity']} = ₹{item['quantity'] * item['price']:.2f}"
                    order_data["items_detail"].append(detail)
            items_string = " | ".join(order_data["items_detail"])
            csv_data = {
                'Order_Number': [order_number],
                'Order_Type': [order_type],
                'Table_Number': [table_number],
                'Total_Amount': [final_total],
                'Total_Items': [total_items],
                'Items_Detail': [items_string],
                'Timestamp': [timestamp]
            }
            try:
                csv_path = os.path.join(project_root, "data", "sales_report.csv")
                if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
                    try:
                        existing = pd.read_csv(csv_path)
                        updated = pd.concat([existing, pd.DataFrame(csv_data)], ignore_index=True)
                        updated.to_csv(csv_path, index=False)
                    except pd.errors.EmptyDataError:
                        pd.DataFrame(csv_data).to_csv(csv_path, index=False)
                else:
                    pd.DataFrame(csv_data).to_csv(csv_path, index=False)
                # Decrement stock in menu.csv now that payment is confirmed
                ok, err = decrement_menu_stock(cart)
                if not ok and err:
                    st.warning(f"Stock update skipped: {err}")
                # Store order info in session for PDF download
                st.session_state['last_order'] = {
                    'order_number': order_number,
                    'table_number': table_number,
                    'total_price': final_total,
                    'subtotal': st.session_state.get('subtotal', total_price),
                    'gst_amount': st.session_state.get('gst_amount', 0),
                    'total_items': total_items,
                    'timestamp': timestamp,
                    'payment_mode': st.session_state.payment_mode
                }
                st.session_state['show_pdf'] = True
                st.session_state.payment_mode = None
            except Exception as e:
                st.error(f"❌ Error saving order: {str(e)}")

elif st.session_state['payment_mode'] == "Cash":
    if st.button("✅ Confirm Cash Payment", use_container_width=True, key="confirm_cash"):
        if not cart:
            st.warning("Cart is empty.")
            st.session_state.page = "home"
            st.switch_page("pages/new order.py")
        else:
            final_total = st.session_state.get('final_total', total_price)
            order_number = f"ORD{random.randint(10000, 99999)}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order_data = {
                'order_number': order_number,
                'order_type': order_type,
                'table_number': table_number,
                'total_amount': final_total,
                'total_items': total_items,
                'timestamp': timestamp,
                'items_detail': []
            }
            for item_key, item in cart.items():
                if item["quantity"] > 0:
                    detail = f"{item['name']} x {item['quantity']} = ₹{item['quantity'] * item['price']:.2f}"
                    order_data["items_detail"].append(detail)
            items_string = " | ".join(order_data["items_detail"])
            csv_data = {
                'Order_Number': [order_number],
                'Order_Type': [order_type],
                'Table_Number': [table_number],
                'Total_Amount': [final_total],
                'Total_Items': [total_items],
                'Items_Detail': [items_string],
                'Timestamp': [timestamp]
            }
            try:
                csv_path = os.path.join(project_root, "data", "sales_report.csv")
                if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
                    try:
                        existing = pd.read_csv(csv_path)
                        updated = pd.concat([existing, pd.DataFrame(csv_data)], ignore_index=True)
                        updated.to_csv(csv_path, index=False)
                    except pd.errors.EmptyDataError:
                        pd.DataFrame(csv_data).to_csv(csv_path, index=False)
                else:
                    pd.DataFrame(csv_data).to_csv(csv_path, index=False)
                # Decrement stock for confirmed order
                ok, err = decrement_menu_stock(cart)
                if not ok and err:
                    st.warning(f"Stock update skipped: {err}")
                st.session_state['last_order'] = {
                    'order_number': order_number,
                    'table_number': table_number,
                    'total_price': final_total,
                    'subtotal': st.session_state.get('subtotal', final_total),
                    'gst_amount': st.session_state.get('gst_amount', 0),
                    'total_items': total_items,
                    'timestamp': timestamp,
                    'payment_mode': st.session_state.payment_mode
                }
                st.session_state['show_pdf'] = True
                st.session_state.payment_mode = None
            except Exception as e:
                st.error(f"❌ Error saving order: {str(e)}")
                st.switch_page("pages/new order.py")

elif st.session_state['payment_mode'] == "Card":
    if st.button("✅ Confirm Card Payment", use_container_width=True, key="confirm_card"):
        if not cart:
            st.warning("Cart is empty.")
            st.session_state.page = "home"
            st.switch_page("pages/new order.py")
        else:
            final_total = st.session_state.get('final_total', total_price)
            order_number = f"ORD{random.randint(10000, 99999)}"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            order_data = {
                'order_number': order_number,
                'order_type': order_type,
                'table_number': table_number,
                'total_amount': final_total,
                'total_items': total_items,
                'timestamp': timestamp,
                'items_detail': []
            }
            for item_key, item in cart.items():
                if item["quantity"] > 0:
                    detail = f"{item['name']} x {item['quantity']} = ₹{item['quantity'] * item['price']:.2f}"
                    order_data["items_detail"].append(detail)
            items_string = " | ".join(order_data["items_detail"])
            csv_data = {
                'Order_Number': [order_number],
                'Order_Type': [order_type],
                'Table_Number': [table_number],
                'Total_Amount': [final_total],
                'Total_Items': [total_items],
                'Items_Detail': [items_string],
                'Timestamp': [timestamp]
            }
            try:
                csv_path = os.path.join(project_root, "data", "sales_report.csv")
                if os.path.exists(csv_path) and os.path.getsize(csv_path) > 0:
                    try:
                        existing = pd.read_csv(csv_path)
                        updated = pd.concat([existing, pd.DataFrame(csv_data)], ignore_index=True)
                        updated.to_csv(csv_path, index=False)
                    except pd.errors.EmptyDataError:
                        pd.DataFrame(csv_data).to_csv(csv_path, index=False)
                else:
                    pd.DataFrame(csv_data).to_csv(csv_path, index=False)
                # Decrement stock for confirmed order
                ok, err = decrement_menu_stock(cart)
                if not ok and err:
                    st.warning(f"Stock update skipped: {err}")
                st.session_state['last_order'] = {
                    'order_number': order_number,
                    'table_number': table_number,
                    'total_price': final_total,
                    'subtotal': st.session_state.get('subtotal', total_price),
                    'gst_amount': st.session_state.get('gst_amount', 0),
                    'total_items': total_items,
                    'timestamp': timestamp,
                    'payment_mode': st.session_state.payment_mode
                }
                st.session_state['show_pdf'] = True
                st.session_state.payment_mode = None
            except Exception as e:
                st.error(f"❌ Error saving order: {str(e)}")
                st.session_state.page = "home"
                st.switch_page("pages/new order.py")

# ---- Show PDF download and summary after payment ----
if st.session_state.get('show_pdf') and st.session_state.get('last_order'):
    order = st.session_state['last_order']
    st.success(f"✅ Order {order['order_number']} placed successfully!")
    
    # Get GST details for display
    subtotal = order.get('subtotal', order['total_price'])
    gst_amount = order.get('gst_amount', 0)
    
    st.info(f"**Order Summary:**\n"
            f"- 🏷️ Order Number: {order['order_number']}\n"
            f"- 🍽️ Table: {order['table_number']}\n"
            f"- 💰 Subtotal: ₹{subtotal:.2f}\n"
            f"- 📊 GST (5%): ₹{gst_amount:.2f}\n"
            f"- 💰 Final Total: ₹{order['total_price']:.2f}\n"
            f"- 📦 Items: {order['total_items']}\n"
            f"- 🕒 Time: {order['timestamp']}\n"
            f"- 💳 Payment Mode: {order['payment_mode']}")
    from fpdf import FPDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=20)
    pdf.cell(0, 15, "Bill", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(2)
    pdf.cell(0, 10, f"Order Number: {order['order_number']}", ln=True)
    pdf.cell(0, 10, f"Table/Customer: {order['table_number']}", ln=True)
    pdf.cell(0, 10, f"Time: {order['timestamp']}", ln=True)
    pdf.ln(2)
    pdf.set_font("Arial", style="B", size=12)
    pdf.cell(80, 10, "Item", border=0)
    pdf.cell(30, 10, "Qty", border=0)
    pdf.cell(40, 10, "Price", border=0)
    pdf.ln()
    pdf.set_font("Arial", size=12)
    # List all items in the order
    items_detail = []
    if 'items_detail' in order:
        items_detail = order['items_detail']
    else:
        # Try to reconstruct from cart if not present
        items_detail = []
    # Try to get item details from sales_report.csv if not in session
    if not items_detail:
        try:
            csv_path = os.path.join(project_root, "data", "sales_report.csv")
            df = pd.read_csv(csv_path)
            row = df[df['Order_Number'] == order['order_number']]
            if not row.empty:
                items_string = row.iloc[0]['Items_Detail']
                items_detail = [x.strip() for x in items_string.split('|')]
        except Exception:
            pass
    for item_line in items_detail:
        # Try to parse: "Item x Qty = ₹Price" and replace ₹ with Rs for PDF compatibility
        try:
            name_qty, price = item_line.split('=')
            name, qty = name_qty.rsplit('x', 1)
            price_str = price.strip().replace('₹', 'Rs')
            pdf.cell(80, 10, name.strip(), border=0)
            pdf.cell(30, 10, qty.strip(), border=0)
            pdf.cell(40, 10, price_str, border=0)
            pdf.ln()
        except Exception:
            pdf.cell(0, 10, item_line.replace('₹', 'Rs'), ln=True)
    pdf.ln(2)
    pdf.set_font("Arial", style="B", size=12)
    
    # Get GST details for PDF
    subtotal = order.get('subtotal', order['total_price'])
    gst_amount = order.get('gst_amount', 0)
    
    # Add billing breakdown with clear GST percentage
    pdf.cell(0, 10, f"Subtotal: Rs {subtotal:.2f}", ln=True)
    pdf.cell(0, 10, f"GST (5%): Rs {gst_amount:.2f}", ln=True)
    pdf.cell(0, 10, "-" * 40, ln=True)
    pdf.cell(0, 10, f"Total Amount: Rs {order['total_price']:.2f}", ln=True)
    pdf.ln(2)
    pdf.cell(0, 10, f"Payment Method: {order['payment_mode']}", ln=True)
    pdf.cell(0, 10, f"Order Number: {order['order_number']}", ln=True)
    pdf_output = pdf.output(dest='S').encode('latin1')
    st.download_button(
        label="⬇️ Download PDF Receipt",
        data=pdf_output,
        file_name=f"receipt_{order['order_number']}.pdf",
        mime="application/pdf"
    )
    # Optionally, add a button to clear session and return to main page
    if st.button("Back to Home"):
        st.session_state.cart = {}
        st.session_state.payment_mode = None
        st.session_state.show_pdf = False
        st.session_state.last_order = None
        st.session_state.page = "home"
        st.switch_page("pages/new order.py")
