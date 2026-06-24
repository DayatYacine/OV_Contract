from PyQt6.QtWidgets import QTreeWidget, QTreeWidgetItem, QApplication, QStyle

class SidebarNavigation(QTreeWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderHidden(True)  # Keeps title clean and hidden
        self.setColumnCount(1)
        self.populate_tree()
        
    def populate_tree(self):
        style = QApplication.style()
        
        # 1. Top-level standalone item: Employees
        self.employees_item = QTreeWidgetItem(self, ["Employees"])
        self.employees_item.setIcon(0, style.standardIcon(QStyle.StandardPixmap.SP_DialogHelpButton))
        
        # 2. Top-level folder item: Contract Settings
        self.contract_settings_item = QTreeWidgetItem(self, ["Contract Settings"])
        self.contract_settings_item.setIcon(0, style.standardIcon(QStyle.StandardPixmap.SP_DirIcon))
        
        # 3. Child items nested cleanly INSIDE Contract Settings
        sub_items = [
            "Contract Types", 
            "Salary Grid", 
            "Bonuses", 
            "Departments", 
            "Positions", 
            "Work Locations", 
            "Document Templates"
        ]
        
        for name in sub_items:
            # Notice we pass 'self.contract_settings_item' instead of 'self' 
            # to make it a sub-item child branch
            child = QTreeWidgetItem(self.contract_settings_item, [name])
            child.setIcon(0, style.standardIcon(QStyle.StandardPixmap.SP_FileIcon))
            
        # 4. Top-level standalone item: Settings
        self.settings_item = QTreeWidgetItem(self, ["Settings"])
        self.settings_item.setIcon(0, style.standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        
        # Force expand the parent category immediately so the branch layout is fully visible on launch
        self.contract_settings_item.setExpanded(True)