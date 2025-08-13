import streamlit as st
import json
import hashlib
import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
import utils.components as components
#add a clock
components.add_live_clock()


st.set_page_config(page_title="User Settings", layout="centered")

# Simple runtime theme application
def apply_theme_css(theme: str):
    if theme == "Dark":
        st.markdown(
            """
            <style>
            :root { --bg:#0e1117; --text:#e1e6ef; --card:#161a22; --accent:#4CAF50; --muted:#9aa4b2; }
            .stApp, .block-container { background-color: var(--bg) !important; color: var(--text) !important; }
            [data-testid="stSidebar"], [data-testid="stSidebar"] * { background-color: var(--card) !important; color: var(--text) !important; }
            .stButton > button { background-color: var(--accent) !important; color: #fff !important; border: 0 !important; }
            hr, small { color: var(--muted) !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )

# Hide default nav
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    [data-testid="stSidebarNav"] {display: none;}
    </style>
    """,
    unsafe_allow_html=True,
)


def project_root_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(os.path.dirname(current_dir))


def settings_path():
    root = project_root_dir()
    db_dir = os.path.join(root, "db")
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, "user_settings.json")


def load_settings():
    path = settings_path()
    if not os.path.exists(path):
        return {"users": {}}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"users": {}}


def save_settings(data: dict):
    path = settings_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def hash_password(password: str, salt: str | None = None) -> str:
    if salt is None:
        salt = os.urandom(8).hex()
    h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"sha256:{salt}:{h}"


def verify_password(stored: str, candidate: str) -> bool:
    try:
        algo, salt, digest = stored.split(":", 2)
        if algo != "sha256":
            return False
        cand = hashlib.sha256((salt + candidate).encode("utf-8")).hexdigest()
        return cand == digest
    except Exception:
        return False


# Require login
if not st.session_state.get("logged_in"):
    st.error("Please login to access settings")
    st.switch_page("login.py")

username = st.session_state.get("username", "guest")
# Apply theme from session (default Light)
apply_theme_css(st.session_state.get("pref_theme", "Light"))

st.markdown(f"<h1 style='text-align:center;'>👤 User Settings</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;'>Signed in as <b>{username}</b></p>", unsafe_allow_html=True)

# Sidebar (same as New Order page)
with st.sidebar:
    st.markdown("### 👨‍💼 Staff Info")
    st.write("**Name:** Vinayak Mishra")
    st.write("**Role:** Cashier")
    st.markdown("---")

    if st.button("New Order"):
        st.switch_page("pages/new order.py")
    if st.button("Reports"):
        st.switch_page("pages/reports.py")
    if st.button("Log Out"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.switch_page("login.py")

data = load_settings()
user = data.setdefault("users", {}).setdefault(
    username,
    {
        "full_name": username,
        "password_hash": "",
    "theme": "Light",
        "updated_at": "",
    },
)

with st.form("profile_form"):
    st.subheader("Profile")
    full_name = st.text_input("Full name", value=user.get("full_name", username))

    st.markdown("---")
    st.subheader("Change Password")
    has_pwd = bool(user.get("password_hash"))
    new_pwd = st.text_input("New password", type="password")
    confirm_pwd = st.text_input("Confirm new password", type="password")

    submitted = st.form_submit_button("💾 Save settings", type="primary")

    if submitted:
        # Update profile + prefs
        user["full_name"] = full_name.strip() or username

        # Handle password change if provided
        if new_pwd or confirm_pwd:
            if new_pwd != confirm_pwd:
                st.error("New password and confirmation do not match.")
                st.stop()
            if len(new_pwd) < 4:
                st.error("Password must be at least 4 characters.")
                st.stop()
            user["password_hash"] = hash_password(new_pwd)

        user["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["users"][username] = user
        try:
            save_settings(data)
            # Update session quick prefs
            st.session_state["display_name"] = user["full_name"]
            # default order type removed
            st.success("Settings saved.")
        except Exception as e:
            st.error(f"Failed to save settings: {e}")
        # Rerun to apply theme immediately if changed
        st.rerun()

