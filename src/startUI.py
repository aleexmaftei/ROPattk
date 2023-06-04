import sys
from PyQt6.QtWidgets import *
from src.components.main_window.main_window import Ui_MainWindow


def StartUIApplication(architectureName: str):
    app = QApplication(sys.argv)

    mainWindow = QMainWindow(None)
    Ui_MainWindow(mainWindow, architectureName)

    mainWindow.show()

    sys.exit(app.exec())

