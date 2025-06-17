# Inventory Management System

## Project Overview

This is a desktop **Inventory Management System** built with **PySide6** (Qt for Python) and a local **SQLite** database. It helps businesses track products, manage incoming goods, and record sales efficiently. The application includes a secure login for operators and dedicated forms for all key inventory operations.

---

## What It Does (Features)

* **Operator Login:** Secure access for system users.

* **Product Master List:**
    * Add, update, and delete product details like barcode, SKU ID, category, name, description, tax rate, price, and default unit of measurement.
    * Attach product images for visual reference.
    * View all your products in a sortable table.

* **Goods Receiving Form:**
    * Record new stock coming in, including product details, supplier, quantity, rate per unit, and automatically calculated total rate and tax.
    * It conveniently pulls product details (like default unit and tax rate) for you.

* **Sales Form:**
    * Record outgoing sales, capturing product details, customer information, quantity, rate per unit, and automatically calculated total rate and tax.
    * This also fetches product details to speed up sales entry.

* **Local Database:** Uses **SQLite** for easy setup and local data storage, meaning no complex server setup is required.

---

## Technologies Used

* **Python 3.x:** The main programming language.

* **PySide6:** The framework used to create the graphical user interface (GUI).

* **SQLite3:** The database system that stores all your inventory data locally.

* **PyInstaller:** A tool that helps turn your Python application into a single, runnable file (like a `.exe` on Windows).

---

## Getting Started (Setup and Installation)

Follow these steps to set up and run the project on your computer.

### 1. Project Structure

Make sure all your Python files are in one directory, structured like this:
Okay, I understand. You want the entire README.md file's content to be presented in a single, large bash code block, so you can easily copy the whole thing, including the Markdown syntax itself, as if it were a script.

Here is the complete README.md file content formatted as a raw bash code block for easy copy-pasting:

Bash

# Inventory Management System

## Project Overview

This is a desktop **Inventory Management System** built with **PySide6** (Qt for Python) and a local **SQLite** database. It helps businesses track products, manage incoming goods, and record sales efficiently. The application includes a secure login for operators and dedicated forms for all key inventory operations.

---

## What It Does (Features)

* **Operator Login:** Secure access for system users.

* **Product Master List:**
    * Add, update, and delete product details like barcode, SKU ID, category, name, description, tax rate, price, and default unit of measurement.
    * Attach product images for visual reference.
    * View all your products in a sortable table.

* **Goods Receiving Form:**
    * Record new stock coming in, including product details, supplier, quantity, rate per unit, and automatically calculated total rate and tax.
    * It conveniently pulls product details (like default unit and tax rate) for you.

* **Sales Form:**
    * Record outgoing sales, capturing product details, customer information, quantity, rate per unit, and automatically calculated total rate and tax.
    * This also fetches product details to speed up sales entry.

* **Local Database:** Uses **SQLite** for easy setup and local data storage, meaning no complex server setup is required.

---

## Technologies Used

* **Python 3.x:** The main programming language.

* **PySide6:** The framework used to create the graphical user interface (GUI).

* **SQLite3:** The database system that stores all your inventory data locally.

* **PyInstaller:** A tool that helps turn your Python application into a single, runnable file (like a `.exe` on Windows).

---

## Getting Started (Setup and Installation)

Follow these steps to set up and run the project on your computer.

### 1. Project Structure

Make sure all your Python files are in one directory, structured like this:

your_project_name/
├── main.py
├── login_window.py
├── main_app_window.py
├── goods_receiving_form.py
├── sales_form.py
├── product_master_form.py
├── database_manager.py
└── requirements.txt (This file will be created by a command below)
### 2. Prepare Environment & Install Dependencies

Open your terminal or command prompt and run the following commands. These will navigate to your project, set up an isolated Python environment, and install necessary libraries.

```bash
# Navigate to your project directory
# Replace 'your_project_name' with the actual path to your project folder
cd your_project_name

# Create a Python virtual environment to manage dependencies
python -m venv venv

# Activate the virtual environment
# For Windows:
# .\venv\Scripts\activate
# For macOS/Linux:
source venv/bin/activate

# Install the required Python GUI library (PySide6)
pip install PySide6

# Optionally, generate a requirements.txt file for easy dependency management
pip freeze > requirements.txt
How to Run the Application
1. Initialize the Database
The inventory.db file (your local SQLite database) will be automatically created and set up with all necessary tables and default operator logins the first time the system starts. You can explicitly run the database setup:



# Ensure your virtual environment is active (if you closed your terminal, activate it again)
# For Windows:
# .\venv\Scripts\activate
# For macOS/Linux:
# source venv/bin/activate

# Run the database manager script to ensure the database file and tables are created
python database_manager.py
2. Launch the GUI Application
Once the database is set up, start the main application:


# Ensure your virtual environment is active
python main.py
