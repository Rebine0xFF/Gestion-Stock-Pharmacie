import sqlite3
from datetime import datetime, date


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
                    initial_quantity INTEGER NOT NULL,
                    quantity_left INTEGER,
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


def read_table():
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Inventory")
            rows = cursor.fetchall()

            today = date.today()
            result = []

            for row in rows:
                expiration_str = row[5]
                try:
                    expiration_date = datetime.strptime(expiration_str, "%Y-%m-%d").date()
                except ValueError:
                    expiration_date = None

                expired = expiration_date is not None and expiration_date < today
                result.append(list(row) + [expired])

            return result
    
    except sqlite3.OperationalError as e:
        print("Error when reading the table: ", e)


def insert_item(name, batch_number, initial_quantity, expiration_date, form, dosage, prescription_required):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Checks if item with same batch_number already exists
            cursor.execute("SELECT batch_number FROM Inventory WHERE batch_number = ?", (batch_number,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("""
                    INSERT INTO Inventory (name, batch_number, initial_quantity, quantity_left, expiration_date, form, dosage, prescription_required )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (name, batch_number, initial_quantity, initial_quantity, expiration_date, form, dosage, prescription_required)
                )
                conn.commit()
                return True
            else:
                print("Item with same batch_number already exists!")
                return False

    except sqlite3.OperationalError as e:
        print("Error when inserting item :", e)


def subtract_item(batch_number):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Inventory SET quantity_left = quantity_left - 1 WHERE batch_number = ?", (batch_number,))
            cursor.execute("DELETE FROM Inventory WHERE quantity_left <= 0")
            conn.commit()

    except sqlite3.OperationalError as e:
        print("Error when subtracting item : ", e)


def remove_item(batch_number):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM Inventory WHERE batch_number = ?", (batch_number,))
            conn.commit()
    
    except sqlite3.OperationalError as e:
        print("Error when removing item : ", e)



# TESTS
if __name__ == "__main__":
    create_table()

    insert_item(
        name='Doliprane',
        batch_number='B12345',
        initial_quantity=20,
        expiration_date='2025-09-10',
        form='Comprimé',
        dosage='500mg',
        prescription_required=True,
    )
    # Test de doublon
    insert_item(
        name='Doliprane',
        batch_number='B12345',
        initial_quantity=20,
        expiration_date='2025-09-10',
        form='Comprimé',
        dosage='500mg',
        prescription_required=True,
    )

    for i in range(5):
        subtract_item(batch_number='B12345')

    insert_item(
        name='Bajhfue',
        batch_number='F332',
        initial_quantity=99,
        expiration_date='2007-09-10',
        form='blahblah',
        dosage='30kg',
        prescription_required=False,
    )

    remove_item(batch_number='F332')

    insert_item(
        name='Amoxicilline',
        batch_number='A98765',
        initial_quantity=50,
        expiration_date='2026-01-15',
        form='Gélule',
        dosage='1g',
        prescription_required=True,
    )

    insert_item(
        name='Ibuprofène',
        batch_number='I54321',
        initial_quantity=30,
        expiration_date='2025-12-05',
        form='Comprimé',
        dosage='400mg',
        prescription_required=False,
    )