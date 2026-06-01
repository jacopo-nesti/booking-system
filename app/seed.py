from app.database import get_db_connection, init_db

def seed_treatments():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM treatments")
    count = cursor.fetchone()[0]

    if count == 0:
        treatments_seed = [
            ("Taglio Uomo", "Uomo", 30),
            ("Taglio Uomo + Shampoo", "Uomo", 45),
            ("Taglio Donna", "Donna", 45),
            ("Taglio Donna + Piega", "Donna", 75),
            ("Piega", "Donna", 45),
            ("Shampoo", "Unisex", 15),
            ("Barba", "Uomo", 15),
            ("Colore Ricrescita", "Donna", 60),
            ("Colore Completo", "Donna", 90),
            ("Tonalizzazione", "Donna", 30),
            ("Meches", "Donna", 120),
            ("Trattamento Ricostruzione", "Unisex", 45),
            ("Cheratina", "Unisex", 180),
            ("Acconciatura Cerimonia", "Donna", 120)
        ]
        
        cursor.executemany(
            """
            INSERT INTO treatments (service_name, category, duration_min)
            VALUES (?, ?, ?)
            """,
            treatments_seed
        )

        conn.commit()
        print("Seed treatments inserted")

    else:
        print("Treatments already present, skip seed")

    conn.close()