import unittest
import sys
import os
import datetime
from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QApplication, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt

from Belt import Belt
from Cake import Cake
from Cup import Cup

from main import (
    ProductManager,
    ProductTableModel,
    ProductFormManager,
    ProductFileHandler,
    ProductWindow
)

app = QApplication(sys.argv)

class TestChildClasses(unittest.TestCase):
    def setUp(self):
        self.sample_belt = Belt(datetime.datetime(2023, 1, 1), "Belt", 10, True)
        self.sample_cake = Cake(datetime.datetime(2023, 1, 1), "Cake", 5, 15)
        self.sample_cup = Cup(datetime.datetime(2023, 1, 1), "Cup", 20, 250)
    
    def test_product_as_string(self):
        self.assertEqual(str(self.sample_belt), "Belt(01.01.2023, \"Belt\", 10, True)")
        self.assertEqual(str(self.sample_cake), "Cake(01.01.2023, \"Cake\", 5, 15)")
        self.assertEqual(str(self.sample_cup), "Cup(01.01.2023, \"Cup\", 20, 250)")

class TestProductManager(unittest.TestCase):
    def setUp(self):
        self.manager = ProductManager()
        self.sample_belt = Belt(datetime.datetime.now(), "Belt", 10, True)
        self.sample_cake = Cake(datetime.datetime.now(), "Cake", 5, 15)
        self.sample_cup = Cup(datetime.datetime.now(), "Cup", 20, 250)

    def test_add_product(self):
        self.manager.add_product(self.sample_belt)
        self.assertEqual(len(self.manager.products), 1)
        self.assertIsInstance(self.manager.products[0], Belt)

    def test_delete_product(self):
        self.manager.add_product(self.sample_belt)
        self.manager.add_product(self.sample_cake)
        self.manager.delete_product(0)
        self.assertEqual(len(self.manager.products), 1)
        self.assertIsInstance(self.manager.products[0], Cake)

    def test_clear_products(self):
        self.manager.add_product(self.sample_belt)
        self.manager.add_product(self.sample_cup)
        self.manager.clear_products()
        self.assertEqual(len(self.manager.products), 0)

    def test_get_products(self):
        self.manager.add_product(self.sample_belt)
        products = self.manager.get_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].name, "Belt")

class TestProductTableModel(unittest.TestCase):
    def setUp(self):
        self.manager = ProductManager()
        self.model = ProductTableModel(self.manager)
        self.sample_belt = Belt(datetime.datetime.now(), "Belt", 10, True)
        self.sample_cake = Cake(datetime.datetime.now(), "Cake", 5, 15)
        self.sample_cup = Cup(datetime.datetime.now(), "Cup", 20, 250)

    def test_row_count(self):
        self.assertEqual(self.model.rowCount(), 0)
        self.manager.add_product(self.sample_belt)
        self.assertEqual(self.model.rowCount(), 1)

    def test_column_count(self):
        self.assertEqual(self.model.columnCount(), 4)

    def test_data_display(self):
        self.manager.add_product(self.sample_belt)
        index = self.model.index(0, 1)
        self.assertEqual(self.model.data(index), "Belt")
        
        index = self.model.index(0, 2)
        self.assertEqual(self.model.data(index), "10")
        
        index = self.model.index(0, 3)
        self.assertEqual(self.model.data(index), "True")

    def test_header_data(self):
        self.assertEqual(self.model.headerData(0, Qt.Orientation.Horizontal), "Supply Date")
        self.assertEqual(self.model.headerData(1, Qt.Orientation.Horizontal), "Name")
        self.assertEqual(self.model.headerData(2, Qt.Orientation.Horizontal), "Amount")
        self.assertEqual(self.model.headerData(3, Qt.Orientation.Horizontal), "Special Attribute")

class TestProductFormManager(unittest.TestCase):
    def setUp(self):
        self.mock_layout = MagicMock()
        self.form_manager = ProductFormManager(self.mock_layout)

    def test_update_form_fields_belt(self):
        self.form_manager.update_form_fields("Belt")
        self.assertEqual(len(self.form_manager.special_fields), 1)
        
    def test_update_form_fields_cake(self):
        self.form_manager.update_form_fields("Cake")
        self.assertEqual(len(self.form_manager.special_fields), 1)
        
    def test_update_form_fields_cup(self):
        self.form_manager.update_form_fields("Cup")
        self.assertEqual(len(self.form_manager.special_fields), 1)

    @patch('PyQt6.QtWidgets.QComboBox', autospec=True)
    @patch('PyQt6.QtWidgets.QSpinBox', autospec=True)
    def test_get_special_field_value(self, mock_spin, mock_combo):
        mock_spin.value.return_value = 2
        self.form_manager.special_fields = [mock_spin]
        self.assertEqual(self.form_manager.get_special_field_value(), 2)
        
        mock_combo.currentText.return_value = False
        self.form_manager.special_fields = [mock_combo]
        self.assertFalse(self.form_manager.get_special_field_value())

