import sys
from PyQt6.QtWidgets import (
    QApplication, QCheckBox, QMainWindow, QMenu, QTableWidget, QTableWidgetItem, 
    QVBoxLayout, QWidget, QHeaderView, QAbstractItemView, QWidgetAction
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt

from gui.employee_table import EmployeeTable
from gui.filter_header import FilterHeader
from gui.mock_data import generate_mock_data

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HR Management System")
        self.resize(800, 500)

        self.setup_ui()

    def setup_ui(self):
        self.craete_menu_bar()
        self.create_toolbar()
        self.create_employee_table()

    def craete_menu_bar(self):
        menu_bar = self.menuBar()
        
        # Defining your layout menus
        file_menu = menu_bar.addMenu("&File")
        employees_menu = menu_bar.addMenu("&Employee")
        contracts_menu = menu_bar.addMenu("&Contracts")
        documents_menu = menu_bar.addMenu("&Documents")
        payroll_menu = menu_bar.addMenu("&Payroll")
        reports_menu = menu_bar.addMenu("&Reports")
        tools_menu = menu_bar.addMenu("&Tools")
        help_menu = menu_bar.addMenu("&Help")

        # "File" Menu
        import_action = QAction("Import Employees", self)
        export_excel_action = QAction("Export to Excel", self)
        export_pdf_action = QAction("Export to PDF", self)
        
        file_menu.addAction(import_action)
        file_menu.addAction(export_excel_action)
        file_menu.addAction(export_pdf_action)
        
        file_menu.addSeparator()
        
        print_action = QAction("Print", self)
        print_preview_action = QAction("Print Preview", self)
        
        file_menu.addAction(print_action)
        file_menu.addAction(print_preview_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")  # Keyboard shortcut bonus!
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # "Employees" Menu
        new_emp_action = QAction("New Employee", self)
        new_emp_action.setShortcut("Ctrl+N")
        
        view_emp_action = QAction("View Employee", self)
        view_emp_action.setShortcut("Ctrl+I")  # "I" for Info/Inspect
        
        edit_emp_action = QAction("Edit Employee", self)
        edit_emp_action.setShortcut("Ctrl+E")
        
        delete_emp_action = QAction("Delete Employee", self)
        
        employees_menu.addAction(new_emp_action)
        employees_menu.addAction(view_emp_action)
        employees_menu.addAction(edit_emp_action)
        employees_menu.addAction(delete_emp_action)
        
        employees_menu.addSeparator()
        
        family_action = QAction("Family", self)
        
        employees_menu.addAction(family_action)

        employees_menu.addSeparator()

        end_employment_action = QAction("End Employment", self)
        history_action = QAction("Career History", self)
        
        employees_menu.addAction(end_employment_action)
        employees_menu.addAction(history_action)

        # "Contracts" Menu
        contract_list_action = QAction("Employee Contracts", self)
        contract_list_action.setShortcut("Ctrl+L")
        
        contracts_menu.addAction(contract_list_action)
        
        contracts_menu.addSeparator()
        
        new_contract_action = QAction("New Contract", self)
        renew_contract_action = QAction("Renew Contract", self)
        
        contracts_menu.addAction(new_contract_action)
        contracts_menu.addAction(renew_contract_action)
        
        contracts_menu.addSeparator()
        
        templates_action = QAction("Contract Templates", self)
        
        contracts_menu.addAction(templates_action)

        # "Documents" Menu
        emp_docs_action = QAction("Employee Documents", self)
        add_doc_action = QAction("Add Document", self)
        scan_doc_action = QAction("Scan Document", self)
        
        documents_menu.addAction(emp_docs_action)
        documents_menu.addAction(add_doc_action)
        documents_menu.addAction(scan_doc_action)
        
        # Separator Line
        documents_menu.addSeparator()
        
        print_file_action = QAction("Print Employee File", self)
        export_zip_action = QAction("Export Employee File (.zip)", self)
        
        documents_menu.addAction(print_file_action)
        documents_menu.addAction(export_zip_action)

        # "Payroll" Menu
        salary_grids_action = QAction("Salary Grid", self)
        bonuses_primes_action = QAction("Bonuses & Primes", self)
        
        payroll_menu.addAction(salary_grids_action)
        payroll_menu.addAction(bonuses_primes_action)

    def create_toolbar(self):
        toolbar = self.addToolBar("Quick Actions")
        toolbar.setMovable(False)  # Locks toolbar in place like a traditional app
        
        # Placeholder standard actions (Add, Edit, Delete)
        # You can replace standard icons with your own QIcon("path/to/icon.png")
        add_action = QAction(self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogNewFolder), "Add Employee", self)
        refresh_action = QAction(self.style().standardIcon(self.style().StandardPixmap.SP_BrowserReload), "Refresh", self)
        
        toggle_filters_action = QAction(self.style().standardIcon(self.style().StandardPixmap.SP_FileDialogContentsView), "Edit Details", self)
        toggle_filters_action.setCheckable(True)
        toggle_filters_action.setChecked(False)

        toggle_filters_action.toggled.connect(self.toggle_table_filters_visibility)

        toolbar.addAction(add_action)
        toolbar.addSeparator()
        toolbar.addAction(refresh_action)
        toolbar.addSeparator()
        toolbar.addAction(toggle_filters_action)

    def create_employee_table(self):
        self.table_widget = EmployeeTable()
        self.setCentralWidget(self.table_widget)

    def toggle_table_filters_visibility(self, visible: bool):
        self.table_widget.toggle_filters(visible=visible)

    def show_header_context_menu(self, position):
        """Generates the checkable column visibility manager menu."""
        menu = QMenu(self)
        
        for col, name in enumerate(self.all_columns):
            checkbox = QCheckBox(name)
            checkbox.setChecked(
                not self.table_widget.isColumnHidden(col)
            )

            checkbox.toggled.connect(lambda checked, c=col, cb=checkbox:self.toggle_column_visibility(c, checked, cb))

            action = QWidgetAction(menu)
            action.setDefaultWidget(checkbox)
            menu.addAction(action)
            
        # Add structural divider
        menu.addSeparator()
        
        # Add global quick actions
        show_all_act = QAction("Show All", menu)
        show_all_act.triggered.connect(lambda: [self.table_widget.setColumnHidden(i, False) for i in range(len(self.all_columns))])
        
        # hide_all_act = QAction("Hide All", menu)
        # hide_all_act.triggered.connect(lambda: [self.table_widget.setColumnHidden(i, True) for i in range(len(self.all_columns))])
        
        reset_act = QAction("Reset Default", menu)
        reset_act.triggered.connect(self.reset_default_columns)
        
        menu.addAction(show_all_act)
        # menu.addAction(hide_all_act)
        menu.addAction(reset_act)

        menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        
        # Execute the popup right where the user cursor clicked
        header = self.table_widget.horizontalHeader()
        menu.exec(header.mapToGlobal(position))

    def toggle_column_visibility(self, column, checked, checkbox):
        # User is trying to hide a column
        if not checked:
            visible_count = sum(
                not self.table_widget.isColumnHidden(c)
                for c in range(self.table_widget.columnCount())
            )

            # Don't allow hiding the last visible column
            if visible_count == 1:
                checkbox.blockSignals(True)
                checkbox.setChecked(True)
                checkbox.blockSignals(False)
                return

        self.table_widget.setColumnHidden(column, not checked)

    def reset_default_columns(self):
        """Helper to return layout state back to original visibility configurations."""
        for index, col_name in enumerate(self.all_columns):
            should_hide = col_name not in self.default_visible
            self.table_widget.setColumnHidden(index, should_hide)

    def insert_mock_data(self):
        dummy_employees = generate_mock_data()
        for row_index, employee_data in enumerate(dummy_employees):
            """Helper to quickly insert text cells."""
            if self.table_widget.rowCount() <= row_index:
                self.table_widget.insertRow(row_index)
            for col, data in enumerate(employee_data):
                self.table_widget.setItem(row_index, col, QTableWidgetItem(data))
