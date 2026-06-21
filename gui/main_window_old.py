# gui/main_window.py

import re
import zipfile
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
)

from gui.employee_selector import EmployeeSelectorWindow

DEFAULT_TEMPLATE = r"C:\Users\Yacine\Desktop\CONTRAT.odt"
DEFAULT_SHEET = r"C:\Users\Yacine\Desktop\full.ods"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("OV ContractGen")
        self.resize(700, 500)

        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(15)

        # Title
        title = QLabel("Contract Generator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 22px; font-weight: bold;"
        )

        subtitle = QLabel(
            "CDD/CDI Contract Generation System"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        
        # -------------------------
        # Employee List Spreadsheet
        # -------------------------
        main_layout.addWidget(
            QLabel("Employee List Spreadsheet")
        )

        sheet_layout = QHBoxLayout()

        self.sheet_edit = QLineEdit()
        # self.sheet_edit.setReadOnly(True)
        self.sheet_edit.setText(r"C:\Users\Yacine\Desktop\full.ods")

        self.sheet_btn = QPushButton("Browse...")
        self.sheet_btn.clicked.connect(
            self.select_spreadsheet
        )

        sheet_layout.addWidget(self.sheet_edit)
        sheet_layout.addWidget(self.sheet_btn)

        main_layout.addLayout(sheet_layout)

        # -------------------------
        # Contract Template
        # -------------------------
        main_layout.addWidget(QLabel("Contract Template"))

        template_layout = QHBoxLayout()

        self.template_edit = QLineEdit()
        # self.template_edit.setReadOnly(True)
        self.template_edit.setText(r"C:\Users\Yacine\Desktop\CONTRAT.odt")

        self.template_btn = QPushButton("Browse...")
        self.template_btn.clicked.connect(
            self.select_template
        )

        template_layout.addWidget(self.template_edit)
        template_layout.addWidget(self.template_btn)

        main_layout.addLayout(template_layout)


        # -------------------------
        # Contract Type
        # -------------------------
        main_layout.addWidget(QLabel("Contract Type"))

        contract_layout = QHBoxLayout()

        self.cdd_radio = QRadioButton("CDD")
        self.cdi_radio = QRadioButton("CDI")

        # Default selection
        self.cdd_radio.setChecked(True)

        self.contract_group = QButtonGroup(self)
        self.contract_group.addButton(self.cdd_radio)
        self.contract_group.addButton(self.cdi_radio)

        contract_layout.addWidget(self.cdd_radio)
        contract_layout.addWidget(self.cdi_radio)
        contract_layout.addStretch()

        main_layout.addLayout(contract_layout)

        # -------------------------
        # Variables
        # -------------------------
        # main_layout.addWidget(
        #     QLabel("Template Variables")
        # )

        # self.variables_list = QListWidget()
        # self.variables_list.setMinimumHeight(180)

        # main_layout.addWidget(self.variables_list)

        # -------------------------
        # Next button
        # -------------------------
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()

        self.next_btn = QPushButton("Next ▶")
        self.next_btn.setEnabled(False)
        self.next_btn.clicked.connect(
            self.open_employee_selector
        )

        bottom_layout.addWidget(self.next_btn)

        main_layout.addLayout(bottom_layout)

        self.update_next_button()

    # ====================================================
    # File Selection
    # ====================================================

    def select_template(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Contract Template",
            "",
            "ODT Files (*.odt)"
        )

        if not filename:
            return

        self.template_edit.setText(filename)
        # self.load_template_variables(filename)
        self.update_next_button()

    def select_spreadsheet(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select Employee List Spreadsheet",
            "",
            "Spreadsheet Files (*.ods *.xlsx *.xls)"
        )

        if not filename:
            return

        self.sheet_edit.setText(filename)
        self.update_next_button()

    def update_next_button(self):
        enabled = (
            bool(self.template_edit.text())
            and bool(self.sheet_edit.text())
        )

        self.next_btn.setEnabled(enabled)

    def get_contract_type(self):
        if self.cdd_radio.isChecked():
            return "CDD"
        elif self.cdi_radio.isChecked():
            return "CDI"
        else:
            return None

    # ====================================================
    # ODT Variable Extraction
    # ====================================================

    def load_template_variables(self, odt_file):
        self.variables_list.clear()

        try:
            with zipfile.ZipFile(odt_file, "r") as zf:
                content = zf.read(
                    "content.xml"
                ).decode(
                    "utf-8",
                    errors="ignore"
                )



            variables = sorted(
                set(
                    re.findall(
                        r"\[\[([A-Za-z0-9_]+)\]\]",
                        content
                    )
                )
            )

            if not variables:
                self.variables_list.addItem(
                    "No variables found."
                )
                return

            for var in variables:
                self.variables_list.addItem(
                    f"{{{{{var}}}}}"
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Could not read template:\n\n{e}"
            )

    # ====================================================
    # Next Window
    # ====================================================

    def open_employee_selector(self):
        spreadsheet = self.sheet_edit.text()
        template = self.template_edit.text()
        contract_type = self.get_contract_type()
        
        self.employee_window = EmployeeSelectorWindow(
            # template=template,
            # spreadsheet=spreadsheet,
            # contract_type=contract_type
        )

        self.employee_window.show()
        self.close()