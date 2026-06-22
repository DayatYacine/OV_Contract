import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFrame, QLineEdit, QComboBox, QDateEdit, 
    QFormLayout, QGroupBox, QSpinBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QDialog, QListWidget, QAbstractItemView
)
from PyQt6.QtCore import Qt, QDate

# ─────────────────────────────────────────────────────────────────
# 1. CONTRACT DIALOG MODAL (Opens via Add/Edit on Contracts Tab)
# ─────────────────────────────────────────────────────────────────
class ContractDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Contract Details")
        self.resize(400, 450)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Inputs
        self.type_combo = QComboBox()
        self.type_combo.addItems(["CDD", "CDI", "Anap"])
        
        self.start_date = QDateEdit(calendarPopup=True)
        self.start_date.setDate(QDate.currentDate())
        
        self.end_date = QDateEdit(calendarPopup=True)
        self.end_date.setDate(QDate.currentDate().addYears(1))
        
        self.category_combo = QComboBox()
        self.category_combo.addItems([str(i) for i in range(1, 21)])
        self.category_combo.setCurrentText("12")
        
        self.class_combo = QComboBox()
        self.class_combo.addItems([str(i) for i in range(1, 11)])
        self.class_combo.setCurrentText("3")
        
        self.base_salary = QLineEdit("75,000.00 DA")
        
        form_layout.addRow("Contract Type:", self.type_combo)
        form_layout.addRow("Start Date:", self.start_date)
        form_layout.addRow("End Date:", self.end_date)
        form_layout.addRow("Salary Category:", self.category_combo)
        form_layout.addRow("Salary Class:", self.class_combo)
        form_layout.addRow("Base Salary:", self.base_salary)
        
        # Bonuses Group
        bonus_group = QGroupBox("Bonuses")
        bonus_layout = QVBoxLayout()
        bonus_list = QListWidget()
        bonus_list.addItems([
            "Prime Rendement          5000 DA",
            "Prime Transport           2000 DA"
        ])
        bonus_layout.addWidget(bonus_list)
        bonus_group.setLayout(bonus_layout)
        
        # Dialog Action Buttons
        btn_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        cancel_btn = QPushButton("Cancel")
        save_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addStretch()
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(form_layout)
        layout.addWidget(bonus_group)
        layout.addLayout(btn_layout)
        self.setLayout(layout)


