from PyQt6.QtWidgets import (
    QApplication, QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QVBoxLayout, QWidget
)
from PyQt6.QtCore import Qt, QEvent


class FilterHeader(QHeaderView):
    def __init__(self, parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.filters = []
        self.filters_visible = False
        self.filter_lable_height = -1
        self.filter_input_height = -1

        self.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setMinimumSectionSize(150)

        self.sectionResized.connect(self.updatePositions)

    def sizeHint(self):
        # Get the original natural size hint (which works perfectly once rendered)
        base_size = super().sizeHint()

        # Check if filters list exists and if the first one is visible
        self.filters_visible = self.filters and self.filters[0].isVisible()
        
        if self.filters_visible:
            dummy = QLineEdit()
            input_height = dummy.sizeHint().height()
            dummy.deleteLater()

            self.filter_lable_height = base_size.height()
            self.filter_input_height = input_height
            
            # Expanded height (Text + Input + Padding)
            base_size.setHeight(base_size.height() + input_height + 6)
        else:
            # Default height (Just text + padding)
            base_size.setHeight(base_size.height())

        return base_size

    def setColumnCount(self, count):
        # Clear old filters if columns change dynamically
        for edit in self.filters:
            edit.deleteLater()
        self.filters.clear()

        for col in range(count):
            edit = QLineEdit(self)
            edit.setVisible(False)
            edit.setPlaceholderText("Filter...")
            # Optional: trigger a filtering function when text changes
            edit.textChanged.connect(self.filterTable)
            self.filters.append(edit)
        
        self.initializeSections()
        self.updateGeometries()
        self.updatePositions()

    def updatePositions(self):
        y = self.filter_lable_height + 3
        h = self.filter_input_height

        # print(y, h)

        for col, edit in enumerate(self.filters):
            if col >= self.count():
                continue
            
            # Get geometry relative to the header viewport
            x = self.sectionPosition(col)
            w = self.sectionSize(col)

            # Account for the current horizontal scroll offset
            # QHeaderView handles its own offset internally, but we must align widgets to it
            edit.setGeometry(x + 2 - self.offset(), y, w - 4, h)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updatePositions()

    def toggle_filters(self, visible: bool):
        """Shows or hides the filter input boxes and adjusts header height."""
        # self.clear_filters()

        self.filters_visible = visible

        for edit in self.filters:
            edit.setVisible(visible)

        self.setFixedHeight(self.sizeHint().height())
        
        self.updateGeometry()
        self.updateGeometries()
        self.viewport().update()

        table = self.parent()
        if table:
            table.updateGeometries()

        if visible:
            self.updatePositions()

    def clear_filters(self):
        """Resets all filter text fields to empty and restores row visibility."""
        # Block signals temporarily so we don't trigger filterTable() 
        # multiple times while clearing each box
        self.blockSignals(True)
        
        for edit in self.filters:
            edit.clear()
            
        self.blockSignals(False)
        
        # Trigger the filter logic one last time to unhide all rows
        self.filterTable()

    def filterTable(self):
        # Basic filtering logic placeholder
        table = self.parent()
        if not isinstance(table, QTableWidget):
            return

        for row in range(table.rowCount()):
            match = True
            for col, edit in enumerate(self.filters):
                filter_text = edit.text().lower()
                if filter_text:
                    item = table.item(row, col)
                    item_text = item.text().lower() if item else ""
                    if filter_text not in item_text:
                        match = False
                        break
            table.setRowHidden(row, not match)


# --- Example Usage ---
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Setup Main Window
    window = QWidget()
    layout = QVBoxLayout(window)

    # Create a toggle button
    toggle_btn = QPushButton("Toggle Filters")
    toggle_btn.setCheckable(True) # Makes the button stay pressed down
    layout.addWidget(toggle_btn)

    table = QTableWidget(5, 4)
    table.setSortingEnabled(True)
    layout.addWidget(table)

    # IMPORTANT: Initialize custom header FIRST before setting labels/counts
    header = FilterHeader(table)
    table.setHorizontalHeader(header)

    # Connect the button click to the header's new toggle function
    toggle_btn.toggled.connect(header.toggle_filters)

    # table.setHorizontalHeaderLabels([
    #     "Matricule",
    #     "First Name",
    #     "Last Name",
    #     "Department"
    # ])

    # 1. Define your labels
    labels = ["Matricule", "First Name", "Last Name", "Department"]
    table.setColumnCount(len(labels))

    # 2. Apply text alignment directly to the horizontal header items
    for col, text in enumerate(labels):
        item = QTableWidgetItem(text)
        
        # Align text to the Top and Center Horizontally
        item.setTextAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        
        table.setHorizontalHeaderItem(col, item)
    
    # Generate the filter inputs matching column count
    header.setColumnCount(table.columnCount())

    # 2. Connect to the horizontal scrollbar to update positions on scroll
    table.horizontalScrollBar().valueChanged.connect(header.updatePositions)

    table.setSortingEnabled(False)

    # Populate dummy data
    data = [
        ["MAT-1001", "Ahmed", "Benali", "IT"],
        ["MAT-1002", "Jane", "Doe", "HR"],
        ["MAT-1003", "John", "Smith", "IT"],
        ["MAT-1004", "Fatima", "Zahra", "Finance"],
        ["MAT-1005", "Alex", "Jones", "Marketing"],
    ]

    for row_idx, row_data in enumerate(data):
        for col_idx, text in enumerate(row_data):
            table.setItem(row_idx, col_idx, QTableWidgetItem(text))

    table.setSortingEnabled(True)
    table.horizontalHeader().setSectionsClickable(True)

    window.resize(600, 400)
    window.show()
    sys.exit(app.exec())