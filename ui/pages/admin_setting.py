import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import utils.components as components
#add a clock
components.add_live_clock()


st.set_page_config(page_title="Admin Settings", layout="wide")

# Hide default page list and adjust sidebar padding (match other pages)
st.markdown(
	"""
	<style>
	#MainMenu {visibility: hidden;}
	[data-testid="stSidebarNav"] {display: none;}
	[data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; margin-top: 0 !important; }
	[data-testid="stSidebar"] > div:first-child > div { padding-top: 0 !important; margin-top: 0 !important; }
	.menu-item { border: none; border-radius: 0; padding: 10px 0; margin: 10px 0; background: transparent; }
	</style>
	""",
	unsafe_allow_html=True,
)

# Access control
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
	st.error("Please login to access this page")
	st.switch_page("login.py")
elif st.session_state.get('user_role') != 'admin':
	st.error("Access denied. Admin privileges required.")
	st.switch_page("login.py")

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
db_path = os.path.join(project_root, "db", "restaurant.db")

# Sidebar
with st.sidebar:
	st.markdown(f"<h2 style='text-align:center;'>🛠️ Admin Settings</h2>", unsafe_allow_html=True)
	st.markdown(f"<p style='text-align:center;'>Welcome, {st.session_state.get('username','Admin')}</p>", unsafe_allow_html=True)
	st.markdown("---")
	if st.button("🏠 Admin Panel", use_container_width=True):
		st.switch_page("pages/admin.py")
	if st.button("📊 Reports", use_container_width=True):
		st.switch_page("pages/reports.py")
	st.markdown("---")
	if st.button("🚪 Logout", use_container_width=True):
		for k in list(st.session_state.keys()):
			del st.session_state[k]
		st.switch_page("login.py")

st.markdown("<h1 style='text-align:center;'>Admin Settings</h1>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📦 Manage Stock", "👥 Cashiers"])

with tab1:
	st.subheader("Update Menu Stock")
	import sqlite3
	try:
		conn = sqlite3.connect(db_path)
		menu_df = pd.read_sql_query("SELECT * FROM menu", conn)
		conn.close()
	except Exception as e:
		st.error(f"Error reading menu table: {e}")
		menu_df = None

	if menu_df is not None:
		required_cols = {"item_id", "item_name", "stock"}
		if not required_cols.issubset(set(menu_df.columns)):
			st.error("menu table must contain columns: item_id, item_name, stock")
		else:
			if 'stock_values' not in st.session_state:
				st.session_state.stock_values = {}
			search_query = st.text_input("🔍 Search items...", placeholder="Search by name or description")
			st.markdown("---")
			for idx, row in menu_df.iterrows():
				name = row.get('item_name', f'Item {idx+1}')
				desc = row.get('short_description', '') if 'short_description' in menu_df.columns else ''
				if search_query:
					if search_query.lower() not in str(name).lower() and search_query.lower() not in str(desc).lower():
						continue
				item_id = row.get('item_id', idx)
				try:
					item_id_int = int(item_id)
				except Exception:
					item_id_int = idx
				key = f"id_{item_id_int}"
				current_stock = int(row.get('stock', 0) or 0)
				if key not in st.session_state.stock_values:
					st.session_state.stock_values[key] = current_stock

				st.markdown('<div class="menu-item">', unsafe_allow_html=True)
				c1, c2, c3 = st.columns([1, 3, 2])
				with c1:
					st.markdown("<div style='text-align:center; font-size: 48px;'>🍽️</div>", unsafe_allow_html=True)
				with c2:
					st.markdown(f"**{name}**")
					if desc:
						st.markdown(f"<small>{desc}</small>", unsafe_allow_html=True)
					st.markdown(f"Current Stock: {current_stock}")
				with c3:
					mcol, qty_col, pcol = st.columns([1, 2, 1])
					with mcol:
						if st.button("➖", key=f"dec_{key}"):
							st.session_state.stock_values[key] = max(0, st.session_state.stock_values[key] - 1)
							st.rerun()
					with qty_col:
						st.markdown(
							f"<div style='text-align:center; font-size:18px; font-weight:bold;'>New Stock: {int(st.session_state.stock_values[key])}</div>",
							unsafe_allow_html=True,
						)
					with pcol:
						if st.button("➕", key=f"inc_{key}"):
							st.session_state.stock_values[key] = st.session_state.stock_values[key] + 1
							st.rerun()
					# Per-item save button
					if st.button("💾 Save", key=f"save_{key}", use_container_width=True):
						try:
							new_val = int(st.session_state.stock_values[key])
							conn = sqlite3.connect(db_path)
							cursor = conn.cursor()
							cursor.execute("UPDATE menu SET stock = ? WHERE item_id = ?", (new_val, item_id_int))
							conn.commit()
							conn.close()
							st.success(f"Saved stock for {name}.")
							st.rerun()
						except Exception as e:
							st.error(f"Failed to save: {e}")
				st.markdown("---")

with tab2:
	st.subheader("Manage Cashiers")
	# Load existing cashier list from DB
	import sqlite3
	try:
		conn = sqlite3.connect(db_path)
		cashier_df = pd.read_sql_query("SELECT * FROM cashiers", conn)
		conn.close()
	except Exception:
		cashier_df = pd.DataFrame(columns=["username", "full_name", "password"])

	for col in ["username", "full_name", "password"]:
		if col not in cashier_df.columns:
			cashier_df[col] = ""

	with st.form("add_cashier_form"):
		st.markdown("### ➕ Add Cashier")
		new_username = st.text_input("Username", placeholder="unique username")
		new_fullname = st.text_input("Full name", placeholder="Cashier full name")
		new_password = st.text_input("Password", placeholder="Set a password", type="password")
		add_submit = st.form_submit_button("Add Cashier")
		if add_submit:
			if not new_username.strip() or not new_fullname.strip() or not new_password.strip():
				st.error("Please enter username, full name, and password.")
			else:
				if not cashier_df.empty and (cashier_df['username'] == new_username).any():
					st.error("Username already exists.")
				else:
					try:
						conn = sqlite3.connect(db_path)
						cursor = conn.cursor()
						cursor.execute("INSERT INTO cashiers (username, full_name, password) VALUES (?, ?, ?)",
									   (new_username.strip(), new_fullname.strip(), new_password.strip()))
						conn.commit()
						conn.close()
						st.success("Cashier added.")
						st.rerun()
					except Exception as e:
						st.error(f"Failed to save: {e}")

	st.markdown("---")
	st.markdown("### 🗂️ Cashier List")
	if cashier_df.empty:
		st.info("No cashiers yet.")
	else:
		for i, row in cashier_df.iterrows():
			c1, c2, c3, c4 = st.columns([3, 3, 3, 1])
			c1.write(f"**{row['full_name']}**")
			c2.write(f"`{row['username']}`")
			masked = '•' * len(str(row.get('password', '')))
			c3.write(masked if masked else '—')
			with c4:
				if st.button("🗑️ Delete", key=f"del_cashier_{i}"):
					try:
						conn = sqlite3.connect(db_path)
						cursor = conn.cursor()
						cursor.execute("DELETE FROM cashiers WHERE username = ?", (row['username'],))
						conn.commit()
						conn.close()
						st.success("Removed.")
						st.rerun()
					except Exception as e:
						st.error(f"Failed to remove: {e}")

