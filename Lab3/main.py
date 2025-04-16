import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableView, QPushButton, QLineEdit, QDateEdit, QSpinBox,
                             QLabel, QMessageBox, QFileDialog, QComboBox)
from PyQt6.QtCore import QDate, Qt, QAbstractTableModel, QModelIndex
from Cake import Cake
from Cup import Cup
from Belt import Belt
from Product import Product
import datetime

import os.path

class Logger:
    """Manages Exception logging"""
    
    def __init__(self):
        """Initialize a folder for logs"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
    def log_message(self, level: str, message: str, filename = f"{datetime.datetime.now().strftime("%d-%m-%Y")}.log") -> None:
        """
        Log message to a file
        
        Args:
            level (str): DEBUG, ERROR, WARNING...
            message (str): Message to log
            filename (str): Name for log file (currant date as default)
        """
        if not os.path.exists(f"logs/{filename}"):
            with open(f"logs/{filename}", "w") as file:
                file.write(f"{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} {level} {message}\n")
        else:
            with open(f"logs/{filename}", "a") as file:
                file.write(f"{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} {level} {message}\n")

    
class ProductManager:
    """Manages a collection of products"""
    
    def __init__(self):
        """Initialize an empty product list"""
        self.products = []
    
    def add_product(self, product: Product) -> None:
        """
        Add a product to the manager
        
        Args:
            product (Product): Product to add
        """
        self.products.append(product)
    
    def delete_product(self, index: int) -> None:
        """
        Delete a product at the specified index
        
        Args:
            index (int): Product position
        """
        if 0 <= index < len(self.products):
            del self.products[index]
    
    def clear_products(self) -> None:
        """Remove all products from list"""
        self.products = []
    
    def get_products(self) -> list[Product]:
        """Get a copy of product list"""
        return self.products.copy()

class ProductTableModel(QAbstractTableModel):
    """Qt model for displaying products in a table view"""
    
    def __init__(self, product_manager: ProductManager, parent=None):
        """
        Initialize the table model
        
        Args:
            product_manager (ProductManager): Manager containing products to display
            parent: Parent QObject
        """
        super().__init__(parent)
        self.product_manager = product_manager
        self.headers = ["Supply Date", "Name", "Amount", "Special Attribute"]
    
    def columnCount(self, parent=None) -> int:
        """Get number of columns"""
        return len(self.headers)
    
    def rowCount(self, parent=None) -> int:
        """Get number of rows"""
        return len(self.product_manager.get_products())
    
    def data(self, index: QModelIndex, role=Qt.ItemDataRole.DisplayRole) -> str|None:
        """
        Get data of the selected row for display
        
        Args:
            index (QModelIndex): Selected model index
            role (Qt.ItemDataRole): Role of QStandartItem
        
        Returns:
            str|None: Selected field as string or None
        """
        if not index.isValid() or role != Qt.ItemDataRole.DisplayRole:
            return None
        
        product = self.product_manager.get_products()[index.row()]
        
        if index.column() == 0:
            return str(product.supplyDate)
        elif index.column() == 1:
            return product.name
        elif index.column() == 2:
            return str(product.amount)
        elif index.column() == 3:
            if isinstance(product, Belt):
                return str(product.metal)
            elif isinstance(product, Cake):
                return str(product.height)
            elif isinstance(product, Cup):
                return str(product.volume)
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role=Qt.ItemDataRole.DisplayRole) -> str|None:
        """
        Get header data
        
        Args:
            section (int): Selected model section
            orientation (Qt.Orientation): Table orientation (Vertical|Horizontal)
        
        Returns:
            str|None: Selected header as string or None
        """
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.headers[section]
        return None

class ProductFormManager:
    """Manages dynamic form fields for different product types"""
    
    def __init__(self, special_layout: QHBoxLayout):
        """
        Initialize the special fields form manager
        
        Args:
            special_layout (QHBoxLayout): Layout to add special fields to
        """
        self.special_layout = special_layout
        self.special_fields = []
    
    def update_form_fields(self, product_type: str) -> None:
        """
        Update form fields based on product type
        
        Args:
            product_type (str): Name of product type (Ex: Belt, Cake, Cup...)
        """
        self.clear_fields()
        
        if product_type == "Belt":
            self.create_belt_fields()
        elif product_type == "Cake":
            self.create_cake_fields()
        elif product_type == "Cup":
            self.create_cup_fields()
    
    def clear_fields(self) -> None:
        """Clear all special fields items and containers"""
        for i in range(self.special_layout.count()):
            for j in range(self.special_layout.itemAt(i).layout().count()):
                self.special_layout.itemAt(i).layout().itemAt(j).widget().deleteLater()
            self.special_layout.itemAt(i).layout().deleteLater()
        self.special_fields = []
    
    def create_belt_fields(self) -> None:
        """Create fields specific to Belt products"""
        metal_layout = QVBoxLayout()
        metal_layout.addWidget(QLabel("Metal?"))
        metal_select = QComboBox()
        metal_select.addItems(["True", "False"])
        metal_layout.addWidget(metal_select)
        self.special_layout.addLayout(metal_layout)
        self.special_fields = [metal_select]
    
    def create_cake_fields(self) -> None:
        """Create fields specific to Cake products"""
        cake_layout = QVBoxLayout()
        cake_layout.addWidget(QLabel("Height"))
        cake_height = QSpinBox()
        cake_height.setMinimum(5)
        cake_height.setMaximum(1000)
        cake_layout.addWidget(cake_height)
        self.special_layout.addLayout(cake_layout)
        self.special_fields = [cake_height]
    
    def create_cup_fields(self) -> None:
        """Create fields specific to Cup products"""
        cup_layout = QVBoxLayout()
        cup_layout.addWidget(QLabel("Volume"))
        cup_volume = QSpinBox()
        cup_volume.setMinimum(30)
        cup_volume.setMaximum(3000)
        cup_layout.addWidget(cup_volume)
        self.special_layout.addLayout(cup_layout)
        self.special_fields = [cup_volume]
    
    def get_special_field_value(self) -> bool|int|None:
        """
        Get the value from the special field
        
        Returns:
            bool|int|None: Special field value or None
        """
        if self.special_fields:
            if isinstance(self.special_fields[0], QComboBox):
                return bool(self.special_fields[0].currentText())
            elif isinstance(self.special_fields[0], QSpinBox):
                return self.special_fields[0].value()
        return None

class ProductFileHandler:
    """Handles saving and loading products to/from files"""
    
    @staticmethod
    def save_products(products: list[Product], filename: str) -> None:
        """
        Save products to a file
        
        Args:
            products (list[Product]): List of products
            filename (str): Path to file
        """
        with open(filename, 'w') as file:
            for product in products:
                file.write(str(product)+"\n")
    
    @staticmethod
    def load_products(filename: str) -> list[Product]:
        """
        Load products from a file
        
        Args:
            filename (str): Path to file
            
        Returns:
            List[Product]: List of products
        """
        products = []
        with open(filename, 'r') as file:
            for line in file:
                supply_type, values = line.strip().split("(")
                values = values[0:-1].split(", ")
                
                if supply_type == "Belt":
                    products.append(Belt(
                        supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"),
                        name=values[1][1:-1],
                        amount=int(values[2]),
                        metal=(values[3].lower() == "true")
                    ))
                elif supply_type == "Cake":
                    products.append(Cake(
                        supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"),
                        name=values[1][1:-1],
                        amount=int(values[2]),
                        height=int(values[3])
                    ))
                elif supply_type == "Cup":
                    products.append(Cup(
                        supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"),
                        name=values[1][1:-1],
                        amount=int(values[2]),
                        volume=int(values[3])
                    ))
        return products

class ProductWindow(QMainWindow):
    """Main application window for product management"""
    
    def __init__(self):
        """Initialize the main window"""
        super().__init__()
        self.setWindowTitle("Product supply")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize components
        self.product_manager = ProductManager()
        self.file_handler = ProductFileHandler()
        self.logger = Logger()
        
        # Create UI
        self.init_ui()
    
    def init_ui(self) -> None:
        """Initialize the user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create table view
        self.table_view = QTableView()
        self.table_model = ProductTableModel(self.product_manager)
        self.table_view.setModel(self.table_model)
        layout.addWidget(self.table_view)
        
        # Create form
        form_layout = QHBoxLayout()
        
        # Type selection
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Product type:"))
        self.type_select = QComboBox()
        self.type_select.addItems(["Belt", "Cake", "Cup"])
        type_layout.addWidget(self.type_select)
        form_layout.addLayout(type_layout)
        
        # Date input
        date_layout = QVBoxLayout()
        date_layout.addWidget(QLabel("Supply Date:"))
        self.date_edit = QDateEdit(QDate.currentDate())
        date_layout.addWidget(self.date_edit)
        form_layout.addLayout(date_layout)
        
        # Name input
        name_layout = QVBoxLayout()
        name_layout.addWidget(QLabel("Product Name:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        form_layout.addLayout(name_layout)
        
        # Amount input
        amount_layout = QVBoxLayout()
        amount_layout.addWidget(QLabel("Amount:"))
        self.amount_edit = QSpinBox()
        self.amount_edit.setMinimum(1)
        self.amount_edit.setMaximum(99999)
        amount_layout.addWidget(self.amount_edit)
        form_layout.addLayout(amount_layout)
        
        # Special fields container
        self.special_layout = QHBoxLayout()
        form_layout.addLayout(self.special_layout)
        
        # Initialize form manager
        self.form_manager = ProductFormManager(self.special_layout)
        self.type_select.activated.connect(self.on_type_changed)
        self.on_type_changed()  # Initialize with default fields
        
        # Add Product button
        self.add_button = QPushButton("Add Product")
        self.add_button.clicked.connect(self.add_product)
        form_layout.addWidget(self.add_button)
        
        layout.addLayout(form_layout)
        
        # Create button layout
        button_layout = QHBoxLayout()
        
        # Load button
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_products)
        button_layout.addWidget(self.load_button)
        
        # Save button
        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_products)
        button_layout.addWidget(self.save_button)
        
        # Delete button
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_product)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
    
    def on_type_changed(self) -> None:
        """Handle product type selection change"""
        self.form_manager.update_form_fields(self.type_select.currentText())
    
    def add_product(self) -> None:
        """Add a new product based on form data"""
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Warning", "Product name cannot be empty!")
            self.logger.log_message("WARNING", "Tried to add empty named product")
            return
        
        supply_date = datetime.datetime.combine(
            self.date_edit.date().toPyDate(),
            datetime.datetime.min.time()
        )
        amount = self.amount_edit.value()
        special_value = self.form_manager.get_special_field_value()
        
        product_type = self.type_select.currentText()
        if product_type == "Belt":
            product = Belt(supply_date, name, amount, special_value)
        elif product_type == "Cake":
            product = Cake(supply_date, name, amount, special_value)
        else:
            product = Cup(supply_date, name, amount, special_value)
        
        self.product_manager.add_product(product)
        self.table_model.layoutChanged.emit()
    
    def delete_product(self) -> None:
        """Deletes selected product"""
        selected = self.table_view.currentIndex()
        if not selected.isValid():
            QMessageBox.warning(self, "Warning", "Please select a product to delete!")
            self.logger.log_message("WARNING", "Tried remove object from table without selecting any")
            return
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            "Are you sure you want to delete this product?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.product_manager.delete_product(selected.row())
            self.table_model.layoutChanged.emit()
    
    def save_products(self) -> None:
        """Save products to file"""
        filename, _ = QFileDialog.getSaveFileName(
            None, "Save File", ".", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            self.file_handler.save_products(
                self.product_manager.get_products(),
                filename
            )
    
    def load_products(self) -> None:
        """Load products from a file"""
        filename, _ = QFileDialog.getOpenFileName(
            None, "Open File", ".", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                products = self.file_handler.load_products(filename)
                self.product_manager.clear_products()
                for product in products:
                    self.product_manager.add_product(product)
                self.table_model.layoutChanged.emit()
                QMessageBox.information(self, "Success", "Data loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")
                self.logger.log_message("ERROR", f"Failed to load file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(app.exec())