import sqlite3
import os

# creo directory e app.db se non esistono
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
db_path = os.path.join(DB_DIR, "app.db")

def init_db():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # crea tabella trattamenti
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS treatments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        duration_min INTEGER NOT NULL
        )
        """)
    
    # crea tabella prenotazioni
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT NOT NULL,
        booking_date TEXT NOT NULL,
        booking_time TEXT NOT NULL,
        treatment_id INTEGER NOT NULL,
        FOREIGN KEY (treatment_id) REFERENCES treatments(id)
        )
        """)
    
    conn.commit()
    conn.close()

# apre connesione al db ogni volta che serve
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row # così accedo alle colonne come dizionario
    return conn

# query SELECT/GET treatments
def get_treatments():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM treatments').fetchall()
    conn.close()
    return [dict(row) for row in rows]

# query INSERT treatments
def add_treatments(service_name, category, duration_min):
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO treatments (service_name, category, duration_min) 
        VALUES (?,?,?)""",
        (service_name, category, duration_min)
    )
    conn.commit()
    conn.close()

# query SELECT/GET treatments by id
def get_treatment_by_id(treatment_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM treatments WHERE id = ?',
                        (treatment_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

# query SELECT/GET bookings
def get_bookings():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM bookings').fetchall()
    conn.close()
    return [dict(row) for row in rows]

# query INSERT bookings
def add_bookings(name, surname, email, booking_date, booking_time, treatment_id):
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO bookings (name, surname, email, booking_date, booking_time, treatment_id) 
        VALUES (?,?,?,?,?,?)""",
        (name, surname, email, booking_date, booking_time, treatment_id)
    )
    conn.commit()
    conn.close()

# query SELECT/GET bookings by data
def get_bookings_by_date(date):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM bookings HWERE booking_date = ?',
                        (date,).fetchall())
    conn.close()
    return [dict(row) for row in rows]