class TestProductFileHandler(unittest.TestCase):
    def setUp(self):
        self.temp_file = "temp_test_file.txt"
        self.sample_belt = Belt(datetime.datetime(2023, 1, 1), "Belt", 10, True)
        self.sample_cake = Cake(datetime.datetime(2023, 1, 1), "Cake", 5, 15)
        self.sample_cup = Cup(datetime.datetime(2023, 1, 1), "Cup", 20, 250)

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)

    def test_save_and_load_products(self):
        products = [self.sample_belt, self.sample_cake, self.sample_cup]
        ProductFileHandler.save_products(products, self.temp_file)
        
        loaded_products = ProductFileHandler.load_products(self.temp_file)
        self.assertEqual(len(loaded_products), 3)
        
        self.assertIsInstance(loaded_products[0], Belt)
        self.assertEqual(loaded_products[0].name, "Belt")
        self.assertTrue(loaded_products[0].metal)
        
        self.assertIsInstance(loaded_products[1], Cake)
        self.assertEqual(loaded_products[1].name, "Cake")
        self.assertEqual(loaded_products[1].height, 15)
        
        self.assertIsInstance(loaded_products[2], Cup)
        self.assertEqual(loaded_products[2].name, "Cup")
        self.assertEqual(loaded_products[2].volume, 250)

class TestProductWindow(unittest.TestCase):
    def setUp(self):
        self.window = ProductWindow()

    def test_initial_state(self):
        self.assertEqual(self.window.windowTitle(), "Product supply")
        self.assertEqual(len(self.window.product_manager.products), 0)
        
    def test_add_product(self):
        self.window.name_edit.setText("Test Product")
        self.window.amount_edit.setValue(5)
        self.window.type_select.setCurrentText("Belt")
        
        self.window.form_manager.get_special_field_value = MagicMock(return_value=True)
        
        self.window.add_product()
        self.assertEqual(len(self.window.product_manager.products), 1)
        self.assertEqual(self.window.product_manager.products[0].name, "Test Product")

    @patch.object(QMessageBox, 'warning')
    def test_add_product_empty_name(self, mock_warning):
        self.window.name_edit.setText("")
        self.window.add_product()
        self.assertEqual(len(self.window.product_manager.products), 0)

    @patch.object(QMessageBox, 'question', return_value=QMessageBox.StandardButton.Yes)
    def test_delete_product(self, mock_question):
        test_product = Belt(datetime.datetime.now(), "Test Belt", 1, True)
        self.window.product_manager.add_product(test_product)
        self.window.table_view = MagicMock()
        self.window.table_view.currentIndex.return_value.isValid.return_value = True
        self.window.table_view.currentIndex.return_value.row.return_value = 0
        self.window.delete_product()
        self.assertEqual(len(self.window.product_manager.products), 0)

    @patch.object(ProductFileHandler, 'save_products')
    @patch.object(QFileDialog, 'getSaveFileName', return_value=("test.txt", None))
    def test_save_products(self, mock_dialog, mock_save):
        self.window.save_products()
        mock_save.assert_called_once()

    @patch.object(ProductFileHandler, 'load_products')
    @patch.object(QFileDialog, 'getOpenFileName', return_value=("test.txt", None))
    @patch.object(QMessageBox, 'information')
    def test_load_products_success(self, mock_info, mock_dialog, mock_load):
        test_product = Belt(datetime.datetime.now(), "Loaded Belt", 1, True)
        mock_load.return_value = [test_product]
        
        self.window.load_products()
        self.assertEqual(len(self.window.product_manager.products), 1)
        mock_info.assert_called_once()

    @patch.object(ProductFileHandler, 'load_products', side_effect=Exception("Test error"))
    @patch.object(QFileDialog, 'getOpenFileName', return_value=("test.txt", None))
    @patch.object(QMessageBox, 'critical')
    def test_load_products_failure(self, mock_critical, mock_dialog, mock_load):
        self.window.load_products()
        mock_critical.assert_called_once()

if __name__ == '__main__':
    unittest.main()