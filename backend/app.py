import sqlite3


def get_connection():
    return sqlite3.connect("stock.db")

def create_table():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                generic_name TEXT,
                dosage TEXT,
                form TEXT,
                price REAL,
                prescription_required BOOLEAN
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                batch_number TEXT,
                quantity INTEGER,
                expiration_date TEXT,
                location TEXT,
                FOREIGN KEY (product_id) REFERENCES Products(id)
            )
        """)


def add_product(name, generic_name, dosage, form, price, prescription_required,
                batch_number, quantity, expiration_date, location):
    with get_connection() as conn:
        cursor = conn.cursor()

        # Check if the product already exists
        cursor.execute("SELECT id FROM Products WHERE name=? AND dosage=? AND form=?", 
                       (name, dosage, form))
        result = cursor.fetchone()

        if result:
            product_id = result[0]
        else:
            cursor.execute("""
                INSERT INTO Products(name, generic_name, dosage, form, price, prescription_required)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, generic_name, dosage, form, price, prescription_required))
            product_id = cursor.lastrowid

        # Insert into Inventory
        cursor.execute("""
            INSERT INTO Inventory(product_id, batch_number, quantity, expiration_date, location)
            VALUES (?, ?, ?, ?, ?)
        """, (product_id, batch_number, quantity, expiration_date, location))




if __name__ == "__main__":
    create_table()

    add_product(
        name='Doliprane',
        generic_name='Paracétamol',
        dosage='500mg',
        form='Comprimé',
        price=6.75,
        prescription_required=True,
        batch_number='B12345',
        quantity=20,
        expiration_date='2025-09-10',
        location='Rayon A3'
    )
    
    add_product(
        name='Doliprane',
        generic_name='Paracétamol',
        dosage='500mg',
        form='Comprimé',
        price=6.75,
        prescription_required=True,
        batch_number='B12346',
        quantity=30,
        expiration_date='2025-10-15',
        location='Rayon A3'
    )