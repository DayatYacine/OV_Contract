from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog,
                             QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, 
                             QMenu, QDialog, QFormLayout, QDialogButtonBox, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from services.employee_service import fetch_employees
from gui.employee_form_window import EmployeeFormDialog


class EmployeeSelectorWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(700, 500)
        self.raw_data = [] # Will hold data fetched from services.database
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # 1. Action Row
        action_layout = QHBoxLayout()
        self.btn_new = QPushButton("+ New Employee")
        self.btn_import = QPushButton("Import Data")
        # self.btn_generate = QPushButton("Generate Contracts")
        
        self.btn_new.clicked.connect(self.open_create_dialog)
        self.btn_import.clicked.connect(self.import_file)
        
        action_layout.addWidget(self.btn_new)
        action_layout.addWidget(self.btn_import)
        # action_layout.addWidget(self.btn_generate)
        action_layout.addStretch()

        header_labels = ["", "Matricule", "First Name", "Last Name",
                         "First Name Arabic", "Last Name Arabic", "National ID",
                         "Date Of Birth", "Place Of Birth", "Place Of Birth Arabic"]
        
        # 2. Table Widget Config
        self.table = QTableWidget()
        self.table.setColumnCount(len(header_labels))
        self.table.setHorizontalHeaderLabels(header_labels)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.verticalHeader().setVisible(False)
        
        # Enable custom context menus
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)
        
        # 3. Dedicated Filter Row (Inserted as the very first row)
        self.table.insertRow(0)
        self.filter_widgets = []

        # Checkbox Item
        chk_item = QTableWidgetItem()
        chk_item.setCheckState(Qt.CheckState.Unchecked)
        self.table.setItem(0, 0, chk_item)

        for col in range(1, len(header_labels)):
            filter_input = QLineEdit()
            filter_input.setPlaceholderText("Filter...")
            filter_input.textChanged.connect(self.apply_filters)
            self.table.setCellWidget(0, col, filter_input)
            self.filter_widgets.append(filter_input)
            
        main_layout.addLayout(action_layout)
        main_layout.addWidget(self.table)
        
        # Test Data Mock
        # self.load_mock_data()

        self.load_data()

    def load_data(self):
        # Fetch rows using our background service
        employees = fetch_employees()
        self.refresh_table(employees)

    def load_mock_data(self):
        """Replace this later with real database select calls"""
        self.raw_data = [
            {"id": 1, "first_name": "Ahmed", "last_name": "Ben", "current_title": "Manager", "status": "Active"},
            {"id": 2, "first_name": "Yacine", "last_name": "Cherif", "current_title": "Engineer", "status": "Active"}
        ]
        self.refresh_table(self.raw_data)

    def refresh_table(self, data_list):
        # Clear items but preserve our filter header row (row 0)
        while self.table.rowCount() > 1:
            self.table.removeRow(1)

        self.raw_data = data_list

        self.table.setSortingEnabled(True)
        # self.table.setRowCount(len(self.raw_data))
        
        for row, emp in enumerate(self.raw_data):
            row = row + 1
            self.table.insertRow(row)
            # Column 0: ID (Hidden or visible, holds the UserRole)
            chk_item = QTableWidgetItem()
            chk_item.setCheckState(Qt.CheckState.Unchecked)
            chk_item.setData(Qt.ItemDataRole.UserRole, emp["id"]) # Hide DB ID here
            self.table.setItem(row, 0, chk_item)

            matricule_item = QTableWidgetItem(emp["matricule"])
            first_name = QTableWidgetItem(emp["first_name"])
            last_name = QTableWidgetItem(emp["last_name"])
            first_name_arabic = QTableWidgetItem(emp["first_name_arabic"])
            last_name_arabic = QTableWidgetItem(emp["last_name_arabic"])
            national_id = QTableWidgetItem(emp["national_id"])
            date_of_birth = QTableWidgetItem(emp["date_of_birth"])
            place_of_birth = QTableWidgetItem(emp["place_of_birth"])
            place_of_birth_arabic = QTableWidgetItem(emp["place_of_birth_arabic"])

            matricule_item.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            first_name.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            last_name.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            first_name_arabic.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            last_name_arabic.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            national_id.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            date_of_birth.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            place_of_birth.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)
            place_of_birth_arabic.setFlags(Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable)

            self.table.setItem(row, 1, matricule_item)
            self.table.setItem(row, 2, first_name)
            self.table.setItem(row, 3, last_name)
            self.table.setItem(row, 4, first_name_arabic)
            self.table.setItem(row, 5, last_name_arabic)
            self.table.setItem(row, 6, national_id)
            self.table.setItem(row, 7, date_of_birth)
            self.table.setItem(row, 8, place_of_birth)
            self.table.setItem(row, 9, place_of_birth_arabic)

    def get_cell_text(self, row, col):
        """Safely retrieve lowercase text from a table cell."""
        item = self.table.item(row, col)
        return item.text().lower() if item else ""

    def apply_filters(self):
        filters = [widget.text().lower() for widget in self.filter_widgets[:9]]

        for row in range(1, self.table.rowCount()):
            row_data = [self.get_cell_text(row, col) for col in range(1, 10)]
            show_row = all(f_text in r_text for f_text, r_text in zip(filters, row_data))
            self.table.setRowHidden(row, not show_row)

    def open_context_menu(self, position):
        current_row = self.table.currentRow()
        # means right-click happened on empty space or no row is selected
        if current_row == -1:
            return
        
        context_menu = QMenu(self)
    
        # ─── SECTION 1 ───
        view_action = QAction("View", self)
        context_menu.addAction(view_action)
        
        context_menu.addSeparator()
        
        # ─── SECTION 2 ───
        edit_action = QAction("Edit", self)
        delete_action = QAction("Delete", self)
        context_menu.addActions([edit_action, delete_action])
        
        context_menu.addSeparator()
        
        # ─── SECTION 3 ───
        new_contract_action = QAction("New Contract", self)
        renew_contract_action = QAction("Renew Contract", self)
        view_contracts_action = QAction("View Contracts", self)
        context_menu.addActions([new_contract_action, renew_contract_action, view_contracts_action])
        
        context_menu.addSeparator()
        
        # ─── SECTION 4: SUBMENU (Generate Documents ▶) ───
        generate_submenu = QMenu("Generate Documents", self)
        
        # Mock document options for the submenu
        gen_contract_doc = QAction("Contract Certificate", self)
        gen_work_doc = QAction("Work Certificate", self)
        generate_submenu.addActions([gen_contract_doc, gen_work_doc])
        
        context_menu.addMenu(generate_submenu)
        
        context_menu.addSeparator()
        
        # ─── SECTION 5 ───
        duplicate_action = QAction("Duplicate Employee", self)
        context_menu.addAction(duplicate_action)
        
        # ─── CONNECT ACTIONS TO FUNCTIONS ───
        # Example wiring:
        # new_contract_action.triggered.connect(self.open_contract_window)
        # edit_action.triggered.connect(self.open_contract_window)
        
        # Executing the menu at the exact right position on screen
        context_menu.exec(self.mapToGlobal(position))

        # menu = QMenu(self)

        # # Update Action
        # act_edit = QAction("Update Employee", self)
        # # Pass the specific row index cleanly via lambda
        # act_edit.triggered.connect(lambda: self.open_edit_dialog(current_row))
        # menu.addAction(act_edit)

        # # Delete Action
        # act_delete = QAction("Delete Employee", self)
        # # Pass it as a list if your delete_rows method still expects a list/iterable
        # act_delete.triggered.connect(lambda: self.delete_rows([current_row]))
        # menu.addAction(act_delete)
    
        # # Map the viewport local position to the global screen position
        # menu.exec(self.table.viewport().mapToGlobal(position))
        
        # # Count rows selected by looking at selected ranges
        # selected_rows = []
        # for r in selected_ranges:
        #     for row_idx in range(r.topRow(), r.bottomRow() + 1):
        #         if row_idx != 0: # Skip filter header
        #             selected_rows.append(row_idx)
                    
        # selected_rows = list(set(selected_rows)) # unique
        
        # if len(selected_rows) == 1:
        #     # Single row choices
        #     act_edit = QAction("Update Employee", self)
        #     act_edit.triggered.connect(lambda: self.open_edit_dialog(selected_rows[0]))
        #     menu.addAction(act_edit)
            
        # if len(selected_rows) >= 1:
        #     # Multi row choice
        #     act_delete = QAction(f"Delete Selected ({len(selected_rows)})", self)
        #     act_delete.triggered.connect(lambda: self.delete_rows(selected_rows))
        #     menu.addAction(act_delete)
            
        # menu.exec(self.table.viewport().mapToGlobal(position))

    def open_create_dialog(self):
        dialog = EmployeeFormDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            # Handle saving to services/database.py here
            print("Creating:", new_data)

    def open_edit_dialog(self, row_index):
        # Ensure the item exists before calling .data() to avoid NoneType crashes
        id_item = self.table.item(row_index, 0)
        if not id_item:
            return
        
        emp_id = id_item.data(Qt.ItemDataRole.UserRole)
    
        # Find local dictionary reference by unique ID (Safe from sorting/filtering)
        # Force both to strings during the match to handle int vs string issues
        emp_data = next((x for x in self.raw_data if x["id"] == emp_id), None)
        if not emp_data:
            print(f"Error: Employee ID {emp_id} not found in local cache.")
            return
        
        # Open the Dialog
        emp_data_dict = dict(emp_data) if emp_data else None
        dialog = EmployeeFormDialog(employee_data=emp_data_dict, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_fields = dialog.get_data()
            
            # Handle Database Transaction
            try:
                # Assuming your database module has an update function
                # database.update_employee(emp_id, updated_fields)
                print(f"Database Transaction Success for ID {emp_id}:", updated_fields)
                
                # Update local memory cache
                # emp_data.update(updated_fields)
                
                # Update the visual table row immediately without reloading everything
                # self.refresh_table_row(row_index, updated_fields)
                
            except Exception as e:
                print(f"Database Transaction Failed: {e}")
                # Optionally show a QMessageBox error dialog here


        # emp_id = self.table.item(row_index, 0).data(Qt.ItemDataRole.UserRole)
        # # Find local dictionary reference
        # emp_data = next((x for x in self.raw_data if x["id"] == emp_id), None)
        # print(row_index)
        
        # dialog = EmployeeFormDialog(employee_data=emp_data, parent=self)
        # if dialog.exec() == QDialog.DialogCode.Accepted:
        #     updated_fields = dialog.get_data()
        #     # Handle updating database.py via transaction here
        #     print(f"Updating ID {emp_id}:", updated_fields)

    def delete_rows(self, row_indices):
        ids_to_delete = [self.table.item(r, 0).data(Qt.ItemDataRole.UserRole) for r in row_indices]
        confirm = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete {len(ids_to_delete)} employees?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            # Run DELETE FROM employees WHERE id IN (...) via database layer
            print("Deleting Database IDs:", ids_to_delete)

    def import_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import File", "", "Spreadsheets (*.csv *.xlsx *.ods)")
        if file_path:
            # Call your services/spreadsheet_reader.py here
            print(f"File selected for background parsing: {file_path}")