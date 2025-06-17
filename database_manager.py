import sqlite3
import os

DATABASE_NAME = 'inventory.db'

class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self._connect()
        if self.conn is None or self.cursor is None:
            raise Exception("Database connection failed. Cannot create tables.")
        else:
            self._create_tables()

    def _connect(self):
        try:
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.cursor = self.conn.cursor()
            print(f"Connected to database: {DATABASE_NAME}")
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            # Handle error appropriately, e.g., exit application

    def _create_tables(self):
        if self.conn is None or self.cursor is None:
            print("Cannot create tables: Database connection or cursor is not available.")
            return
        try:
            # Users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL, -- In a real app, hash this!
                    role TEXT DEFAULT 'operator'
                )
            ''')

            # Products table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    barcode TEXT UNIQUE,
                    sku_id TEXT UNIQUE NOT NULL,
                    category TEXT,
                    subcategory TEXT,
                    product_name TEXT NOT NULL,
                    description TEXT,
                    tax_percentage REAL NOT NULL DEFAULT 0.0,
                    price REAL NOT NULL,
                    default_unit TEXT,
                    image_path TEXT
                )
            ''')

            # Suppliers table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS suppliers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    supplier_name TEXT NOT NULL,
                    contact_person TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT
                )
            ''')

            # Customers table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS customers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_name TEXT NOT NULL,
                    contact_person TEXT,
                    phone TEXT,
                    email TEXT,
                    address TEXT
                )
            ''')

            # Goods Receipts table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS goods_receipts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    receipt_date TEXT NOT NULL,
                    product_id INTEGER NOT NULL,
                    supplier_id INTEGER NOT NULL,
                    quantity REAL NOT NULL,
                    unit_of_measurement TEXT NOT NULL,
                    rate_per_unit REAL NOT NULL,
                    total_rate REAL NOT NULL,
                    tax_amount REAL NOT NULL,
                    operator_id INTEGER NOT NULL,
                    FOREIGN KEY(product_id) REFERENCES products(id),
                    FOREIGN KEY(supplier_id) REFERENCES suppliers(id),
                    FOREIGN KEY(operator_id) REFERENCES users(id)
                )
            ''')

            # Sales table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_date TEXT NOT NULL,
                    product_id INTEGER NOT NULL,
                    customer_id INTEGER NOT NULL,
                    quantity REAL NOT NULL,
                    unit_of_measurement TEXT NOT NULL,
                    rate_per_unit REAL NOT NULL,
                    total_rate REAL NOT NULL,
                    tax_amount REAL NOT NULL,
                    operator_id INTEGER NOT NULL,
                    FOREIGN KEY(product_id) REFERENCES products(id),
                    FOREIGN KEY(customer_id) REFERENCES customers(id),
                    FOREIGN KEY(operator_id) REFERENCES users(id)
                )
            ''')
            self.conn.commit()
            print("Database tables checked/created successfully.")
            self._add_default_users() # Add default users after table creation

        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def _add_default_users(self):
        # Add default operator logins if they don't exist
        users_to_add = [
            ('operator1', 'pass123', 'operator'),
            ('operator2', 'securepass', 'operator')
        ]
        for username, password, role in users_to_add:
            try:
                if self.cursor is not None:
                    self.cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                                        (username, password, role))
                    if self.conn is not None:
                        self.conn.commit()
                    print(f"Default user '{username}' added.")
                else:
                    print("Cannot add default user: Cursor is not available.")
            except sqlite3.IntegrityError:
                print(f"User '{username}' already exists.")
            except sqlite3.Error as e:
                print(f"Error adding default user '{username}': {e}")

    def close_connection(self):
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        if self.cursor is None:
            print("Database query error: Cursor is not available.")
            return False
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            if self.conn is not None:
                self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return False

    def fetch_all(self, query, params=None):
        try:
            if self.cursor is None:
                print("Database fetch error: Cursor is not available.")
                return []
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database fetch error: {e}")
            return []

    def fetch_one(self, query, params=None):
        try:
            if self.cursor is None:
                print("Database fetch error: Cursor is not available.")
                return None
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database fetch error: {e}")
            return None

    # --- Specific CRUD Operations (Examples) ---

    def verify_user(self, username, password):
        query = "SELECT id, username, role FROM users WHERE username = ? AND password = ?"
        user = self.fetch_one(query, (username, password))
        if user:
            return {'id': user[0], 'username': user[1], 'role': user[2]}
        return None

    def add_product(self, barcode, sku_id, category, subcategory, product_name, description, tax_percentage, price, default_unit, image_path):
        query = '''
            INSERT INTO products (barcode, sku_id, category, subcategory, product_name, description, tax_percentage, price, default_unit, image_path)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (barcode, sku_id, category, subcategory, product_name, description, tax_percentage, price, default_unit, image_path))

    def get_all_products(self):
        query = "SELECT id, barcode, sku_id, category, subcategory, product_name, description, tax_percentage, price, default_unit, image_path FROM products"
        return self.fetch_all(query)

    def get_product_by_id(self, product_id):
        query = "SELECT * FROM products WHERE id = ?"
        return self.fetch_one(query, (product_id,))

    def get_product_by_sku(self, sku_id):
        query = "SELECT * FROM products WHERE sku_id = ?"
        return self.fetch_one(query, (sku_id,))

    def update_product(self, product_id, barcode, sku_id, category, subcategory, product_name, description, tax_percentage, price, default_unit, image_path):
        query = '''
            UPDATE products SET
                barcode = ?, sku_id = ?, category = ?, subcategory = ?, product_name = ?,
                description = ?, tax_percentage = ?, price = ?, default_unit = ?, image_path = ?
            WHERE id = ?
        '''
        return self.execute_query(query, (barcode, sku_id, category, subcategory, product_name, description, tax_percentage, price, default_unit, image_path, product_id))

    def delete_product(self, product_id):
        query = "DELETE FROM products WHERE id = ?"
        return self.execute_query(query, (product_id,))

    def add_supplier(self, name, contact, phone, email, address):
        query = "INSERT INTO suppliers (supplier_name, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?)"
        return self.execute_query(query, (name, contact, phone, email, address))

    def get_all_suppliers(self):
        query = "SELECT id, supplier_name FROM suppliers"
        return self.fetch_all(query)

    def add_customer(self, name, contact, phone, email, address):
        query = "INSERT INTO customers (customer_name, contact_person, phone, email, address) VALUES (?, ?, ?, ?, ?)"
        return self.execute_query(query, (name, contact, phone, email, address))

    def get_all_customers(self):
        query = "SELECT id, customer_name FROM customers"
        return self.fetch_all(query)

    def add_goods_receipt(self, receipt_date, product_id, supplier_id, quantity, unit, rate_per_unit, total_rate, tax_amount, operator_id):
        query = '''
            INSERT INTO goods_receipts (receipt_date, product_id, supplier_id, quantity, unit_of_measurement, rate_per_unit, total_rate, tax_amount, operator_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (receipt_date, product_id, supplier_id, quantity, unit, rate_per_unit, total_rate, tax_amount, operator_id))

    def add_sale(self, sale_date, product_id, customer_id, quantity, unit, rate_per_unit, total_rate, tax_amount, operator_id):
        query = '''
            INSERT INTO sales (sale_date, product_id, customer_id, quantity, unit_of_measurement, rate_per_unit, total_rate, tax_amount, operator_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        return self.execute_query(query, (sale_date, product_id, customer_id, quantity, unit, rate_per_unit, total_rate, tax_amount, operator_id))

# Example Usage (for testing the DB manager)
if __name__ == '__main__':
    db = DatabaseManager()
    # You can add test queries here to verify table creation and user insertion
    print("\nVerifying default users:")
    user1 = db.verify_user('operator1', 'pass123')
    user2 = db.verify_user('operator2', 'securepass')
    print(f"Operator1 login success: {user1 is not None}")
    print(f"Operator2 login success: {user2 is not None}")

    # Clean up (optional)
    # db.close_connection()