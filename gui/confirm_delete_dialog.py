from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class ConfirmDeleteDialog(QDialog):
    def __init__(self, employee_name, matricule, parent=None):
        super().__init__(parent)
        
        # Window configuration
        self.setWindowTitle("Confirm Action")
        self.setFixedSize(320, 150)  # Locked size to match a standard modal dialog
        # Standard modal flag (hides window minimize/maximize buttons)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowContextHelpButtonHint)

        # Main Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # 1. Message Labels
        title_label = QLabel("Delete employee?")
        title_label.setStyleSheet("font-size: 14px; color: #333333;")
        
        # Bold details layout matching your mockup
        details_label = QLabel(f"<b>{employee_name} ({matricule})</b>")
        details_label.setStyleSheet("font-size: 13px; color: #d32f2f;")  # Subtle crimson error color
        
        layout.addWidget(title_label)
        layout.addWidget(details_label)
        layout.addStretch()

        # 2. Action Buttons Row
        btn_layout = QHBoxLayout()
        
        self.btn_delete = QPushButton("Delete")
        self.btn_cancel = QPushButton("Cancel")
        
        # Style choices: Make delete stand out as a destructive action
        self.btn_delete.setStyleSheet("""
            QPushButton {
                background-color: #d32f2f; 
                color: white; 
                font-weight: bold; 
                padding: 6px 15px; 
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #b71c1c; }
        """)
        self.btn_cancel.setStyleSheet("padding: 6px 15px;")

        # Connect core dialog loop handlers
        self.btn_delete.clicked.connect(self.accept)  # Returns QDialog.DialogCode.Accepted
        self.btn_cancel.clicked.connect(self.reject)  # Returns QDialog.DialogCode.Rejected

        # Add to button layout (Left-aligned as drawn in your mockup)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addStretch()  # Pushes everything nicely to the left side

        layout.addLayout(btn_layout)