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
                    base_quantity INTEGER NOT NULL,
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


def insert_item(name, batch_number, base_quantity, expiration_date, form, dosage, prescription_required):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            # Checks if item with same batch_number already exists
            cursor.execute("SELECT batch_number FROM Inventory WHERE batch_number = ?", (batch_number,))
            result = cursor.fetchone()
            if result is None:
                cursor.execute("""
                    INSERT INTO Inventory (name, batch_number, base_quantity, quantity_left, expiration_date, form, dosage, prescription_required )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (name, batch_number, base_quantity, base_quantity, expiration_date, form, dosage, prescription_required)
                )
                conn.commit()
            else:
                print("Item with same batch_number already exists!")

    except sqlite3.OperationalError as e:
        print("Error when inserting item :", e)


def substract_item(batch_number):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE Inventory SET quantity_left = quantity_left - 1 WHERE batch_number = ?", (batch_number,))
            conn.commit()

    except sqlite3.OperationalError as e:
        print("Error when substracting item : ", e)


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
        base_quantity=20,
        expiration_date='2025-09-10',
        form='Comprimé',
        dosage='500mg',
        prescription_required=True,
    )
    # Test de doublon
    insert_item(
        name='Doliprane',
        batch_number='B12345',
        base_quantity=20,
        expiration_date='2025-09-10',
        form='Comprimé',
        dosage='500mg',
        prescription_required=True,
    )

    for i in range(5):
        substract_item(batch_number='B12345')

    insert_item(
        name='Bajhfue',
        batch_number='F332',
        base_quantity=99,
        expiration_date='2007-09-10',
        form='blahblah',
        dosage='30kg',
        prescription_required=False,
    )

    remove_item(batch_number='F332')