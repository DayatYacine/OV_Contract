from PyQt6.QtWidgets import (
    QDialog, QLabel, QLineEdit, QDateEdit, 
    QDialogButtonBox, QFormLayout, QVBoxLayout
)
from PyQt6.QtCore import Qt, QDate

class EmployeeFormDialog(QDialog):
    def __init__(self, employee_data=None, parent=None):
        super().__init__(parent)
        self.employee_data = employee_data  # sqlite3.Row or dict if editing, else None
        self.setWindowTitle("New Employee" if not employee_data else "Update Employee")
        self.setMinimumWidth(450)
        
        # Field registry for clean data extraction and population
        self.fields = {}
        
        self.init_ui()
        if self.employee_data:
            self.populate_fields(self.employee_data)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Use a clean form layout for fields and labels
        form_layout = QFormLayout()
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form_layout.setSpacing(10)  # Adds clean breathing room matching your mock
        
        # 1. Base Fields
        self.fields["matricule"] = QLineEdit()
        self.fields["first_name"] = QLineEdit()
        self.fields["last_name"] = QLineEdit()
        
        # 2. Arabic Fields (Right-to-Left aligned text)
        self.fields["first_name_arabic"] = QLineEdit()
        self.fields["first_name_arabic"].setAlignment(Qt.AlignmentFlag.AlignRight)
        self.fields["last_name_arabic"] = QLineEdit()
        self.fields["last_name_arabic"].setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # 3. National Identification & Birth Information
        self.fields["national_id"] = QLineEdit()
        
        self.fields["date_of_birth"] = QDateEdit()
        self.fields["date_of_birth"].setCalendarPopup(True)
        self.fields["date_of_birth"].setDisplayFormat("dd-MM-yyyy")
        self.fields["date_of_birth"].setDate(QDate.currentDate())
        
        self.fields["place_of_birth"] = QLineEdit()
        self.fields["place_of_birth_arabic"] = QLineEdit()
        self.fields["place_of_birth_arabic"].setAlignment(Qt.AlignmentFlag.AlignRight)
        
        # Build the Form Row Elements
        form_layout.addRow("Matricule:", self.fields["matricule"])
        form_layout.addRow("First Name:", self.fields["first_name"])
        form_layout.addRow("Last Name:", self.fields["last_name"])
        form_layout.addRow("First Name (Arabic):", self.fields["first_name_arabic"])
        form_layout.addRow("Last Name (Arabic):", self.fields["last_name_arabic"])
        form_layout.addRow("National ID (NIN):", self.fields["national_id"])
        form_layout.addRow("Date of Birth:", self.fields["date_of_birth"])
        form_layout.addRow("Place of Birth:", self.fields["place_of_birth"])
        form_layout.addRow("Place of Birth (Arabic):", self.fields["place_of_birth_arabic"])
        
        main_layout.addLayout(form_layout)
        
        # Standard Save and Cancel Action Buttons
        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.button_box)

    def populate_fields(self, data):
        """Pre-fills fields cleanly. Supports both dict and sqlite3.Row."""
        if not data:
            return
        for key in data.keys():
            value = data[key]
            if key in self.fields:
                widget = self.fields[key]
                if isinstance(widget, QLineEdit):
                    widget.setText(str(value or ""))
                elif isinstance(widget, QDateEdit):
                    if value:
                        qdate = QDate.fromString(value, "yyyy-MM-dd") if isinstance(value, str) else value
                        if qdate.isValid():
                            widget.setDate(qdate)

    def get_data(self):
        """Collects field inputs into a standard python dictionary payload."""
        data = {}
        for key, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                data[key] = widget.text().strip()
            elif isinstance(widget, QDateEdit):
                data[key] = widget.date().toString("yyyy-MM-dd")
        return data




# from PyQt6.QtWidgets import (
#     QDialog, QTabWidget, QWidget, QLabel, QLineEdit, 
#     QComboBox, QDateEdit, QDialogButtonBox, QFormLayout, 
#     QVBoxLayout, QHBoxLayout
# )
# from PyQt6.QtCore import Qt, QDate

