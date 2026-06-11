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
        duration_min INTEGER NOT NULL,
        price TEXT NOT NULL
        )
        """)
    
    # crea tabella users
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
        )         
        """)
    
    # crea tabella prenotazioni
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        booking_date TEXT NOT NULL,
        booking_time TEXT NOT NULL,
        treatment_id INTEGER NOT NULL,
        interaction_level TEXT,
                   
        FOREIGN KEY (user_id) REFERENCES users(id),
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
def add_treatments(service_name, category, duration_min, price):
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO treatments (service_name, category, duration_min, price) 
        VALUES (?,?,?,?)""",
        (service_name, category, duration_min, price)
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
def add_bookings(user_id, booking_date, booking_time, treatment_id, interaction_level):
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO bookings (user_id, booking_date, booking_time, treatment_id, interaction_level) 
        VALUES (?,?,?,?,?)""",
        (user_id, booking_date, booking_time, treatment_id, interaction_level)
    )
    conn.commit()
    conn.close()

# query SELECT/GET bookings by data
def get_bookings_by_date(date):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM bookings WHERE booking_date = ?',
                        (date,)).fetchall()
    conn.close()
    return [dict(row) for row in rows]

# funzione create_user
def create_user(
    name,
    surname,
    email,
    password_hash,
    role="user"
):
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO users (name, surname, email, password_hash, role)
        VALUES (?,?,?,?,?)""",
        (name, surname, email, password_hash, role)
    )
    conn.commit()
    conn.close()

# funzione get_user_by_email
def get_user_by_email(email):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM users WHERE email = ?',
                        (email,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# funzione get_user_by_id
def get_user_by_id(user_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM users WHERE id = ?',
                       (user_id,)).fetchone()
    conn.close()
    if row:
        return dict(row)
    return None

# funzione prenotazioni utente
def get_bookings_by_user(user_id):
    conn = get_db_connection()

    rows = conn.execute("""
        SELECT
            bookings.*,
            treatments.service_name
        FROM bookings
        JOIN treatments
            ON bookings.treatment_id = treatments.id
        WHERE bookings.user_id = ?
        ORDER BY bookings.booking_date, bookings.booking_time
    """, (user_id,)).fetchall()
    
    conn.close()

    return [dict(row) for row in rows]

# funzione GET all bookings
def get_all_bookings():
    conn = get_db_connection()

    rows = conn.execute("""
        SELECT 
            bookings.*,
            users.name,
            users.surname,
            users.email
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        ORDER BY booking_date DESC, booking_time DESC
    """).fetchall()

    conn.close
    
    return [dict(row) for row in rows]

# funzione admin CREATE treatment
def create_treatment(service_name, duration_min, price, category):
    conn = get_db_connection()

    conn.execute("""
        INSERT INTO treatments (
            service_name,
            duration_min,
            price,
            category
        )
        VALUES (?,?,?,?)
    """, (service_name, duration_min, price, category))

    conn.commit()
    conn.close()

# funzione admin UPDATE treatment
def update_treatment(treatment_id, service_name, duration_min, price, category):
    conn = get_db_connection()

    conn.execute("""
        UPDATE treatments
        SET
            service_name = ?,
            duration_min = ?,
            price = ?,
            category = ?
        WHERE id = ?
    """, (service_name, duration_min, price, category, treatment_id))

    conn.commit()
    conn.close()

# funzione admin DELETE TREATMENT
def delete_treatment(treatment_id):
    conn = get_db_connection()

    conn.execute("""
        DELETE FROM treatments
        WHERE id = ? 
    """, (treatment_id,))

    conn.commit()
    conn.close()

# esegue una query SQL di lettura (SELECT) in modo sicuro e restituisce i risultati
def execute_query(query, params=[]):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row

    risultati = conn.execute(query, params).fetchall()
    conn.close()

    return risultati

