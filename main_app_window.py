import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QToolBar, QMessageBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction

# Import your form classes (will be created in subsequent steps)
# from goods_receiving_form import GoodsReceivingForm
# from sales_form import SalesForm
# from product_master_form import ProductMasterForm
# from database_manager import DatabaseManager # Import if needed for logout/session management

class MainAppWindow(QMainWindow):
    logout_requested = Signal() # Signal to handle logout

    def __init__(self, user_info):
        super().__init__()
        self.user_info = user_info
        self.setWindowTitle(f"Inventory Management System - Logged in as {user_info['username']}")
        self.setGeometry(100, 100, 1000, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.stacked_widget = QStackedWidget()
        self.main_layout.addWidget(self.stacked_widget)

        self._create_toolbar()
        self._setup_forms()

    def _create_toolbar(self):
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False) # Prevent toolbar from being moved

        # Product Master Action
        self.product_master_action = QAction("Product Master", self)
        self.product_master_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        toolbar.addAction(self.product_master_action)

        # Goods Receiving Action
        self.goods_receiving_action = QAction("Goods Receiving", self)
        self.goods_receiving_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        toolbar.addAction(self.goods_receiving_action)

        # Sales Action
        self.sales_action = QAction("Sales", self)
        self.sales_action.triggered.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        toolbar.addAction(self.sales_action)

        toolbar.addSeparator()

        # Logout Action
        self.logout_action = QAction("Logout", self)
        self.logout_action.triggered.connect(self._request_logout)
        toolbar.addAction(self.logout_action)

    def _setup_forms(self):
        # Placeholder forms for now
        # You will replace these with actual instances of your form classes
        self.product_master_form = QLabel("Product Master Form Content Here")
        self.product_master_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stacked_widget.addWidget(self.product_master_form)

        self.goods_receiving_form = QLabel("Goods Receiving Form Content Here")
        self.goods_receiving_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stacked_widget.addWidget(self.goods_receiving_form)

        self.sales_form = QLabel("Sales Form Content Here")
        self.sales_form.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stacked_widget.addWidget(self.sales_form)

        # Example of how you would initialize real forms:
        # self.product_master_form = ProductMasterForm(self.user_info['id'])
        # self.stacked_widget.addWidget(self.product_master_form)
        # self.goods_receiving_form = GoodsReceivingForm(self.user_info['id'])
        # self.stacked_widget.addWidget(self.goods_receiving_form)
        # self.sales_form = SalesForm(self.user_info['id'])
        # self.stacked_widget.addWidget(self.sales_form)

    def _request_logout(self):
        reply = QMessageBox.question(self, "Logout", "Are you sure you want to log out?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.logout_requested.emit()
            self.close()

# For testing the main app window directly
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Simulate a successful login for testing
    dummy_user = {'id': 1, 'username': 'test_operator', 'role': 'operator'}
    main_window = MainAppWindow(dummy_user)
    main_window.show()
    sys.exit(app.exec())