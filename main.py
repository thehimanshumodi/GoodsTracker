import sys
from PySide6.QtWidgets import QApplication
from login_window import LoginWindow
from main_app_window import MainAppWindow
from database_manager import DatabaseManager # Import to ensure DB initialization happens

# Import your actual form classes
from product_master_form import ProductMasterForm
from goods_receiving_form import GoodsReceivingForm
from sales_form import SalesForm

class App(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        self.db_manager = DatabaseManager() # Initialize DB Manager
        self.login_window = LoginWindow()
        self.login_window.login_successful.connect(self.show_main_window)
        self.main_app_window = None # Will be created after login
        self.login_window.show()

    def show_main_window(self, user_info):
        self.main_app_window = MainAppWindow(user_info)
        # Now, replace placeholder forms with actual instances
        if hasattr(self.main_app_window, 'product_master_form'):
            self.main_app_window.stacked_widget.removeWidget(self.main_app_window.product_master_form)
        if hasattr(self.main_app_window, 'goods_receiving_form'):
            self.main_app_window.stacked_widget.removeWidget(self.main_app_window.goods_receiving_form)
        if hasattr(self.main_app_window, 'sales_form'):
            self.main_app_window.stacked_widget.removeWidget(self.main_app_window.sales_form)

        product_master_form = ProductMasterForm(user_info['id'])
        self.main_app_window.stacked_widget.addWidget(product_master_form)

        goods_receiving_form = GoodsReceivingForm(user_info['id'])
        self.main_app_window.stacked_widget.addWidget(goods_receiving_form)

        sales_form = SalesForm(user_info['id'])
        self.main_app_window.stacked_widget.addWidget(sales_form)

        # Set initial view to Product Master (or any default)
        self.main_app_window.stacked_widget.setCurrentWidget(product_master_form)

        self.main_app_window.logout_requested.connect(self.handle_logout)
        self.main_app_window.show()

    def handle_logout(self):
        if self.main_app_window:
            self.main_app_window.close()
            self.main_app_window = None
        self.login_window = LoginWindow() # Recreate login window
        self.login_window.login_successful.connect(self.show_main_window)
        self.login_window.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
    