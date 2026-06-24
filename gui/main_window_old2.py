import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem, 
    QStackedWidget, QWidget, QVBoxLayout, QLabel, QSplitter, QStyle
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

# Import your standalone modular UI assets cleanly
from gui.sidebar_nav import SidebarNavigation
from gui.pages.employees_page import Employees
from gui.pages.settings_page import SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OV HR Management System")
        self.resize(1000, 650)
        
        self.init_ui()

    def init_ui(self):
        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.setCentralWidget(splitter)

        # Instantiate the navigation sidebar
        self.nav_tree = SidebarNavigation()
        splitter.addWidget(self.nav_tree)

        # Instantiate the dynamic central page stack container
        self.content_stack = QStackedWidget()
        splitter.addWidget(self.content_stack)
        
        self.page_map = {}
        contract_sub_items = [
            "Contract Types", "Salary Grid", "Bonuses", 
            "Departments", "Positions", "Work Locations", "Document Templates"
        ]
        all_pages = ["Employees", "Contract Settings"] + contract_sub_items + ["Settings"]

        for index, page_name in enumerate(all_pages):
            if page_name == "Employees":
                page_widget = Employees(parent=self)
                self.content_stack.addWidget(page_widget)
            elif page_name == "Settings":
                page_widget = SettingsPage(parent=self)
                self.content_stack.addWidget(page_widget)
            else:
                page_widget = self.create_placeholder_page(page_name)
                self.content_stack.addWidget(page_widget)
            self.page_map[page_name] = index

        splitter.setSizes([230, 770])
        self.nav_tree.itemClicked.connect(self.on_nav_changed)

    def create_placeholder_page(self, title):
        page = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"<h2>{title} Management View</h2>")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        page.setLayout(layout)
        return page

    def on_nav_changed(self, item, column):
        page_name = item.text(0)
        if page_name in self.page_map:
            self.content_stack.setCurrentIndex(self.page_map[page_name])
