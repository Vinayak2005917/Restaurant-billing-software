# utils/db_utils.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../db/restaurant.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            quantity INTEGER,
            total_price REAL,
            sale_time TEXT,
            FOREIGN KEY(item_id) REFERENCES menu(id)
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS cashiers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.commit()
