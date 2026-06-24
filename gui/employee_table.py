from PyQt6.QtWidgets import (QFrame, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
                             QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMenu, QDialog, QFormLayout, QDialogButtonBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont
from gui.employee_form_window import EmployeeFormDialog
from gui.confirm_delete_dialog import ConfirmDeleteDialog
from gui.filter_header import FilterHeader
from gui.mock_data import generate_mock_data

class EmployeeTable(QTableWidget):    
    def __init__(self, parent=None):
        # Call the parent QTableWidget constructor
        super().__init__(parent)
        self.all_header = [
            "Matricule", "First Name", "Last Name",
            "First Name Arabic", "Last Name Arabic", "National ID",
            "Date Of Birth", "Place Of Birth", "Place Of Birth Arabic"
        ]
        
        # Default columns you want visible out of the gate
        self.header_default_visible = [
            "Matricule", "First Name", "Last Name",
            "First Name Arabic", "Last Name Arabic"
        ]
        self.headers = self.all_header
        self.filters: dict[int, QLineEdit] = {}
        self.header = FilterHeader(self)
        self.setup_table()

    def setup_table(self):
        """Initial configuration for the table look and structure."""
        self.setSortingEnabled(True)

        self.setColumnCount(len(self.headers))
        self.setHorizontalHeader(self.header)

        # Apply text alignment directly to the horizontal header items
        for col, header in enumerate(self.headers):
            header_item = QTableWidgetItem(header)
            
            # Align text to the Top and Center Horizontally
            header_item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
            
            self.setHorizontalHeaderItem(col, header_item)
        
        # Generate the filter inputs matching column count
        self.header.setColumnCount(self.columnCount())

        # 2. Connect to the horizontal scrollbar to update positions on scroll
        self.horizontalScrollBar().valueChanged.connect(self.header.updatePositions)

        # Select entire rows rather than individual cells
        # self.resizeColumnsToContents()
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        # self.verticalHeader().setVisible(False)

        # self.setSortingEnabled(True)

        # self.create_filter_row()

        employess = generate_mock_data()
        self.load_employees(employees=employess)

    def toggle_filters(self, visible: bool):
        self.header.toggle_filters(visible=visible)

    def load_employees(self, employees):
        self.employees = employees

        self.setSortingEnabled(False)
        if not employees:
            self.setRowCount(0)
            self.setColumnCount(0)
            return

        self.setRowCount(len(employees))

        for row, employee in enumerate(employees):
            for col, key in enumerate(self.headers):
                dict_key = key.lower().replace(" ", "_")
                value = str(employee.get(dict_key, "NON"))
                item = QTableWidgetItem()
                item.setText(value)
                item.setData(Qt.ItemDataRole.UserRole, employee.get("id", ""))
                self.setItem(row, col, item)
                # print(col, key, dict_key, value)
                # print(employee)

        self.resizeColumnsToContents()
        self.setSortingEnabled(True)
        self.horizontalHeader().setSectionsClickable(True)

    def add_row(self, row_data: list[str]):
        """Helper to dynamically append a row of data."""
        current_row = self.rowCount()
        self.insertRow(current_row)
        
        for column, value in enumerate(row_data):
            item = QTableWidgetItem(str(value))
            self.setItem(current_row, column, item)
            
    def get_selected_row_data(self) -> list[str] | None:
        """Helper to get data from the currently selected row."""
        selected_ranges = self.selectedRanges()
        if not selected_ranges:
            return None
            
        row = selected_ranges[0].topRow()
        return [self.item(row, col).text() for col in range(self.columnCount())]

    def clear_all(self):
        """Removes all rows."""
        self.setRowCount(0)
