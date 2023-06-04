import os
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from src.common.globalEventHandler import GlobalEventHandlerObject
from src.components.gadget_details_tab.gadget_details_tab import CreateGadgetDetailsTab
from src.components.menubar.menubar import Menubar
from src.utils.common import DeleteUILayout
from src.utils.parseFile import ReadFile
from src.components.register_tabs.register_tabs import CreateRegisterTabs


class Ui_MainWindow(object):
    def __init__(self, MainWindow: QMainWindow):
        self.__setupUi(MainWindow)
        self.createRegisterTabs = None
        self.createGadgetDetailsTab = None

    def __displayRegisterTabsAfterFileWrite(self, architectureName: str):
        if self.createRegisterTabs is not None:
            DeleteUILayout(self, self.createRegisterTabs.Registers_Frame)

        if self.createGadgetDetailsTab is not None:
            DeleteUILayout(self, self.createGadgetDetailsTab.GadgetDetails_Frame)

        # Create register tab window
        instructionList = ReadFile(f"{os.getcwd()}/src/resources/instructions.txt", architectureName)
        self.createRegisterTabs = CreateRegisterTabs()
        Registers_Frame = self.createRegisterTabs.CreateUITabsByArchitecture(
            currentSelectedArchitecture=architectureName,
            frame=self.Right_Frame,
            instructionList=instructionList)

        # Gadget details tab window
        self.createGadgetDetailsTab = CreateGadgetDetailsTab(currentSelectedArchitecture=architectureName)
        GadgetDetails_Frame = self.createGadgetDetailsTab.CreateUIGadgetDetails(frame=self.Right_Frame)

        self.createRegisterTabs.setSameEventForEachTab(self.createGadgetDetailsTab.setSelectedGadgetDetails)

        # Add widgets
        self.verticalLayout.addWidget(Registers_Frame)
        self.verticalLayout.addWidget(GadgetDetails_Frame)

    def __setupUi(self, MainWindow: QMainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(829, 724)

        # Create menubar widget
        MenuBar = Menubar()
        menubar = MenuBar.CreateUIMenubar(mainWindow=MainWindow)
        MainWindow.setMenuBar(menubar)

        self.Central_Widget = QtWidgets.QWidget(parent=MainWindow)
        self.Central_Widget.setObjectName("Central_Widget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Central_Widget)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.Left_Frame = QtWidgets.QFrame(parent=self.Central_Widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Left_Frame.sizePolicy().hasHeightForWidth())
        self.Left_Frame.setSizePolicy(sizePolicy)
        self.Left_Frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.Left_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.Left_Frame.setObjectName("Left_Frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Left_Frame)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(9, 9, 0, 0)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.SettingsTabs = QtWidgets.QTabWidget(parent=self.Left_Frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SettingsTabs.sizePolicy().hasHeightForWidth())
        self.SettingsTabs.setSizePolicy(sizePolicy)
        self.SettingsTabs.setMinimumSize(QtCore.QSize(150, 0))
        self.SettingsTabs.setObjectName("SettingsTabs")
        self.FilterRegisters = QtWidgets.QWidget()
        self.FilterRegisters.setObjectName("FilterRegisters")
        self.SettingsTabs.addTab(self.FilterRegisters, "")
        self.horizontalLayout.addWidget(self.SettingsTabs)
        self.gridLayout_3.addWidget(self.Left_Frame, 0, 0, 1, 1)

        self.Right_Frame = QtWidgets.QFrame(parent=self.Central_Widget)
        self.Right_Frame.setMinimumSize(QtCore.QSize(0, 0))
        self.Right_Frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.Right_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.Right_Frame.setObjectName("Right_Frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Right_Frame)
        self.verticalLayout.setContentsMargins(0, 9, 9, 0)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")

        GlobalEventHandlerObject.addEventListener("readGadgetsFile", self.__displayRegisterTabsAfterFileWrite)

        self.gridLayout_3.addWidget(self.Right_Frame, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.Central_Widget)

        self.__retranslateUi(MainWindow)
        self.SettingsTabs.setCurrentIndex(0)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def __retranslateUi(self, MainWindow: QMainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.SettingsTabs.setTabText(self.SettingsTabs.indexOf(self.FilterRegisters),
                                     _translate("MainWindow", "Filter"))
