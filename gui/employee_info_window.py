import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QTabWidget, QPushButton, QTableWidget, QTableWidgetItem, 
    QHeaderView, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class EmployeeProfileApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HR Management System - Employee Profile")
        self.resize(800, 600)
        
        # Main container widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # 1. HEADER BANNER
        header_frame = QFrame()
        header_frame.setFrameShape(QFrame.Shape.StyledPanel)
        header_frame.setStyleSheet("background-color: #2b2b2b; color: white; border-radius: 6px;")
        header_layout = QVBoxLayout(header_frame)
        
        top_row = QHBoxLayout()
        name_label = QLabel("👤 Ahmed Benali")
        name_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        status_label = QLabel("● Active  ")
        status_label.setStyleSheet("color: #4CAF50;")
        status_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        top_row.addWidget(name_label)
        top_row.addStretch()
        top_row.addWidget(status_label)
        
        meta_label = QLabel("EMP-0001 • Developer • IT Department • CDI")
        meta_label.setStyleSheet("color: #b0b0b0;")
        meta_label.setFont(QFont("Arial", 10))
        
        header_layout.addLayout(top_row)
        header_layout.addWidget(meta_label)
        main_layout.addWidget(header_frame)

        # 2. TAB PANEL
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Initialize tabs
        self.create_personal_tab()
        self.create_contact_tab()
        self.create_family_tab()
        self.create_employment_tab()
        self.create_contracts_tab()
        self.create_documents_tab()
        
        # # Add placeholders for remaining tabs
        # for missing_tab in ["Personal", "Contact", "Family"]:
        #     self.tabs.addTab(QLabel(f"Content for {missing_tab} Tab"), missing_tab)

        # 3. FOOTER ACTIONS
        footer_layout = QHBoxLayout()
        btn_edit = QPushButton("Edit Employee")
        btn_new = QPushButton("New Contract")
        btn_gen = QPushButton("Generate Document")
        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.close)
        
        footer_layout.addWidget(btn_edit)
        footer_layout.addWidget(btn_new)
        footer_layout.addWidget(btn_gen)
        footer_layout.addStretch()
        footer_layout.addWidget(btn_close)
        main_layout.addLayout(footer_layout)

    def create_personal_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        
        layout.addWidget(QLabel("<b>Personal Information</b>"))
        layout.addSpacing(10)
        
        # Form structure mapping fields to values
        # Format: (Field Label, Value, Is_Arabic_RTL)
        personal_data = [
            ("First Name", "Ahmed", False),
            ("Last Name", "Benali", False),
            ("First Name (Arabic)", "أحمد", True),
            ("Last Name (Arabic)", "بن علي", True),
            ("National ID", "1234567890123456", False),
            ("Gender", "Male", False),
            ("Date of Birth", "15-03-1990", False),
            ("Place of Birth", "Oran", False),
            ("Place of Birth (Arabic)", "وهران", True),
            ("Nationality", "Algerian", False)
        ]
        
        form_layout = QVBoxLayout()
        for field, value, is_rtl in personal_data:
            row = QHBoxLayout()
            
            # Left side: Fixed width label for strict alignment
            lbl_field = QLabel(f"{field}:")
            lbl_field.setFixedWidth(180) 
            lbl_field.setStyleSheet("color: #555555;")
            
            # Right side: The value token
            lbl_val = QLabel(value)
            lbl_val.setFont(QFont("Arial", 10))
            
            # Handle Right-To-Left alignment for Arabic entries
            if is_rtl:
                lbl_val.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                # Keep text flowing correctly if numbers/symbols mix in
                lbl_val.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
            else:
                lbl_val.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
                
            row.addWidget(lbl_field)
            row.addWidget(lbl_val)
            
            # Push non-RTL text to the left; let RTL text take up the dynamic width naturally
            if not is_rtl:
                row.addStretch()
                
            form_layout.addLayout(row)
            
        layout.addLayout(form_layout)
        layout.addStretch() # Push everything to the top
        
        # Replace the placeholder tab or append it
        # Assuming index 3 based on your original layout structure
        self.tabs.insertTab(0, tab, "Personal")

    def create_contact_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Section 1: Core Contact Details
        layout.addWidget(QLabel("<b>Contact Information</b>"))
        
        contact_data = [
            ("Phone Number", "+213 555 12 34 56"),
            ("Email", "ahmed.benali@example.com"),
            ("", ""), # Empty placeholder line to match text spacing
            ("Address", "15 Rue Emir Abdelkader"),
            ("Commune", "Bir El Djir"),
            ("Wilaya", "Oran")
        ]
        
        form_layout1 = QVBoxLayout()
        for field, value in contact_data:
            if not field and not value:
                form_layout1.addSpacing(10)
                continue
                
            row = QHBoxLayout()
            lbl_field = QLabel(f"{field}:")
            lbl_field.setFixedWidth(180)
            lbl_field.setStyleSheet("color: #555555;")
            
            lbl_val = QLabel(value)
            lbl_val.setFont(QFont("Arial", 10))
            
            row.addWidget(lbl_field)
            row.addWidget(lbl_val)
            row.addStretch()
            form_layout1.addLayout(row)
            
        layout.addLayout(form_layout1)
        layout.addSpacing(15)
        
        # Separator Line for Emergency Contact
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        sep.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(sep)
        layout.addSpacing(5)
        
        # Section 2: Emergency Contact
        layout.addWidget(QLabel("<b>Emergency Contact</b>"))
        
        emergency_data = [
            ("Contact Name", "Mohamed Benali"),
            ("Phone Number", "+213 666 11 22 33")
        ]
        
        form_layout2 = QVBoxLayout()
        for field, value in emergency_data:
            row = QHBoxLayout()
            lbl_field = QLabel(f"{field}:")
            lbl_field.setFixedWidth(180)
            lbl_field.setStyleSheet("color: #555555;")
            
            lbl_val = QLabel(value)
            lbl_val.setFont(QFont("Arial", 10))
            
            row.addWidget(lbl_field)
            row.addWidget(lbl_val)
            row.addStretch()
            form_layout2.addLayout(row)
            
        layout.addLayout(form_layout2)
        layout.addStretch() # Push everything north
        
        # Insert as the second tab (Index 1)
        self.tabs.insertTab(1, tab, "Contact")

    def create_family_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Section 1: Overview Summary Fields
        layout.addWidget(QLabel("<b>Family Information</b>"))
        
        summary_data = [
            ("Marital Status", "Married"),
            ("Number of Children", "2")
        ]
        
        form_layout = QVBoxLayout()
        for field, value in summary_data:
            row = QHBoxLayout()
            lbl_field = QLabel(f"{field}:")
            lbl_field.setFixedWidth(180)
            lbl_field.setStyleSheet("color: #555555;")
            
            lbl_val = QLabel(value)
            lbl_val.setFont(QFont("Arial", 10))
            
            row.addWidget(lbl_field)
            row.addWidget(lbl_val)
            row.addStretch()
            form_layout.addLayout(row)
            
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        
        # Separator Line before the Table
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setFrameShadow(QFrame.Shadow.Sunken)
        sep.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(sep)
        layout.addSpacing(5)
        
        # Section 2: Dependents Structured Grid
        layout.addWidget(QLabel("<b>Dependents</b>"))
        
        # Setup Grid Table (3 rows, 4 columns matching mock structural blueprint)
        table = QTableWidget(3, 4)
        table.setHorizontalHeaderLabels(["#", "Name", "Relationship", "Date of Birth"])
        
        # Sizing rules: Small column for ID number, stretch remaining columns evenly
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        for i in range(1, 4):
            table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
            
        dependents_data = [
            ["1", "Fatima Benali", "Spouse", "15-03-1990"],
            ["2", "Mohamed Benali", "Son", "21-08-2018"],
            ["3", "Sara Benali", "Daughter", "10-11-2021"]
        ]
        
        for row_idx, row_data in enumerate(dependents_data):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                # Center align the index identifier column (#)
                if col_idx == 0:
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_idx, col_idx, item)
                
        layout.addWidget(table)
        
        # Add Tab contextual operational actions to mirror the other table subviews
        # actions = QHBoxLayout()
        # actions.addWidget(QPushButton("Add Dependent"))
        # actions.addWidget(QPushButton("Modify"))
        # actions.addWidget(QPushButton("Remove"))
        # actions.addStretch()
        # layout.addLayout(actions)
        
        # Insert as the third tab (Index 2)
        self.tabs.insertTab(2, tab, "Family")

    def create_employment_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Grid/Form style for Employment Details
        form_layout = QVBoxLayout()
        details = [
            ("Matricule", "EMP-0001"), ("Hire Date", "01-01-2024"),
            ("Department", "IT"), ("Position", "Developer"),
            ("Work Location", "Oran"), ("Social Security No.", "123456789012"),
            ("Bank Account", "CCP ************")
        ]
        
        layout.addWidget(QLabel("<b>Employment Details</b>"))
        for field, value in details:
            row = QHBoxLayout()
            lbl_field = QLabel(f"{field}:")
            lbl_field.setFixedWidth(150)
            lbl_val = QLabel(value)
            row.addWidget(lbl_field)
            row.addWidget(lbl_val)
            row.addStretch()
            form_layout.addLayout(row)
            
        layout.addLayout(form_layout)
        layout.addSpacing(15)
        
        # Current Contract Section
        layout.addWidget(QLabel("<b>Current Contract</b>"))
        contract_details = [
            ("Type", "CDI"), ("Start Date", "01-01-2024"),
            ("Salary Grid", "Category 12 / Class 3"), ("Base Salary", "75,000 DA")
        ]
        for field, value in contract_details:
            row = QHBoxLayout()
            lbl_field = QLabel(f"{field}:")
            lbl_field.setFixedWidth(150)
            lbl_val = QLabel(value)
            row.addWidget(lbl_field)
            row.addWidget(lbl_val)
            row.addStretch()
            layout.addLayout(row)
            
        layout.addStretch()
        self.tabs.addTab(tab, "Employment")

    def create_contracts_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        table = QTableWidget(2, 5)
        table.setHorizontalHeaderLabels(["ID", "Type", "Start Date", "End Date", "Salary Grid"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        data = [
            ["1", "CDD", "01-01-2023", "31-12-2023", "Category 11 / Cl 2"],
            ["2", "CDI", "01-01-2024", "-", "Category 12 / Cl 3"]
        ]
        
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(value))
                
        layout.addWidget(table)
        
        # Tab Context Actions
        # actions = QHBoxLayout()
        # actions.addWidget(QPushButton("New Contract"))
        # actions.addWidget(QPushButton("Renew"))
        # actions.addWidget(QPushButton("View Details"))
        # actions.addStretch()
        # layout.addLayout(actions)
        
        self.tabs.addTab(tab, "Contracts")

    def create_documents_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        table = QTableWidget(3, 3)
        table.setHorizontalHeaderLabels(["ID", "Document", "File"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        data = [
            ["1", "National ID", "cin.pdf"],
            ["2", "Birth Certificate", "naissance.pdf"],
            ["3", "Diploma", "master.pdf"]
        ]
        
        for row_idx, row_data in enumerate(data):
            for col_idx, value in enumerate(row_data):
                table.setItem(row_idx, col_idx, QTableWidgetItem(value))
                
        layout.addWidget(table)
        
        # Tab Context Actions
        # actions = QHBoxLayout()
        # actions.addWidget(QPushButton("Add"))
        # actions.addWidget(QPushButton("Open"))
        # actions.addWidget(QPushButton("Delete"))
        # actions.addStretch()
        # layout.addLayout(actions)
        
        self.tabs.addTab(tab, "Documents")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Optional styling to give it a modern clean edge
    app.setStyleSheet("""
        QTabWidget::panel { border: 1px solid #ccc; }
        QTabBar::tab { padding: 8px 16px; background: #e0e0e0; }
        QTabBar::tab:selected { background: #ffffff; border-bottom: 2px solid #0078d4; }
        QPushButton { padding: 6px 12px; }
    """)
    window = EmployeeProfileApp()
    window.show()
    sys.exit(app.exec())