# class EmployeeFormDialog(QDialog):
#     def __init__(self, employee_data=None, parent=None):
#         super().__init__(parent)
#         self.employee_data = employee_data  # Dictionary if editing, None if new
#         self.setWindowTitle("Employee Form Dialog" if not employee_data else "Update Employee Details")
#         self.setMinimumWidth(500)
        
#         # Dictionary tracking all field widgets for easy retrieval/setting
#         self.fields = {}
        
#         self.init_ui()
#         if self.employee_data:
#             self.populate_fields(self.employee_data)

#     def init_ui(self):
#         main_layout = QVBoxLayout(self)
        
#         # Initialize Tab Container
#         self.tabs = QTabWidget()
        
#         # Build individual tabs
#         self.tabs.addTab(self.create_identity_tab(), "Identity")
#         self.tabs.addTab(self.create_administrative_tab(), "Administrative")
#         self.tabs.addTab(self.create_employment_tab(), "Employment")
        
#         main_layout.addWidget(self.tabs)
        
#         # Standard Save / Cancel Buttons at bottom
#         self.button_box = QDialogButtonBox(
#             QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
#         )
#         self.button_box.accepted.connect(self.accept)
#         self.button_box.rejected.connect(self.reject)
#         main_layout.addWidget(self.button_box)

#     def create_identity_tab(self):
#         tab = QWidget()
#         layout = QFormLayout(tab)
#         layout.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        
#         self.fields["matricule"] = QLineEdit()
#         self.fields["first_name"] = QLineEdit()
#         self.fields["last_name"] = QLineEdit()
        
#         # Visual differentiation or RTL adjustments can be made here
#         self.fields["first_name_arabic"] = QLineEdit()
#         self.fields["first_name_arabic"].setAlignment(Qt.AlignmentFlag.AlignRight)
#         self.fields["last_name_arabic"] = QLineEdit()
#         self.fields["last_name_arabic"].setAlignment(Qt.AlignmentFlag.AlignRight)
        
#         self.fields["father_name"] = QLineEdit()
#         self.fields["mother_name"] = QLineEdit()
#         self.fields["national_id"] = QLineEdit()
        
#         self.fields["gender"] = QComboBox()
#         self.fields["gender"].addItems(["Male", "Female"])
        
#         self.fields["nationality"] = QComboBox()
#         self.fields["nationality"].addItems(["Algerian", "Other"])
        
#         # Map Form Fields
#         layout.addRow("Matricule:", self.fields["matricule"])
#         layout.addRow("First Name:", self.fields["first_name"])
#         layout.addRow("Last Name:", self.fields["last_name"])
#         layout.addRow("First Name (Arabic):", self.fields["first_name_arabic"])
#         layout.addRow("Last Name (Arabic):", self.fields["last_name_arabic"])
#         layout.addRow("Father's Name:", self.fields["father_name"])
#         layout.addRow("Mother's Name:", self.fields["mother_name"])
#         layout.addRow("National ID (NIN):", self.fields["national_id"])
#         layout.addRow("Gender:", self.fields["gender"])
#         layout.addRow("Nationality:", self.fields["nationality"])
        
#         return tab

#     def create_administrative_tab(self):
#         tab = QWidget()
#         layout = QFormLayout(tab)
        
#         self.fields["date_of_birth"] = QDateEdit()
#         self.fields["date_of_birth"].setCalendarPopup(True)
#         self.fields["date_of_birth"].setDisplayFormat("dd-MM-yyyy")
#         self.fields["date_of_birth"].setDate(QDate.currentDate())
        
#         self.fields["place_of_birth"] = QLineEdit()
#         self.fields["place_of_birth_arabic"] = QLineEdit()
#         self.fields["place_of_birth_arabic"].setAlignment(Qt.AlignmentFlag.AlignRight)
        
#         self.fields["address"] = QLineEdit()
#         self.fields["commune"] = QLineEdit()
#         self.fields["wilaya"] = QLineEdit()
#         self.fields["nss"] = QLineEdit() # Social Security
        
