import streamlit as st
import time


def add_live_clock():
    """Inject a live clock at the bottom-right corner of the app.

    Uses Python's time module to get the current time.
    """
    # Get current time using Python's time module (only time, no date)
    current_time = time.strftime("%H:%M", time.localtime())
    
    clock_css = """
    <style>
    #live-clock {
        position: fixed;
        top: 50px;
        right: 50px;
        color: #ffffff;
        padding: 6px 10px;
        font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
        font-size: 2.5rem;
        font-weight: bold;
        z-index: 9999;
        pointer-events: none;
    }
    @media (max-width: 768px) {
        #live-clock { top: 8px; right: 8px; font-size: 1.2rem; }
    }
    </style>
    """

    clock_html = f"""
    <div id="live-clock">{current_time}</div>
    """

    try:
        st.markdown(clock_css + clock_html, unsafe_allow_html=True)
    except Exception:
        pass