# ─────────────────────────────────────────────────────────────────
# 2. MAIN EMPLOYEE WINDOW WITH TABS
# ─────────────────────────────────────────────────────────────────
class EmployeeManagementApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Employee Management System")
        self.resize(750, 550)
        
        # Base Application Layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Master Tab Control
        self.tabs = QTabWidget()
        
        # Setup individual tabs
        self.tabs.addTab(self.create_personal_tab(), "Personal")
        self.tabs.addTab(self.create_contact_tab(), "Contact")
        self.tabs.addTab(self.create_family_tab(), "Family")
        self.tabs.addTab(self.create_employment_tab(), "Employment")
        self.tabs.addTab(self.create_contracts_tab(), "Contracts")
        self.tabs.addTab(self.create_documents_tab(), "Documents")
        
        main_layout.addWidget(self.tabs)
        
        # Divider Line
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(divider)
        
        # Persistent Bottom Action Bar
        action_layout = QHBoxLayout()
        save_main_btn = QPushButton("Save Employee Data")
        cancel_main_btn = QPushButton("Cancel")
        
        save_main_btn.setStyleSheet("font-weight: bold; padding: 5px 15px;")
        cancel_main_btn.setStyleSheet("padding: 5px 15px;")
        
        action_layout.addStretch()
        action_layout.addWidget(save_main_btn)
        action_layout.addWidget(cancel_main_btn)
        main_layout.addLayout(action_layout)
        
        # Wire up app closing action
        cancel_main_btn.clicked.connect(self.close)

    # --- 1. PERSONAL TAB ---
    def create_personal_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("Personal Information")
        form = QFormLayout()
        
        form.addRow("First Name:", QLineEdit())
        form.addRow("Last Name:", QLineEdit())
        form.addRow("First Name (Arabic):", QLineEdit())
        form.addRow("Last Name (Arabic):", QLineEdit())
        form.addRow("National ID:", QLineEdit())
        
        gender = QComboBox()
        gender.addItems(["Male", "Female"])
        form.addRow("Gender:", gender)
        
        dob = QDateEdit(calendarPopup=True)
        dob.setDate(QDate(1990, 1, 1))
        form.addRow("Date of Birth:", dob)
        
        form.addRow("Place of Birth:", QLineEdit())
        form.addRow("Place of Birth (Arabic):", QLineEdit())
        
        nationality = QComboBox()
        nationality.addItems(["Algerian", "Tunisian", "Moroccan", "Other"])
        form.addRow("Nationality:", nationality)
        
        group.setLayout(form)
        layout.addWidget(group)
        widget.setLayout(layout)
        return widget

    # --- 2. CONTACT TAB ---
    def create_contact_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("Contact Information")
        form = QFormLayout()
        
        form.addRow("Phone Number:", QLineEdit())
        form.addRow("Email:", QLineEdit())
        form.addRow("Address:", QLineEdit())
        form.addRow("Commune:", QLineEdit())
        form.addRow("Wilaya:", QLineEdit())
        form.addRow("Emergency Contact Name:", QLineEdit())
        form.addRow("Emergency Contact Tel:", QLineEdit())
        
        group.setLayout(form)
        layout.addWidget(group)
        widget.setLayout(layout)
        return widget

    # --- 3. FAMILY TAB ---
    def create_family_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("Family Information")
        form = QFormLayout()
        
        marital_status = QComboBox()
        marital_status.addItems(["Single", "Married", "Divorced", "Widowed"])
        form.addRow("Marital Status:", marital_status)
        
        children_count = QSpinBox()
        children_count.setRange(0, 20)
        form.addRow("Number of Children:", children_count)
        
        group.setLayout(form)
        layout.addWidget(group)
        layout.addStretch()  # Keeps things compact at the top
        widget.setLayout(layout)
        return widget

    # --- 4. EMPLOYMENT TAB ---
    def create_employment_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        group = QGroupBox("Employment Details")
        form = QFormLayout()
        
        matricule = QLineEdit("EMP-2026-001")
        form.addRow("Matricule:", matricule)
        
        hire_date = QDateEdit(calendarPopup=True)
        hire_date.setDate(QDate(2026, 6, 22))
        form.addRow("Hire Date:", hire_date)
        
        dept = QComboBox()
        dept.addItems(["IT Department", "HR Department", "Finance", "Logistics"])
        form.addRow("Department:", dept)
        
        pos = QComboBox()
        pos.addItems(["Developer", "Systems Engineer", "HR Manager", "Accountant"])
        form.addRow("Position:", pos)
        
        loc = QLineEdit("Oran Office")
        form.addRow("Work Location:", loc)
        
        form.addRow("Social Security (NSS):", QLineEdit())
        form.addRow("Bank Account (CCP/RIB):", QLineEdit())
        
        group.setLayout(form)
        layout.addWidget(group)
        widget.setLayout(layout)
        return widget

    # --- 5. CONTRACTS TAB ---
    def create_contracts_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Data Grid Setup
        table = QTableWidget(2, 5)
        table.setHorizontalHeaderLabels(["ID", "Type", "Start Date", "End Date", "Salary Grid"])
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Populate Mock Contract Records
        mock_data = [
            ("1", "CDD", "01-01-2025", "31-12-2025", "Category 12 / Cl 3"),
            ("2", "CDI", "01-01-2026", "-", "Category 13 / Cl 1")
        ]
        for row_idx, row_data in enumerate(mock_data):
            for col_idx, text in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(text))
                
        layout.addWidget(QLabel("<b>Contract History</b>"))
        layout.addWidget(table)
        
        # Sub-Action Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add")
        edit_btn = QPushButton("Edit")
        del_btn = QPushButton("Delete")
        renew_btn = QPushButton("Renew")
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addWidget(renew_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        # Launch detail pop-up on Add or Edit click
        add_btn.clicked.connect(self.open_contract_window)
        edit_btn.clicked.connect(self.open_contract_window)
        
        widget.setLayout(layout)
        return widget

    # --- 6. DOCUMENTS TAB ---
    def create_documents_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Data Grid Setup
        table = QTableWidget(3, 3)
        table.setHorizontalHeaderLabels(["ID", "Type", "File Name"])
        table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        mock_docs = [
            ("1", "Birth Certificate", "naissance.pdf"),
            ("2", "Diploma", "master.pdf"),
            ("3", "National ID", "cin.pdf")
        ]
        for row_idx, row_data in enumerate(mock_docs):
            for col_idx, text in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(text))
                
        layout.addWidget(QLabel("<b>Attached Documents</b>"))
        layout.addWidget(table)
        
        # Sub-Action Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Document")
        open_btn = QPushButton("Open File")
        del_btn = QPushButton("Delete")
        
        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(open_btn)
        btn_layout.addWidget(del_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        widget.setLayout(layout)
        return widget

    def open_contract_window(self):
        # Open Modal Popup
        dialog = ContractDialog(self)
        dialog.exec()


# ─────────────────────────────────────────────────────────────────
# APPLICATION RUNNER
# ─────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Simple styling cleanup 
    app.setStyle("Fusion") 
    
    window = EmployeeManagementApp()
    window.show()
    sys.exit(app.exec())