#         layout.addRow("Date of Birth:", self.fields["date_of_birth"])
#         layout.addRow("Place of Birth:", self.fields["place_of_birth"])
#         layout.addRow("Place of Birth (Arabic):", self.fields["place_of_birth_arabic"])
#         layout.addRow("Address:", self.fields["address"])
#         layout.addRow("Commune:", self.fields["commune"])
#         layout.addRow("Wilaya:", self.fields["wilaya"])
#         layout.addRow("Social Security (NSS):", self.fields["nss"])
        
#         return tab

#     def create_employment_tab(self):
#         tab = QWidget()
#         layout = QFormLayout(tab)
        
#         self.fields["employee_code"] = QLineEdit()
#         self.fields["position"] = QLineEdit()
#         self.fields["department"] = QLineEdit()
        
#         self.fields["contract_type"] = QComboBox()
#         self.fields["contract_type"].addItems(["CDI", "CDD", "CTA", "Other"])
        
#         self.fields["salary"] = QLineEdit()
        
#         self.fields["hire_date"] = QDateEdit()
#         self.fields["hire_date"].setCalendarPopup(True)
#         self.fields["hire_date"].setDisplayFormat("dd-MM-yyyy")
#         self.fields["hire_date"].setDate(QDate.currentDate())
        
#         layout.addRow("Employee Code:", self.fields["employee_code"])
#         layout.addRow("Position:", self.fields["position"])
#         layout.addRow("Department:", self.fields["department"])
#         layout.addRow("Contract Type:", self.fields["contract_type"])
#         layout.addRow("Salary:", self.fields["salary"])
#         layout.addRow("Hire Date:", self.fields["hire_date"])
        
#         return tab

#     def populate_fields(self, data):
#         """Pre-fills fields dynamically from a dictionary when updating an existing entry."""
#         for key, value in data.items():
#             if key in self.fields:
#                 widget = self.fields[key]
#                 if isinstance(widget, QLineEdit):
#                     widget.setText(str(value or ""))
#                 elif isinstance(widget, QComboBox):
#                     index = widget.findText(str(value))
#                     if index >= 0:
#                         widget.setCurrentIndex(index)
#                 elif isinstance(widget, QDateEdit):
#                     if value:
#                         # Assuming incoming date format is string 'YYYY-MM-DD' or QDate
#                         qdate = QDate.fromString(value, "yyyy-MM-dd") if isinstance(value, str) else value
#                         if qdate.isValid():
#                             widget.setDate(qdate)

#     def get_data(self):
#         """Collects field state into a single python dictionary clean payload."""
#         data = {}
#         for key, widget in self.fields.items():
#             if isinstance(widget, QLineEdit):
#                 data[key] = widget.text().strip()
#             elif isinstance(widget, QComboBox):
#                 data[key] = widget.currentText()
#             elif isinstance(widget, QDateEdit):
#                 data[key] = widget.date().toString("yyyy-MM-dd") # Standard DB storage format
#         return data


# class EmployeeFormDialog(QDialog):
#     """Popup window to create or update an employee"""
#     def __init__(self, employee_data=None, parent=None):
#         super().__init__(parent)
#         self.setWindowTitle("Employee Details" if employee_data else "New Employee")
#         self.layout = QFormLayout(self)
        
#         # self.inputs = {
#         #     "first_name": QLineEdit(self),
#         #     "last_name": QLineEdit(self),
#         #     "current_title": QLineEdit(self)
#         # }
        
#         # for label, widget in self.inputs.items():
#         #     self.layout.addRow(label.replace("_", " ").title() + ":", widget)
#         #     if employee_data:
#         #         widget.setText(str(employee_data.get(label, '')))
                
#         # self.buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
#         # self.buttons.accepted.connect(self.accept)
#         # self.buttons.rejected.connect(self.reject)
#         # self.layout.addRow(self.buttons)

#     def get_data(self):
#         return {key: widget.text() for key, widget in self.inputs.items()}
