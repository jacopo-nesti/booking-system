import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "app", "database")
db_path = os.path.join(DB_DIR, "app.db")