import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QPushButton, QLabel, QDoubleSpinBox,
                               QComboBox, QMessageBox, QDateEdit)
from PySide6.QtCore import Qt, QDate
from database_manager import DatabaseManager

class SalesForm(QWidget):
    def __init__(self, operator_id):
        super().__init__()
        self.operator_id = operator_id
        self.db_manager = DatabaseManager()
        self.init_ui()
        self.load_initial_data()

    def init_ui(self):
        self.setWindowTitle("Sales Form")
        self.main_layout = QVBoxLayout()

        # Input fields
        self.form_grid = QVBoxLayout()

        self.date_input = QDateEdit(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.form_grid.addWidget(QLabel("Sale Date:"))
        self.form_grid.addWidget(self.date_input)

        self.product_combo = QComboBox()
        self.product_combo.setPlaceholderText("Select Product")
        self.product_combo.currentIndexChanged.connect(self.update_product_details)
        self.form_grid.addWidget(QLabel("Product:"))
        self.form_grid.addWidget(self.product_combo)

        self.customer_combo = QComboBox()
        self.customer_combo.setPlaceholderText("Select Customer")
        self.form_grid.addWidget(QLabel("Customer:"))
        self.form_grid.addWidget(self.customer_combo)

        self.quantity_input = QDoubleSpinBox()
        self.quantity_input.setRange(0.01, 99999.99)
        self.quantity_input.setDecimals(2)
        self.quantity_input.valueChanged.connect(self.calculate_totals)
        self.form_grid.addWidget(QLabel("Quantity:"))
        self.form_grid.addWidget(self.quantity_input)

        self.unit_of_measurement_input = QLineEdit()
        self.unit_of_measurement_input.setPlaceholderText("Unit (e.g., Pcs, Kg)")
        self.form_grid.addWidget(QLabel("Unit of Measurement:"))
        self.form_grid.addWidget(self.unit_of_measurement_input)

        self.rate_per_unit_input = QDoubleSpinBox()
        self.rate_per_unit_input.setRange(0.01, 99999.99)
        self.rate_per_unit_input.setDecimals(2)
        self.rate_per_unit_input.valueChanged.connect(self.calculate_totals)
        self.form_grid.addWidget(QLabel("Rate Per Unit:"))
        self.form_grid.addWidget(self.rate_per_unit_input)

        self.tax_percentage_display = QLabel("Tax: 0.00%") # Display tax from product master
        self.form_grid.addWidget(self.tax_percentage_display)

        self.total_rate_label = QLabel("Total Rate: $0.00")
        self.form_grid.addWidget(self.total_rate_label)

        self.tax_amount_label = QLabel("Tax Amount: $0.00")
        self.form_grid.addWidget(self.tax_amount_label)

        self.main_layout.addLayout(self.form_grid)

        # Buttons
        self.buttons_layout = QHBoxLayout()
        self.add_sale_button = QPushButton("Add Sale")
        self.add_sale_button.clicked.connect(self.add_sale)
        self.buttons_layout.addWidget(self.add_sale_button)

        self.clear_button = QPushButton("Clear Form")
        self.clear_button.clicked.connect(self.clear_form)
        self.buttons_layout.addWidget(self.clear_button)

        self.main_layout.addLayout(self.buttons_layout)
        self.setLayout(self.main_layout)

    def load_initial_data(self):
        products = self.db_manager.get_all_products()
        self.product_combo.clear()
        self.product_combo.addItem("Select Product", userData=None)
        for product in products:
            self.product_combo.addItem(f"{product[5]} (SKU: {product[2]})", userData=product[0])

        customers = self.db_manager.get_all_customers()
        self.customer_combo.clear()
        self.customer_combo.addItem("Select Customer", userData=None)
        for customer in customers:
            self.customer_combo.addItem(customer[1], userData=customer[0])

        # Add a dummy customer for testing if none exist
        if not customers:
            self.db_manager.add_customer("Walk-in Customer", "", "", "", "")
            customers = self.db_manager.get_all_customers()
            for customer in customers:
                self.customer_combo.addItem(customer[1], userData=customer[0])

    def update_product_details(self):
        selected_product_id = self.product_combo.currentData()
        if selected_product_id:
            product = self.db_manager.get_product_by_id(selected_product_id)
            if product:
                self.unit_of_measurement_input.setText(product[9])
                self.rate_per_unit_input.setValue(product[8])
                self.tax_percentage_display.setText(f"Tax: {product[7]:.2f}%")
                self.current_product_tax_rate = product[7]
                self.calculate_totals()
        else:
            self.unit_of_measurement_input.clear()
            self.rate_per_unit_input.setValue(0.00)
            self.tax_percentage_display.setText("Tax: 0.00%")
            self.current_product_tax_rate = 0.00
            self.calculate_totals()

    def calculate_totals(self):
        quantity = self.quantity_input.value()
        rate_per_unit = self.rate_per_unit_input.value()
        tax_percentage = getattr(self, 'current_product_tax_rate', 0.00)

        sub_total = quantity * rate_per_unit
        tax_amount = sub_total * (tax_percentage / 100)
        total_rate = sub_total + tax_amount

        self.total_rate_label.setText(f"Total Rate: ${total_rate:.2f}")
        self.tax_amount_label.setText(f"Tax Amount: ${tax_amount:.2f}")

    def add_sale(self):
        sale_date = self.date_input.date().toString("yyyy-MM-dd")
        product_id = self.product_combo.currentData()
        customer_id = self.customer_combo.currentData()
        quantity = self.quantity_input.value()
        unit_of_measurement = self.unit_of_measurement_input.text().strip()
        rate_per_unit = self.rate_per_unit_input.value()

        if not (product_id and customer_id and quantity > 0 and unit_of_measurement and rate_per_unit > 0):
            QMessageBox.warning(self, "Input Error", "Please fill all required fields and ensure quantity/rate are positive.")
            return

        tax_percentage = getattr(self, 'current_product_tax_rate', 0.00)
        sub_total = quantity * rate_per_unit
        tax_amount = sub_total * (tax_percentage / 100)
        total_rate = sub_total + tax_amount

        if self.db_manager.add_sale(sale_date, product_id, customer_id, quantity,
                                      unit_of_measurement, rate_per_unit, total_rate,
                                      tax_amount, self.operator_id):
            QMessageBox.information(self, "Success", "Sale added successfully!")
            self.clear_form()
        else:
            QMessageBox.critical(self, "Error", "Failed to add sale.")

    def clear_form(self):
        self.date_input.setDate(QDate.currentDate())
        self.product_combo.setCurrentIndex(0)
        self.customer_combo.setCurrentIndex(0)
        self.quantity_input.setValue(0.00)
        self.unit_of_measurement_input.clear()
        self.rate_per_unit_input.setValue(0.00)
        self.total_rate_label.setText("Total Rate: $0.00")
        self.tax_amount_label.setText("Tax Amount: $0.00")
        self.tax_percentage_display.setText("Tax: 0.00%")
        self.current_product_tax_rate = 0.00

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sales_form = SalesForm(operator_id=1)
    sales_form.show()
    sys.exit(app.exec())