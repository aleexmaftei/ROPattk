from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QMainWindow, QFileDialog
from rop_src.services.file_service import FileService
from rop_src.services.gadget_service import GadgetService
import os

from src.common.globalEventHandler import GlobalEventHandlerObject


class Menubar:
    def _openFile(self):
        file = QFileDialog.getOpenFileName()
        path = file[0]
        arch, mode, endianness = FileService.findFileArchModeAndEndianness(path)
        FileService.addFile(path, arch, mode, endianness)
        gadgets = GadgetService.loadGadgets()
        FileService.writeGadgetsToFile(gadgets, f"{os.getcwd()}/src/resources/instructions.txt")

        GlobalEventHandlerObject.dispatchEventWithParams("readGadgetsFile", FileService.architectureClass.NAME)

    def CreateUIMenubar(self, mainWindow: QMainWindow):
        menubar = QtWidgets.QMenuBar(parent=mainWindow)
        menubar.setGeometry(QtCore.QRect(0, 0, 829, 23))
        menubar.setObjectName("menubar")
        menuMenu = QtWidgets.QMenu(parent=menubar)
        menuMenu.setObjectName("menuMenu")
        menuMenu.setTitle("File")  # TODO: translations

        # Load file action
        actionLoad_file = QtGui.QAction(parent=mainWindow)
        actionLoad_file.setObjectName("actionLoad_file")
        actionLoad_file.setText("Load")  # TODO: translations
        actionLoad_file.triggered.connect(lambda: self._openFile())

        # Remove file action
        actionRemove_file = QtGui.QAction(parent=mainWindow)
        actionRemove_file.setObjectName("actionRemove_file")
        actionRemove_file.setText("Remove")  # TODO: translations

        # Add actions to menubar
        menuMenu.addAction(actionLoad_file)
        menuMenu.addAction(actionRemove_file)
        menubar.addAction(menuMenu.menuAction())

        return menubar
