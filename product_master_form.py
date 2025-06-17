import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QPushButton, QLabel, QDoubleSpinBox,
                               QTextEdit, QComboBox, QFileDialog, QTableView,
                               QHeaderView, QMessageBox, QAbstractItemView)
from PySide6.QtGui import QPixmap, QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, Signal
import os
from database_manager import DatabaseManager

class ProductMasterForm(QWidget):
    def __init__(self, operator_id):
        super().__init__()
        self.operator_id = operator_id
        self.db_manager = DatabaseManager()
        self.current_product_id = None # To track which product is being edited
        self.init_ui()
        self.load_products()

    def init_ui(self):
        self.setWindowTitle("Product Master List")
        self.main_layout = QVBoxLayout()

        # Input Fields
        self.form_layout = QHBoxLayout()
        self.fields_layout = QVBoxLayout()

        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Barcode")
        self.fields_layout.addWidget(QLabel("Barcode:"))
        self.fields_layout.addWidget(self.barcode_input)

        self.sku_id_input = QLineEdit()
        self.sku_id_input.setPlaceholderText("SKU ID (Required)")
        self.fields_layout.addWidget(QLabel("SKU ID:"))
        self.fields_layout.addWidget(self.sku_id_input)

        self.product_name_input = QLineEdit()
        self.product_name_input.setPlaceholderText("Product Name (Required)")
        self.fields_layout.addWidget(QLabel("Product Name:"))
        self.fields_layout.addWidget(self.product_name_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")
        self.fields_layout.addWidget(QLabel("Category:"))
        self.fields_layout.addWidget(self.category_input)

        self.subcategory_input = QLineEdit()
        self.subcategory_input.setPlaceholderText("Subcategory")
        self.fields_layout.addWidget(QLabel("Subcategory:"))
        self.fields_layout.addWidget(self.subcategory_input)

        self.price_input = QDoubleSpinBox()
        self.price_input.setPrefix("$")
        self.price_input.setRange(0.00, 999999.99)
        self.price_input.setDecimals(2)
        self.fields_layout.addWidget(QLabel("Price:"))
        self.fields_layout.addWidget(self.price_input)

        self.tax_percentage_input = QDoubleSpinBox()
        self.tax_percentage_input.setSuffix("%")
        self.tax_percentage_input.setRange(0.00, 100.00)
        self.tax_percentage_input.setDecimals(2)
        self.fields_layout.addWidget(QLabel("Tax Percentage:"))
        self.fields_layout.addWidget(self.tax_percentage_input)

        self.default_unit_input = QLineEdit()
        self.default_unit_input.setPlaceholderText("e.g., Pcs, Kg, Liters")
        self.fields_layout.addWidget(QLabel("Default Unit:"))
        self.fields_layout.addWidget(self.default_unit_input)

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Product Description")
        self.fields_layout.addWidget(QLabel("Description:"))
        self.fields_layout.addWidget(self.description_input)

        self.form_layout.addLayout(self.fields_layout)

        # Image selection
        self.image_layout = QVBoxLayout()
        self.image_label = QLabel("No Image Selected")
        self.image_label.setFixedSize(200, 200) # Fixed size for image display
        self.image_label.setStyleSheet("border: 1px solid gray;")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_path = "" # To store the path
        self.image_layout.addWidget(self.image_label)

        self.upload_image_button = QPushButton("Upload Image")
        self.upload_image_button.clicked.connect(self.upload_image)
        self.image_layout.addWidget(self.upload_image_button)

        self.form_layout.addLayout(self.image_layout)
        self.main_layout.addLayout(self.form_layout)

        # Buttons
        self.buttons_layout = QHBoxLayout()
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)
        self.buttons_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Update Product")
        self.update_button.clicked.connect(self.update_product)
        self.update_button.setEnabled(False) # Initially disabled
        self.buttons_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Delete Product")
        self.delete_button.clicked.connect(self.delete_product)
        self.delete_button.setEnabled(False) # Initially disabled
        self.buttons_layout.addWidget(self.delete_button)

        self.clear_button = QPushButton("Clear Form")
        self.clear_button.clicked.connect(self.clear_form)
        self.buttons_layout.addWidget(self.clear_button)

        self.main_layout.addLayout(self.buttons_layout)

        # Product Table
        self.product_table = QTableView()
        self.product_model = QStandardItemModel()
        self.product_table.setModel(self.product_model)
        self.product_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.product_table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.product_table.clicked.connect(self.load_product_into_form)
        self.main_layout.addWidget(self.product_table)
        self.setLayout(self.main_layout)

    def upload_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Product Image", "", "Image Files (*.png *.jpg *.jpeg *.gif)")
        if file_name:
            self.image_path = file_name
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.image_label.setText("") # Clear "No Image Selected"

    def clear_form(self):
        self.barcode_input.clear()
        self.sku_id_input.clear()
        self.product_name_input.clear()
        self.category_input.clear()
        self.subcategory_input.clear()
        self.description_input.clear()
        self.price_input.setValue(0.00)
        self.tax_percentage_input.setValue(0.00)
        self.default_unit_input.clear()
        self.image_path = ""
        self.image_label.setText("No Image Selected")
        self.image_label.setPixmap(QPixmap()) # Clear any loaded image
        self.current_product_id = None
        self.add_button.setEnabled(True)
        self.update_button.setEnabled(False)
        self.delete_button.setEnabled(False)
        self.product_table.clearSelection()

    def add_product(self):
        barcode = self.barcode_input.text().strip()
        sku_id = self.sku_id_input.text().strip()
        product_name = self.product_name_input.text().strip()
        category = self.category_input.text().strip()
        subcategory = self.subcategory_input.text().strip()
        description = self.description_input.toPlainText().strip()
        price = self.price_input.value()
        tax_percentage = self.tax_percentage_input.value()
        default_unit = self.default_unit_input.text().strip()

        if not sku_id or not product_name:
            QMessageBox.warning(self, "Input Error", "SKU ID and Product Name are required.")
            return

        if self.db_manager.add_product(barcode, sku_id, category, subcategory, product_name,
                                       description, tax_percentage, price, default_unit, self.image_path):
            QMessageBox.information(self, "Success", "Product added successfully!")
            self.clear_form()
            self.load_products()
        else:
            QMessageBox.critical(self, "Error", "Failed to add product. SKU ID or Barcode might already exist.")

    def load_products(self):
        products = self.db_manager.get_all_products()
        self.product_model.clear()
        headers = ["ID", "Barcode", "SKU ID", "Category", "Subcategory", "Product Name",
                   "Description", "Tax %", "Price", "Default Unit", "Image Path"]
        self.product_model.setHorizontalHeaderLabels(headers)

        for row_idx, product in enumerate(products):
            for col_idx, data in enumerate(product):
                item = QStandardItem(str(data))
                item.setEditable(False) # Make cells non-editable directly in the table
                self.product_model.setItem(row_idx, col_idx, item)

        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # Stretch columns

    def load_product_into_form(self, index):
        row = index.row()
        product_data = []
        for col in range(self.product_model.columnCount()):
            product_data.append(self.product_model.item(row, col).text())

        self.current_product_id = int(product_data[0]) # ID is the first column
        self.barcode_input.setText(product_data[1])
        self.sku_id_input.setText(product_data[2])
        self.category_input.setText(product_data[3])
        self.subcategory_input.setText(product_data[4])
        self.product_name_input.setText(product_data[5])
        self.description_input.setText(product_data[6])
        self.tax_percentage_input.setValue(float(product_data[7]))
        self.price_input.setValue(float(product_data[8]))
        self.default_unit_input.setText(product_data[9])
        self.image_path = product_data[10] # Image path is the last column

        if self.image_path and os.path.exists(self.image_path):
            pixmap = QPixmap(self.image_path)
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
            self.image_label.setText("")
        else:
            self.image_label.setText("No Image Selected")
            self.image_label.setPixmap(QPixmap())

        self.add_button.setEnabled(False)
        self.update_button.setEnabled(True)
        self.delete_button.setEnabled(True)

    def update_product(self):
        if self.current_product_id is None:
            QMessageBox.warning(self, "Selection Error", "Please select a product to update.")
            return

        barcode = self.barcode_input.text().strip()
        sku_id = self.sku_id_input.text().strip()
        product_name = self.product_name_input.text().strip()
        category = self.category_input.text().strip()
        subcategory = self.subcategory_input.text().strip()
        description = self.description_input.toPlainText().strip()
        price = self.price_input.value()
        tax_percentage = self.tax_percentage_input.value()
        default_unit = self.default_unit_input.text().strip()

        if not sku_id or not product_name:
            QMessageBox.warning(self, "Input Error", "SKU ID and Product Name are required.")
            return

        if self.db_manager.update_product(self.current_product_id, barcode, sku_id, category, subcategory,
                                          product_name, description, tax_percentage, price, default_unit, self.image_path):
            QMessageBox.information(self, "Success", "Product updated successfully!")
            self.clear_form()
            self.load_products()
        else:
            QMessageBox.critical(self, "Error", "Failed to update product. SKU ID or Barcode might already exist.")

    def delete_product(self):
        if self.current_product_id is None:
            QMessageBox.warning(self, "Selection Error", "Please select a product to delete.")
            return

        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this product?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            if self.db_manager.delete_product(self.current_product_id):
                QMessageBox.information(self, "Success", "Product deleted successfully!")
                self.clear_form()
                self.load_products()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete product.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Simulate an operator ID for testing
    product_master_form = ProductMasterForm(operator_id=1)
    product_master_form.show()
    sys.exit(app.exec())