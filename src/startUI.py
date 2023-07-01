import sys
from PyQt6.QtWidgets import *
from src.components.main_window.main_window import Ui_MainWindow


def StartUIApplication():
    try:
        app = QApplication(sys.argv)

        mainWindow = QMainWindow(None)
        Ui_MainWindow(mainWindow)

        mainWindow.show()

        sys.exit(app.exec())
    except Exception as err:
        print("Unexpected error", repr(err))

