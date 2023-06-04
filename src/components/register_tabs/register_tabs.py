from typing import Callable
from PyQt6.QtWidgets import QFrame, QListWidget, QListWidgetItem
from PyQt6 import QtCore, QtWidgets
from src.common.constRegisterDetails import ConstRegisters
from src.common.constants import REGISTERS_TAB_FRAME_OBJECT_NAME, REGISTERS_TAB_WIDGET_OBJECT_NAME
from src.enums.dataRole import DataRole


class CreateRegisterTabs:
    def __init__(self):
        self._gadgetWidgetListGroupedByRegister = []
        self._Registers_Frame = None

    @property
    def Registers_Frame(self):
        return self._Registers_Frame
    
    @property
    def gadgetListGroupedByTabs(self) -> list[QListWidget]:
        return self._gadgetWidgetListGroupedByRegister

    def setSameEventForEachTab(self, eventFunction: Callable[[QListWidgetItem, QListWidgetItem | None], None]):
        for gadgetWidget in self.gadgetListGroupedByTabs:
            gadgetWidget.currentItemChanged.connect(lambda currentItem, oldItem: eventFunction(currentItem, oldItem))

    def disconnectAllEvents(self):
        for gadgetWidget in self.gadgetListGroupedByTabs:
            gadgetWidget.currentItemChanged.disconnect()

    def AddGadgetsToUI(self, instructionList: dict[str, list[dict[str, str]]], currentSelectedArchitecture: str, ):
        RegistersDictionary = ConstRegisters[currentSelectedArchitecture]
        tabIndex = 0
        firstTabEnabled = None
        for registerKey in RegistersDictionary:
            register = RegistersDictionary[registerKey]
            # Create a tab for a single register
            CurrentRegister_Widget = QtWidgets.QWidget()
            # Check if register is used in any instruction and disable the content if it is not used
            isRegisterUsed = len(instructionList[register["name"]]) != 0
            CurrentRegister_Widget.setEnabled(isRegisterUsed)
            CurrentRegister_Widget.setObjectName(register["name"])

            # Create the main grid layout for displaying the assembly instructions in frames
            mainGridLayout = QtWidgets.QGridLayout(CurrentRegister_Widget)
            mainGridLayout.setObjectName(f"mainGridLayoutFor_{register['name']}")

            # Create the frame where the list will reside
            list_Frame = QtWidgets.QFrame(parent=CurrentRegister_Widget)
            ## Frame settings
            list_Frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
            list_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
            list_Frame.setObjectName(f"listFrameFor_{register['name']}")

            # Create a frame for the list
            listGridLayout = QtWidgets.QGridLayout(list_Frame)
            listGridLayout.setContentsMargins(0, 6, 0, 6)
            listGridLayout.setObjectName(f"listGridLayoutFor_{register['name']}")

            # List widget
            list_Widget = QtWidgets.QListWidget(parent=list_Frame)
            ## List widget settings
            list_Widget.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
            list_Widget.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
            list_Widget.setProperty("showDropIndicator", False)
            list_Widget.setViewMode(QtWidgets.QListView.ViewMode.ListMode)
            list_Widget.setObjectName(f"listWidgetFor_{register['name']}")

            # Actual list with items (instructions in our case)
            if register['name'] in instructionList:
                for instructionObject in instructionList[register['name']]:
                    listItemWidget = QtWidgets.QListWidgetItem()
                    listItemWidget.setText(instructionObject["gadget"])
                    listItemWidget.setData(DataRole.UserRole.value, instructionObject)
                    list_Widget.addItem(listItemWidget)

            self._gadgetWidgetListGroupedByRegister.append(list_Widget)

            # Add the tab to frames
            listGridLayout.addWidget(list_Widget, 0, 0, 1, 1)
            mainGridLayout.addWidget(list_Frame, 0, 0, 1, 1)
            self.RegistersTabs_Widget.addTab(CurrentRegister_Widget, register['name'])

            if not isRegisterUsed:
                self.RegistersTabs_Widget.setTabEnabled(tabIndex, False)
            elif firstTabEnabled is None:
                firstTabEnabled = tabIndex

            tabIndex = tabIndex + 1

        self.verticalLayout2.addWidget(self.RegistersTabs_Widget)

        # Set the first tab as startup index
        self.RegistersTabs_Widget.setCurrentIndex(firstTabEnabled)

    def CreateUITabsByArchitecture(
            self,
            currentSelectedArchitecture: str,
            frame: QFrame,
            instructionList: dict[str, list[dict[str, str]]],
            registersFrameObjectName: str = REGISTERS_TAB_FRAME_OBJECT_NAME,
            registerWidgetObjectName: str = REGISTERS_TAB_WIDGET_OBJECT_NAME
    ):
        # Create the frame where the tabs should reside
        self._Registers_Frame = QtWidgets.QFrame(parent=frame)
        self._Registers_Frame.setMinimumSize(QtCore.QSize(517, 365))
        self._Registers_Frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self._Registers_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self._Registers_Frame.setObjectName(registersFrameObjectName)

        # Another vertical frame
        self.verticalLayout2 = QtWidgets.QVBoxLayout(self._Registers_Frame)
        self.verticalLayout2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout2.setObjectName("verticalLayout2")

        # Create the widget
        self.RegistersTabs_Widget = QtWidgets.QTabWidget(parent=self._Registers_Frame)
        self.RegistersTabs_Widget.setObjectName(registerWidgetObjectName)

        self.AddGadgetsToUI(instructionList, currentSelectedArchitecture)

        return self._Registers_Frame
