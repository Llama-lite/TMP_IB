import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QTableView, QPushButton, QLineEdit, QDateEdit, QSpinBox,
                             QLabel, QMessageBox, QFileDialog, QComboBox)
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtGui import QStandardItemModel, QStandardItem
from Cake import Cake
from Cup import Cup
from Belt import Belt
import datetime


# Main window class
class ProductWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product supply")
        self.setGeometry(100, 100, 800, 600)
        
        self.products = []  # For Product children objects
        self.special_fields = [] # For special class fields
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create table view and model
        self.table_view = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Supply Date", "Name", "Amount", '*'])
        self.table_view.setModel(self.model)
        layout.addWidget(self.table_view)
        
        # Create form for adding new products
        form_layout = QHBoxLayout()
        
        # Type input
        type_layout = QVBoxLayout()
        type_layout.addWidget(QLabel("Product type:"))
        self.type_select = QComboBox()
        self.type_select.addItems(["Belt", "Cake", "Cup"])
        self.type_select.activated.connect(self.selected_type_changed)
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
        
        # Container for special class fields
        self.special_layout = QHBoxLayout()
        form_layout.addLayout(self.special_layout)
        
        # Container Belt fields (as it is first selected)
        metal_layout = QVBoxLayout()
        metal_layout.addWidget(QLabel("Metal?"))
        metal_select = QComboBox()
        metal_select.addItems(["True", "False"])
        metal_layout.addWidget(metal_select)
        self.special_layout.addLayout(metal_layout)
        self.special_fields = [metal_select]
        
        # Add button
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
    
    
    # Add new product to the list and update table
    def add_product(self):
        supplyDate = datetime.datetime.combine(self.date_edit.date().toPyDate(), datetime.datetime.min.time())
        name = self.name_edit.text().strip()
        ammount = self.amount_edit.value()
        
        if not name:
            QMessageBox.warning(self, "Warning", "Product name cannot be empty!")
            return
        
        if self.type_select.currentText() == "Belt":
            self.products.append(Belt(supplyDate, name, ammount, bool(self.special_fields[0].currentText())))
        elif self.type_select.currentText() == "Cake":
            self.products.append(Cake(supplyDate, name, ammount, bool(self.special_fields[0].value())))
        else:
            self.products.append(Cup(supplyDate, name, ammount, bool(self.special_fields[0].value())))
        
        self.update_table()
    
    
    # Delete selected product from table and file
    def delete_product(self):
        selected = self.table_view.currentIndex()
        if not selected.isValid():
            QMessageBox.warning(self, "Warning", "Please select a product to delete!")
            return
        
        # Confirm deletion
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            "Are you sure you want to delete this product?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            row = selected.row()
            del self.products[row]
            self.update_table()
    
    
    # Change UI based on selected product type
    def selected_type_changed(self):
        selected = self.type_select.currentText()
        
        for i in range(self.special_layout.count()):
            container = self.special_layout.itemAt(i)
            for j in range(container.count()):
                container.itemAt(j).widget().deleteLater()
            container.layout().deleteLater()
        
        if selected == "Belt":
            metal_layout = QVBoxLayout()
            metal_layout.addWidget(QLabel("Metal?"))
            metal_select = QComboBox()
            metal_select.addItems(["True", "False"])
            metal_layout.addWidget(metal_select)
            self.special_layout.addLayout(metal_layout)
            self.special_fields = [metal_select]
        elif selected == "Cake":
            cake_layout = QVBoxLayout()
            cake_layout.addWidget(QLabel("Height"))
            cake_height = QSpinBox()
            cake_height.setMinimum(5)
            cake_height.setMaximum(1000)
            cake_layout.addWidget(cake_height)
            self.special_layout.addLayout(cake_layout)
            self.special_fields = [cake_height]
        elif selected == "Cup":
            cup_layout = QVBoxLayout()
            cup_layout.addWidget(QLabel("Volume"))
            cup_volume = QSpinBox()
            cup_volume.setMinimum(30)
            cup_volume.setMaximum(3000)
            cup_layout.addWidget(cup_volume)
            self.special_layout.addLayout(cup_layout)
            self.special_fields = [cup_volume]
        ...
    
    # Update visual grid table items
    def update_table(self):
        self.model.clear()
        self.model.setHorizontalHeaderLabels(["Supply Date", "Name", "Amount", "*"])
        
        for product in self.products:
            date_item = QStandardItem(str(product.supplyDate))
            name_item = QStandardItem(product.name)
            amount_item = QStandardItem(str(product.ammount))
            
            if isinstance(product, Belt):
                metal_item = QStandardItem(str(product.metal))
                self.model.appendRow([date_item, name_item, amount_item, metal_item])
            elif isinstance(product, Cake):
                height_item = QStandardItem(str(product.height))
                self.model.appendRow([date_item, name_item, amount_item, height_item])
            elif isinstance(product, Cup):
                volume_item = QStandardItem(str(product.volume))
                self.model.appendRow([date_item, name_item, amount_item, volume_item])
    
    
    # Save data to selected file
    def save_products(self):
        filename, _ = QFileDialog.getSaveFileName(None, "Save File", ".", "Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, 'w') as file:
                for product in self.products:
                    file.write(str(product)+"\n")
    
    
    # Load data from file
    def load_products(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Save File", ".", "Text Files (*.txt);;All Files (*)")
        if filename:
            products = []
            with open(filename, 'r') as file:
                for line in file:
                    supply_type, values = line.strip().split("(")
                    values = values[0:-1].split(", ")
                    
                    if supply_type == "Belt":
                        products.append(Belt(supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"), name=values[1][1:-1], ammount=int(values[2]), metal=(values[3].lower() == "true")))
                    
                    elif supply_type == "Cake":
                        products.append(Cake(supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"), name=values[1][1:-1], ammount=int(values[2]), height=int(values[3])))
                    
                    elif supply_type == "Cup":
                        products.append(Cup(supplyDate=datetime.datetime.strptime(values[0], "%d.%m.%Y"), name=values[1][1:-1], ammount=int(values[2]), volume=int(values[3])))
            
            self.products = products
            self.update_table()
            QMessageBox.information(self, "Success", "Data loaded successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProductWindow()
    window.show()
    sys.exit(app.exec())