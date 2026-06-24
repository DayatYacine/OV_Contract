import sys
from PyQt6.QtWidgets import QApplication
from services.database import init_db
# from gui.main_window_old import MainWindow
# from gui.employee_selector import EmployeeSelectorWindow
from gui.main_window import MainWindow


def main():
    # Run database initialization before the GUI starts
    init_db()

    app = QApplication(sys.argv)

    # Optional
    app.setApplicationName("OV Contract")
    app.setOrganizationName("Oran Vert")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()