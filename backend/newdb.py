import sqlite3


def get_connection():
    return sqlite3.connect("backend\\stock.db")


def create_table():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Inventory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    batch_number TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    expiration_date TEXT,
                    price REAL,
                    location TEXT,
                    form TEXT,
                    dosage TEXT,
                    prescription_required BOOLEAN )
                """)
            conn.commit()

    except sqlite3.OperationalError as e:
        print("Error when creating table: ", e)


def insert_item(name, batch_number, quantity, expiration_date, form, dosage, prescription_required):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Checks if item with same batch_number already exists
            cursor.execute("SELECT * FROM Inventory WHERE batch_number = ?", (batch_number,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("""
                    INSERT INTO Inventory (name, batch_number, quantity, expiration_date, form, dosage, prescription_required )
                    VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (name, batch_number, quantity, expiration_date, form, dosage, prescription_required)
                )
                conn.commit()
            else:
                print("Item with same batch_number already exists!")

    except sqlite3.OperationalError as e:
        print("Error when inserting item :", e)



# TESTS
if __name__ == "__main__":
    create_table()
    insert_item(
        name='Doliprane',
        batch_number='B12345',
        quantity=20,
        expiration_date='2025-09-10',
        form='Comprimé',
        dosage='500mg',
        prescription_required=True,
    )
    # Test de doublon
    insert_item(
        name='Doliprane',
        batch_number='B12345',
        quantity=20,
        expiration_date='2025-09-10',
        form='Comprimé',
        dosage='500mg',
        prescription_required=True,
    )