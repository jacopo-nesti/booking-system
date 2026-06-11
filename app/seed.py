from app.database import get_db_connection, init_db, get_user_by_email, create_user
from app.auth import hash_password
import os

def seed_treatments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM treatments")
    count = cursor.fetchone()[0]

    if count == 0:
        treatments_seed = [
            ("Taglio Uomo", "Uomo", 30, 25.00),
            ("Taglio Uomo + Shampoo", "Uomo", 45, 30.00),
            ("Taglio Donna", "Donna", 45, 50.00),
            ("Taglio Donna + Piega", "Donna", 75, 75.00),
            ("Piega", "Donna", 45, 25.00),
            ("Shampoo", "Unisex", 15, 8.00),
            ("Barba", "Uomo", 15, 12.00),
            ("Colore Ricrescita", "Donna", 60, 55.00),
            ("Colore Completo", "Donna", 90, 80.00),
            ("Tonalizzazione", "Donna", 30, 25.00),
            ("Meches", "Donna", 120, 110.00),
            ("Trattamento Ricostruzione", "Unisex", 45, 35.00),
            ("Cheratina", "Unisex", 180, 180.00),
            ("Acconciatura Cerimonia", "Donna", 120, 100.00),
        ]
        
        cursor.executemany(
            """
            INSERT INTO treatments (service_name, category, duration_min, price)
            VALUES (?, ?, ?, ?)
            """,
            treatments_seed
        )

        conn.commit()
        print("Seed treatments inserted")

    else:
        print("Treatments already present, skip seed")

    conn.close()

def seed_admin():
    admin = get_user_by_email(os.getenv("ADMIN_EMAIL"))

    if admin:
        return
    
    create_user(
        name="Admin",
        surname="System",
        email=os.getenv("ADMIN_EMAIL"),
        password_hash=hash_password(os.getenv("ADMIN_PASSWORD")),
        role="admin"
    )