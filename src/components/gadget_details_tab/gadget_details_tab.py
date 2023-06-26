from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QFrame, QListWidgetItem

from src.common.constGadgetDetailsTab import ConstGadgetDetailsTabTitle, ConstROPChainTabTitle
from src.enums.dataRole import DataRole
from src.utils.common import BeautifyAssemblyCodeFromText, ExtractUsedRegistersFromAssemblyCode, DeleteUILayout
from src.utils.parseFile import WriteToFileDialog


class CreateGadgetDetailsTab:
    def __init__(self, currentSelectedArchitecture: str):
        self._currentSelectedArchitecture = currentSelectedArchitecture
        self._GadgetDetails_Frame = None
        self._listOfSelectedGadgets = []
        self._currentSelectedGadget = None
        self.frame_for_buttons = None
        self.GadgetDetailsTabs = None
        self.removeGadgetButton = None

    @property
    def GadgetDetails_Frame(self):
        return self._GadgetDetails_Frame

    def setSelectedGadgetDetails(self, currentItem: QListWidgetItem, oldItem: QListWidgetItem | None):
        newData = currentItem.data(DataRole.UserRole.value)
        self._currentSelectedGadget = newData

        self.offset_value.setText(newData['offset'])
        self.stack_size_2.setText(str(newData['size']))

        usedRegisters = ExtractUsedRegistersFromAssemblyCode(newData["gadget"], self._currentSelectedArchitecture)
        self.modified_registers.setText(", ".join(usedRegisters))

        assemblyCode = BeautifyAssemblyCodeFromText(newData["gadget"])
        self.assembly_code.setText(assemblyCode)

        if self.frame_for_buttons is not None:
            DeleteUILayout(self, self.frame_for_buttons, False)

            self.removeGadgetButton = QtWidgets.QPushButton(parent=self.frame_simple_details_wrapper)
            self.removeGadgetButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            self.removeGadgetButton.setObjectName("removeGadgetButton")
            self.removeGadgetButton.setText("Delete gadget")  # TODO: translations
            self.removeGadgetButton.clicked.connect(lambda x: self.__removeGadgetFromChain())
            self.frame_for_buttons.addWidget(self.removeGadgetButton)

            addGadgetButton = QtWidgets.QPushButton(parent=self.frame_simple_details_wrapper)
            addGadgetButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            addGadgetButton.setFlat(False)
            addGadgetButton.setObjectName("addGadgetButton")
            addGadgetButton.setText("Add gadget")  # TODO: translations
            addGadgetButton.clicked.connect(lambda x: self.__addGadgetToChain())
            self.frame_for_buttons.addWidget(addGadgetButton)

            # Disable the Remove button if the gadget is not in the list
            isAdded = False
            for selectedGadget in self._listOfSelectedGadgets:
                if selectedGadget["offset"] == self._currentSelectedGadget["offset"]:
                    isAdded = True
                    self.removeGadgetButton.setEnabled(True)
            if isAdded is False:
                self.removeGadgetButton.setEnabled(False)

    def _createFirstTab(self):
        # Create the first tab
        SelectedGadgetDetails = QtWidgets.QWidget()
        SelectedGadgetDetails.setObjectName("SelectedGadgetDetails")

        # Frames
        verticalLayout_6 = QtWidgets.QVBoxLayout(SelectedGadgetDetails)
        verticalLayout_6.setObjectName("verticalLayout_6")
        frame_selected_gadget_details = QtWidgets.QFrame(parent=SelectedGadgetDetails)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred,
                                           QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(frame_selected_gadget_details.sizePolicy().hasHeightForWidth())
        frame_selected_gadget_details.setSizePolicy(sizePolicy)
        frame_selected_gadget_details.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        frame_selected_gadget_details.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        frame_selected_gadget_details.setObjectName("frame_selected_gadget_details")
        horizontalLayout_4 = QtWidgets.QHBoxLayout(frame_selected_gadget_details)
        horizontalLayout_4.setObjectName("horizontalLayout_4")

        # Frame Wrapper
        self.frame_simple_details_wrapper = QtWidgets.QFrame(parent=frame_selected_gadget_details)
        self.frame_simple_details_wrapper.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.frame_simple_details_wrapper.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.frame_simple_details_wrapper.setObjectName("frame_simple_details_wrapper")
        verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_simple_details_wrapper)
        verticalLayout_3.setObjectName("verticalLayout_3")
        frame_for_offset = QtWidgets.QFrame(parent=self.frame_simple_details_wrapper)
        font = QtGui.QFont()
        font.setPointSize(11)
        frame_for_offset.setFont(font)
        frame_for_offset.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        frame_for_offset.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        frame_for_offset.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        frame_for_offset.setObjectName("frame_for_offset")
        horizontalLayout = QtWidgets.QHBoxLayout(frame_for_offset)
        horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        horizontalLayout.setObjectName("horizontalLayout")

        # Frame + Label keyword "Offset"
        offset_keyword = QtWidgets.QLabel(parent=frame_for_offset)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        offset_keyword.setFont(font)
        offset_keyword.setWordWrap(True)
        offset_keyword.setObjectName("offset_keyword")
        offset_keyword.setText("Address:")  # TODO: translation
        horizontalLayout.addWidget(offset_keyword)

        # Frame + Dynamic offset text taken from file
        self.offset_value = QtWidgets.QLabel(parent=frame_for_offset)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.offset_value.setFont(font)
        self.offset_value.setWordWrap(True)
        self.offset_value.setObjectName("offset_value")
        horizontalLayout.addWidget(self.offset_value)

        # Spacing
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout.addItem(spacerItem)
        verticalLayout_3.addWidget(frame_for_offset)

        # Frame wrapper for used registers
        frame_for_used_registers = QtWidgets.QFrame(parent=self.frame_simple_details_wrapper)
        frame_for_used_registers.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        frame_for_used_registers.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        frame_for_used_registers.setObjectName("frame_for_used_registers")
        horizontalLayout_2 = QtWidgets.QHBoxLayout(frame_for_used_registers)
        horizontalLayout_2.setContentsMargins(-1, 0, -1, 0)
        horizontalLayout_2.setObjectName("horizontalLayout_2")

        # Frame + Label keyword "Modified registers"
        modified_registers_keyword = QtWidgets.QLabel(parent=frame_for_used_registers)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        modified_registers_keyword.setFont(font)
        modified_registers_keyword.setWordWrap(True)
        modified_registers_keyword.setIndent(-1)
        modified_registers_keyword.setObjectName("modified_registers_keyword")
        modified_registers_keyword.setText("Modified Registers:")  # TODO: translations
        horizontalLayout_2.addWidget(modified_registers_keyword)

        # Dynamic modified registers text taken from file
        self.modified_registers = QtWidgets.QLabel(parent=frame_for_used_registers)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.modified_registers.setFont(font)
        self.modified_registers.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.modified_registers.setWordWrap(True)
        self.modified_registers.setObjectName("modified_registers")
        horizontalLayout_2.addWidget(self.modified_registers)

        # Spacer
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Policy.MinimumExpanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout_2.addItem(spacerItem1)
        verticalLayout_3.addWidget(frame_for_used_registers)

        # Frame + Label keyword "Stack size"
        frame_for_stack_size = QtWidgets.QFrame(parent=self.frame_simple_details_wrapper)
        frame_for_stack_size.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        frame_for_stack_size.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        frame_for_stack_size.setObjectName("frame_for_stack_size")
        horizontalLayout_3 = QtWidgets.QHBoxLayout(frame_for_stack_size)
        horizontalLayout_3.setContentsMargins(-1, 0, -1, 0)
        horizontalLayout_3.setSpacing(6)
        horizontalLayout_3.setObjectName("horizontalLayout_3")
        stack_size = QtWidgets.QLabel(parent=frame_for_stack_size)
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        stack_size.setFont(font)
        stack_size.setWordWrap(True)
        stack_size.setObjectName("stack_size")
        stack_size.setText("Gadget Size:")
        horizontalLayout_3.addWidget(stack_size)

        # Dynamic stack size text calculated from gadget
        self.stack_size_2 = QtWidgets.QLabel(parent=frame_for_stack_size)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.stack_size_2.setFont(font)
        self.stack_size_2.setWordWrap(True)
        self.stack_size_2.setObjectName("stack_size_2")
        horizontalLayout_3.addWidget(self.stack_size_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding,
                                            QtWidgets.QSizePolicy.Policy.Minimum)
        horizontalLayout_3.addItem(spacerItem2)
        verticalLayout_3.addWidget(frame_for_stack_size)

        # Add/remove buttons frame
        self.frame_for_buttons = QtWidgets.QHBoxLayout()
        self.frame_for_buttons.setContentsMargins(-1, 20, -1, -1)
        self.frame_for_buttons.setObjectName("frame_for_buttons")
        verticalLayout_3.addLayout(self.frame_for_buttons)

        # Spacer
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        verticalLayout_3.addItem(spacerItem3)
        horizontalLayout_4.addWidget(self.frame_simple_details_wrapper)

        # Frame with assembly code
        frame_assembly_wrapper = QtWidgets.QFrame(parent=frame_selected_gadget_details)
        frame_assembly_wrapper.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        frame_assembly_wrapper.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        frame_assembly_wrapper.setObjectName("frame_assembly_wrapper")
        horizontalLayout_7 = QtWidgets.QHBoxLayout(frame_assembly_wrapper)
        horizontalLayout_7.setObjectName("horizontalLayout_7")

        # Scrollable area
        scrollArea = QtWidgets.QScrollArea(parent=frame_assembly_wrapper)
        scrollArea.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        scrollArea.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        scrollArea.setWidgetResizable(True)
        scrollArea.setAlignment(QtCore.Qt.AlignmentFlag.AlignJustify | QtCore.Qt.AlignmentFlag.AlignTop)
        scrollArea.setObjectName("scrollArea")
        scroll_for_assembly_code = QtWidgets.QWidget()
        scroll_for_assembly_code.setGeometry(QtCore.QRect(0, 0, 450, 266))
        scroll_for_assembly_code.setObjectName("scroll_for_assembly_code")
        verticalLayout_5 = QtWidgets.QVBoxLayout(scroll_for_assembly_code)
        verticalLayout_5.setObjectName("verticalLayout_5")

        # Dynamic assembly code from gadget
        self.assembly_code = QtWidgets.QLabel(parent=scroll_for_assembly_code)
        self.assembly_code.setBaseSize(QtCore.QSize(1, 0))
        self.assembly_code.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.assembly_code.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.assembly_code.setObjectName("assembly_code")
        verticalLayout_5.addWidget(self.assembly_code)
        scrollArea.setWidget(scroll_for_assembly_code)
        horizontalLayout_7.addWidget(scrollArea)
        horizontalLayout_4.addWidget(frame_assembly_wrapper)
        verticalLayout_6.addWidget(frame_selected_gadget_details)

        return SelectedGadgetDetails

    def __inputTextChanged(self, uuid, register, x):
        print(uuid, register, x)

    def __addGadgetToChain(self):
        if self._currentSelectedGadget is None:
            return

        if len(self._listOfSelectedGadgets) == 0:
            self.GadgetDetailsTabs.setTabEnabled(1, True)

        # Enable the Remove button
        if self.removeGadgetButton is not None:
            self.removeGadgetButton.setEnabled(True)

        gadgetUuid = self._currentSelectedGadget["gadgetUuid"]
        self._listOfSelectedGadgets.append(self._currentSelectedGadget)

        gadget = QtWidgets.QWidget(parent=self.gadget_list_wrapper)
        gadget.setObjectName(f"gadget_{gadgetUuid}")

        verticalLayout = QtWidgets.QVBoxLayout(gadget)
        verticalLayout.setObjectName(f"verticalLayout_{gadgetUuid}")

        scrollArea_gadget = QtWidgets.QScrollArea(parent=gadget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(scrollArea_gadget.sizePolicy().hasHeightForWidth())
        scrollArea_gadget.setSizePolicy(sizePolicy)
        scrollArea_gadget.setMaximumSize(QtCore.QSize(350, 120))
        scrollArea_gadget.setStyleSheet("margin-bottom: 0;")
        scrollArea_gadget.setWidgetResizable(True)
        scrollArea_gadget.setObjectName(f"scrollArea_gadget_{gadgetUuid}")
        scrollAreaWidgetContents_gadget = QtWidgets.QWidget()
        scrollAreaWidgetContents_gadget.setGeometry(QtCore.QRect(0, 0, 342, 108))
        scrollAreaWidgetContents_gadget.setObjectName(f"scrollAreaWidgetContents_gadget_{gadgetUuid}")

        verticalLayout_2 = QtWidgets.QVBoxLayout(scrollAreaWidgetContents_gadget)
        verticalLayout_2.setObjectName(f"verticalLayout2_{gadgetUuid}")

        assembly_code_gadget = QtWidgets.QLabel(parent=scrollAreaWidgetContents_gadget)
        assembly_code_gadget.setObjectName(f"assembly_code_gadget_{gadgetUuid}")
        assembly_code_gadget.setText(BeautifyAssemblyCodeFromText(self._currentSelectedGadget["gadget"]))

        verticalLayout_2.addWidget(assembly_code_gadget)
        scrollArea_gadget.setWidget(scrollAreaWidgetContents_gadget)
        verticalLayout.addWidget(scrollArea_gadget)

        index = 0
        for register in self._currentSelectedGadget["dataForRegisters"]:
            user_input_gadget = QtWidgets.QTextEdit(parent=gadget)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                               QtWidgets.QSizePolicy.Policy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(user_input_gadget.sizePolicy().hasHeightForWidth())
            user_input_gadget.setSizePolicy(sizePolicy)
            user_input_gadget.setMaximumSize(QtCore.QSize(16777215, 30))
            user_input_gadget.setObjectName(f"user_input_gadget_{gadgetUuid}_{index}")
            user_input_gadget.setPlaceholderText(f"Data on Stack for register {register}")  # TODO: translations

            verticalLayout.addWidget(user_input_gadget)
            index = index + 1

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        verticalLayout.addItem(spacerItem)

        self.scrollArea_wrapper.setWidget(self.gadget_list_wrapper)
        self.horizontalLayout_5.addWidget(gadget)

    def __exportROPChain(self):
        ROPstring = "\n\nbufferLength=...\n" \
                    "returnAddressOverflowValue='BBBB'\n\n" \
                    "print('A'*bufferLength + \n" \
                    "returnAddressOverflowValue + \n"
        for selectedGadget in self._listOfSelectedGadgets:
            index = 0
            for register in selectedGadget["dataForRegisters"]:
                userTextInput = self.gadget_list_wrapper.findChild(QtWidgets.QTextEdit,
                                                                   f"user_input_gadget_{selectedGadget['gadgetUuid']}_{index}")
                ROPstring += f"'{userTextInput.toPlainText()}'"

                if index != len(selectedGadget["dataForRegisters"]) - 1:
                    ROPstring += ' + \n'
                index = index + 1
        ROPstring += ")"

        WriteToFileDialog(ROPstring)

    def __removeGadgetFromChain(self):
        for selectedGadget in self._listOfSelectedGadgets:
            if self._currentSelectedGadget["offset"] == selectedGadget["offset"]:
                self._listOfSelectedGadgets.remove(selectedGadget)
                gadgetToDelete = self.gadget_list_wrapper.findChild(QtWidgets.QWidget,
                                                                    f"gadget_{selectedGadget['gadgetUuid']}")
                DeleteUILayout(self, gadgetToDelete)

                # Disable Remove Button
                self.removeGadgetButton.setEnabled(False)

                # Disable ROPChain tab
                if len(self._listOfSelectedGadgets) == 0:
                    self.GadgetDetailsTabs.setTabEnabled(1, False)

    def _createSecondTab(self):
        # Create the second tab
        ROPChain = QtWidgets.QWidget()
        ROPChain.setObjectName("ROPChain")

        verticalLayout_7 = QtWidgets.QVBoxLayout(ROPChain)
        verticalLayout_7.setObjectName("verticalLayout_7")

        frame_wrapper = QtWidgets.QFrame(parent=ROPChain)
        frame_wrapper.setAutoFillBackground(False)
        frame_wrapper.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        frame_wrapper.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        frame_wrapper.setLineWidth(0)
        frame_wrapper.setObjectName("frame_wrapper")

        verticalLayout_9 = QtWidgets.QVBoxLayout(frame_wrapper)
        verticalLayout_9.setObjectName("verticalLayout_9")

        self.scrollArea_wrapper = QtWidgets.QScrollArea(parent=frame_wrapper)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding,
                                           QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea_wrapper.sizePolicy().hasHeightForWidth())
        self.scrollArea_wrapper.setSizePolicy(sizePolicy)
        self.scrollArea_wrapper.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.scrollArea_wrapper.setStyleSheet("QScrollArea { background-color:transparent; margin-bottom: 12px }")
        self.scrollArea_wrapper.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.scrollArea_wrapper.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self.scrollArea_wrapper.setWidgetResizable(True)
        self.scrollArea_wrapper.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeading | QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop)
        self.scrollArea_wrapper.setObjectName("scrollArea_wrapper")

        self.gadget_list_wrapper = QtWidgets.QWidget()
        self.gadget_list_wrapper.setGeometry(QtCore.QRect(0, 0, 1134, 260))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gadget_list_wrapper.sizePolicy().hasHeightForWidth())
        self.gadget_list_wrapper.setSizePolicy(sizePolicy)
        self.gadget_list_wrapper.setObjectName("gadget_list_wrapper")

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.gadget_list_wrapper)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        exportGadgetChain = QtWidgets.QPushButton(parent=frame_wrapper)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(exportGadgetChain.sizePolicy().hasHeightForWidth())
        exportGadgetChain.setSizePolicy(sizePolicy)
        exportGadgetChain.setMaximumSize(QtCore.QSize(16777215, 16777215))
        exportGadgetChain.setStyleSheet("background-color: green;\n"
                                        "color: black;")
        exportGadgetChain.setObjectName("exportGadgetChain")
        exportGadgetChain.setText("Export chain")  # TODO: translations
        exportGadgetChain.clicked.connect(lambda: self.__exportROPChain())

        verticalLayout_9.addWidget(self.scrollArea_wrapper)
        verticalLayout_9.addWidget(exportGadgetChain)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        verticalLayout_9.addItem(spacerItem8)
        verticalLayout_7.addWidget(frame_wrapper)

        return ROPChain

    def CreateUIGadgetDetails(self, frame: QFrame):
        # Create the frame where the tabs should reside
        self._GadgetDetails_Frame = QtWidgets.QFrame(parent=frame)
        self._GadgetDetails_Frame.setMinimumSize(QtCore.QSize(517, 250))
        self._GadgetDetails_Frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self._GadgetDetails_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        self._GadgetDetails_Frame.setObjectName("GadgetDetails_Frame")

        # Another vertical frame
        verticalLayout2 = QtWidgets.QVBoxLayout(self._GadgetDetails_Frame)
        verticalLayout2.setContentsMargins(0, 0, 0, 0)
        verticalLayout2.setSpacing(0)
        verticalLayout2.setObjectName("gadgetDetails_verticalLayout2")

        # Create the widget
        self.GadgetDetailsTabs = QtWidgets.QTabWidget(parent=self._GadgetDetails_Frame)
        self.GadgetDetailsTabs.setObjectName("GadgetDetailsTabs")

        # Create the first tab
        firstTab = self._createFirstTab()
        self.GadgetDetailsTabs.addTab(firstTab, ConstGadgetDetailsTabTitle)

        # Create the first tab
        secondTab = self._createSecondTab()
        self.GadgetDetailsTabs.addTab(secondTab, ConstROPChainTabTitle)
        self.GadgetDetailsTabs.setTabEnabled(1, False)

        verticalLayout2.addWidget(self.GadgetDetailsTabs)

        return self._GadgetDetails_Frame
