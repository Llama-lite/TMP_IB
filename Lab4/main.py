import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableView, QPushButton, QLineEdit, QDateEdit, QSpinBox,
                             QLabel, QMessageBox, QFileDialog, QComboBox)
from PyQt6.QtCore import QDate, Qt, QAbstractTableModel, QModelIndex
from Cake import Cake
from Cup import Cup
from Belt import Belt
from Product import Product
from datetime import datetime, date, timedelta
import re

import os.path

# TODO: add unittests for new functions and class
class Logger:
    """Manages Exception logging"""
    
    def __init__(self):
        """Initialize a folder for logs"""
        if not os.path.exists('logs'):
            os.makedirs('logs')
        
    def log_message(self, level: str, message: str, filename = f"{datetime.now().strftime("%d-%m-%Y")}.log") -> None:
        """
        Log message to a file
        
        Args:
            level (str): DEBUG, ERROR, WARNING...
            message (str): Message to log
            filename (str): Name for log file (currant date as default)
        """
        if not os.path.exists(f"logs/{filename}"):
            with open(f"logs/{filename}", "w") as file:
                file.write(f"{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} {level} {message}\n")
        else:
            with open(f"logs/{filename}", "a") as file:
                file.write(f"{datetime.now().strftime("%d-%m-%Y %H:%M:%S")} {level} {message}\n")
 
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
    
    def remove_by_range(self, field: str, range_min: int|datetime, range_max: int|datetime) -> None:
        """
        Remove products with field value in selected range [start, end]
        
        Args:
            field (str): Desired field to equation (Ex: supplyDate, amount...)
            range_min (int|datetime): Start of the range
            range_max (int|datetime): End of the range
        """
        i = 0
        while i < len(self.products):
            if field == "amount" and range_min <= self.products[i].amount <= range_max:
                self.delete_product(i)
            elif field == "supplyDate" and range_min <= self.products[i].supplyDate <= range_max: 
                self.delete_product(i)
            elif field == "special":
                if isinstance(self.products[i], Cake) and range_min <= self.products[i].height <= range_max:
                    self.delete_product(i)
                elif isinstance(self.products[i], Cup) and range_min <= self.products[i].volume <= range_max:
                    self.delete_product(i)
                else:
                    i += 1
            else:
                i += 1
    
    def remove_equal(self, field: str, value: str, is_equal: bool) -> None:
        """
        Remove products with field value equal to desired value
        
        Args:
            field (str): Desired field to equation (Ex: supplyDate, amount...)
            value (str): Value for equation
            is_equal (bool): Should the field be equal to value or not
        """
        i = 0
        while i < len(self.products):
            if field == "name" and ((self.products[i].name == value and is_equal) or (self.products[i].name != value and not is_equal)):
                self.delete_product(i)
            elif field == "supplyDate" and ((str(self.products[i].supplyDate) == value and is_equal) or (str(self.products[i].supplyDate) != value and not is_equal)): 
                self.delete_product(i)
            elif field == "amount" and ((str(self.products[i].amount) == value and is_equal) or (str(self.products[i].amount) != value and not is_equal)):
                self.delete_product(i)
            elif field == "special":
                if isinstance(self.products[i], Cake) and ((str(self.products[i].height) == value and is_equal) or (str(self.products[i].height) != value and not is_equal)):
                    self.delete_product(i)
                elif isinstance(self.products[i], Cup) and ((str(self.products[i].volume) == value and is_equal) or (str(self.products[i].volume) != value and not is_equal)):
                    self.delete_product(i)
                elif isinstance(self.products[i], Belt) and ((str(self.products[i].metal) == value and is_equal) or (str(self.products[i].metal) != value and not is_equal)):
                    self.delete_product(i)
                else:
                    i += 1
            else:
                i += 1
    
    def remove_by_inequality(self, field: str, value: int|datetime, is_greater: bool) -> None:
        """
        Remove products with field value below equal or greater equal than desired value
        
        Args:
            field (str): Desired field to equation (Ex: supplyDate, amount...)
            value (int|datetime): Value for equation
            is_greater (bool): Should the field be greater than value or not
        """
        i = 0
        while i < len(self.products):
            if field == "amount" and ((self.products[i].amount >= value and is_greater) or (self.products[i].amount <= value and not is_greater)):
                self.delete_product(i)
            elif field == "supplyDate" and ((self.products[i].supplyDate >= value and is_greater) or (self.products[i].supplyDate <= value and not is_greater)):
                self.delete_product(i)
            elif field == "special":
                if isinstance(self.products[i], Cake) and ((self.products[i].height >= value and is_greater) or (self.products[i].height <= value and not is_greater)):
                    self.delete_product(i)
                elif isinstance(self.products[i], Cup) and ((self.products[i].volume >= value and is_greater) or (self.products[i].volume <= value and not is_greater)):
                    self.delete_product(i)
                else:
                    i += 1
            else:
                i += 1
                    
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
                        supplyDate=datetime.strptime(values[0], "%d.%m.%Y"),
                        name=values[1][1:-1],
                        amount=int(values[2]),
                        metal=(values[3].lower() == "true")
                    ))
                elif supply_type == "Cake":
                    products.append(Cake(
                        supplyDate=datetime.strptime(values[0], "%d.%m.%Y"),
                        name=values[1][1:-1],
                        amount=int(values[2]),
                        height=int(values[3])
                    ))
                elif supply_type == "Cup":
                    products.append(Cup(
                        supplyDate=datetime.strptime(values[0], "%d.%m.%Y"),
                        name=values[1][1:-1],
                        amount=int(values[2]),
                        volume=int(values[3])
                    ))
        return products

class CommandProcessor:
    """Handles processing of command files following SRP"""
    
    def __init__(self, product_manager: ProductManager, file_handler: ProductFileHandler, logger: Logger):
        """
        First call initialization
        
        Args:
            product_manager (ProductManager): Instance of ProductManager in use
            logger (Logger): Instance of Logger in use
        """
        self.product_manager = product_manager
        self.logger = logger
        self.file_handler = file_handler
    
    def process_command_file(self, filename: str) -> None:
        """
        Process a command file line by line
        
        Args:
            filename (str): Path to file
        """
        try:
            with open(filename, 'r') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    
                    if not line or line.startswith('#'):
                        continue
                    
                    try:
                        if line.startswith('ADD'):
                            self._process_add_command(line[4:].strip())
                        elif line.startswith('REM'):
                            self._process_remove_command(line[4:].strip())
                        elif line.startswith('SAVE'):
                            self._process_save_command(line[5:].strip())
                        else:
                            self.logger.log_message("WARNING", f"Unknown command at line {line_num}: {line}")
                    except Exception as e:
                        self.logger.log_message("ERROR", f"Failed processing line {line_num}: {line}. Error: {str(e)}")
                        raise
        except FileNotFoundError:
            self.logger.log_message("ERROR", f"Command file not found: {filename}")
        except Exception as e:
            self.logger.log_message("ERROR", f"Failed to process command file: {str(e)}")
    
    def _process_add_command(self, data: str) -> None:
        """
        Process ADD command
        
        Args:
            data (str): New product data in csv format
        """
        parts = [p.strip() for p in data.split(';')]
        if len(parts) < 5:
            raise ValueError("Invalid ADD command format")
        
        product_type = parts[0]
        date = datetime.strptime(parts[1], "%d.%m.%Y")
        name = parts[2]
        amount = int(parts[3])
        special = parts[4]
        
        if product_type == "Belt":
            special = bool(special)
            product = Belt(date, name, amount, special)
        elif product_type == "Cake":
            special = int(special)
            product = Cake(date, name, amount, special)
        elif product_type == "Cup":
            special = int(special)
            product = Cup(date, name, amount, special)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
        
        self.product_manager.add_product(product)
    
    def _process_remove_command(self, condition: str) -> None:
        """
        Process REM command
        
        Args:
            condition (str): Condition for removing (Ex: field < 100)
        """
        # Handle range condition (e.g., "100 <= amount <= 300")
        range_match = re.match(r"(.+) (<=|<) (supplyDate|amount|special) (<=|<) (.+)", condition)
        if range_match:
            sign_start = range_match.group(2)
            sign_end = range_match.group(4)
            field = range_match.group(3)
            if field == "supplyDate":
                try:
                    range_min = date.fromisoformat(range_match.group(1))
                    range_max = date.fromisoformat(range_match.group(5))
                    if sign_start == "<":
                        range_min += timedelta(microseconds=1)
                    if sign_end == "<":
                        range_max -= timedelta(microseconds=1)
                    if range_min > range_max:
                        raise ValueError(f"Incorrect condition min/max values: {range_min} > {range_max}")
                    self.product_manager.remove_by_range(field, range_min, range_max)
                except:
                    raise ValueError(f"Incorrect special field value. Only dates and integers are supported.")
            else:
                try:
                    range_min = int(range_match.group(1))
                    range_max = int(range_match.group(5))
                    if sign_start == "<":
                        range_min += 1
                    if sign_end == "<":
                        range_max -= 1
                    if range_min > range_max:
                        raise ValueError(f"Incorrect condition min/max values: {range_min} > {range_max}")
                    self.product_manager.remove_by_range(field, range_min, range_max)
                except:
                    raise ValueError(f"Incorrect special field value. Only dates and integers are supported: {range_match.group(1)}, {range_match.group(5)}")
            return

        # Handle equal condition (e.g., "name = Test name")
        equal_match = re.match(r"(supplyDate|name|amount|special) (=|!=) (.+)", condition)
        if equal_match:
            field = equal_match.group(1)
            is_equal = equal_match.group(2) == "="
            value = equal_match.group(3)
            self.product_manager.remove_equal(field, value, is_equal)
            return
        
        # Handle greater or below condition (e.g., "amount > 100")
        inequality_match = re.match(r"(supplyDate|amount|special) (<=|>=|<|>) (.+)", condition)
        if inequality_match:
            field = inequality_match.group(1)
            sign = inequality_match.group(2)
            if sign.startswith("<"):
                is_greater = False
            else:
                is_greater = True
            if field == "supplyDate":
                try:
                    value = date.fromisoformat(inequality_match.group(3))
                    if sign == "<":
                        value -= timedelta(microseconds=1)
                    elif sign == ">":
                        value += timedelta(microseconds=1)
                    self.product_manager.remove_by_inequality(field, value, is_greater)
                except:
                    raise ValueError(f"Incorrect special field value. Only dates and integers are supported.")
            else:
                try:
                    value = int(inequality_match.group(3))
                    if sign == "<":
                        value -= 1
                    if sign == ">":
                        value += 1
                    self.product_manager.remove_by_inequality(field, value, is_greater)
                except:
                    raise ValueError(f"Incorrect special field value. Only dates and integers are supported.")
            return
        raise ValueError(f"Unsupported REM condition: {condition}")
    
    def _process_save_command(self, filename: str) -> None:
        """Process SAVE command"""
        self.file_handler.save_products(self.product_manager.get_products(), filename)

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
        
        # Load data button
        self.load_button = QPushButton("Load Data")
        self.load_button.clicked.connect(self.load_products)
        button_layout.addWidget(self.load_button)
        
        # Save data button
        self.save_button = QPushButton("Save Data")
        self.save_button.clicked.connect(self.save_products)
        button_layout.addWidget(self.save_button)
        
        # Delete selected button
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_product)
        button_layout.addWidget(self.delete_button)
        
        # Load scenario button
        self.scenario_button = QPushButton("Load scenario")
        self.scenario_button.clicked.connect(self.load_scenario)
        button_layout.addWidget(self.scenario_button)
        
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
        
        supply_date = datetime.combine(
            self.date_edit.date().toPyDate(),
            datetime.min.time()
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

    def load_scenario(self) -> None:
        """Load scenario from a file and executes it"""
        filename, _ = QFileDialog.getOpenFileName(
            None, "Open File", ".", "Text Files (*.txt);;All Files (*)"
        )
        if filename:
            scenario = CommandProcessor(self.product_manager, self.file_handler, self.logger)
            scenario.process_command_file(filename)
            self.table_model.layoutChanged.emit()
            QMessageBox.information(self, "Info", "Comands executed")
            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(app.exec())