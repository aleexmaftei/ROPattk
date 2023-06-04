from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtWidgets import QFrame, QListWidgetItem, QLabel

from src.common.constGadgetDetailsTab import ConstGadgetDetailsTabTitle, ConstROPChainTabTitle
from src.enums.dataRole import DataRole
from src.utils.common import BeautifyAssemblyCodeFromText, ExtractUsedRegistersFromAssemblyCode


class CreateGadgetDetailsTab:
    def __init__(self, currentSelectedArchitecture: str):
        self._currentSelectedArchitecture = currentSelectedArchitecture

    def setSelectedGadgetDetails(self, currentItem: QListWidgetItem, oldItem: QListWidgetItem | None):
        newData = currentItem.data(DataRole.UserRole.value)

        self.offset_value.setText(newData['offset'])
        self.stack_size_2.setText(str(newData['size']))

        usedRegisters = ExtractUsedRegistersFromAssemblyCode(newData["gadget"], self._currentSelectedArchitecture)
        self.modified_registers.setText(", ".join(usedRegisters))

        assemblyCode = BeautifyAssemblyCodeFromText(newData["gadget"])
        self.assembly_code.setText(assemblyCode)

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
        frame_simple_details_wrapper = QtWidgets.QFrame(parent=frame_selected_gadget_details)
        frame_simple_details_wrapper.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        frame_simple_details_wrapper.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        frame_simple_details_wrapper.setObjectName("frame_simple_details_wrapper")
        verticalLayout_3 = QtWidgets.QVBoxLayout(frame_simple_details_wrapper)
        verticalLayout_3.setObjectName("verticalLayout_3")
        frame_for_offset = QtWidgets.QFrame(parent=frame_simple_details_wrapper)
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
        frame_for_used_registers = QtWidgets.QFrame(parent=frame_simple_details_wrapper)
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
        frame_for_stack_size = QtWidgets.QFrame(parent=frame_simple_details_wrapper)
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

        # Spacer
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum,
                                            QtWidgets.QSizePolicy.Policy.Expanding)
        verticalLayout_3.addItem(spacerItem3)
        horizontalLayout_4.addWidget(frame_simple_details_wrapper)

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

    def _createSecondTab(self):
        # Create the second tab
        ROPChain = QtWidgets.QWidget()
        ROPChain.setObjectName("ROPChain")

        return ROPChain

    def CreateUIGadgetDetails(self, frame: QFrame):
        # Create the frame where the tabs should reside
        GadgetDetails_Frame = QtWidgets.QFrame(parent=frame)
        GadgetDetails_Frame.setMinimumSize(QtCore.QSize(517, 250))
        GadgetDetails_Frame.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        GadgetDetails_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Plain)
        GadgetDetails_Frame.setObjectName("GadgetDetails_Frame")

        # Another vertical frame
        verticalLayout2 = QtWidgets.QVBoxLayout(GadgetDetails_Frame)
        verticalLayout2.setContentsMargins(0, 0, 0, 0)
        verticalLayout2.setSpacing(0)
        verticalLayout2.setObjectName("gadgetDetails_verticalLayout2")

        # Create the widget
        GadgetDetailsTabs = QtWidgets.QTabWidget(parent=GadgetDetails_Frame)
        GadgetDetailsTabs.setObjectName("GadgetDetailsTabs")

        # Create the first tab
        firstTab = self._createFirstTab()
        GadgetDetailsTabs.addTab(firstTab, ConstGadgetDetailsTabTitle)

        # Create the first tab
        secondTab = self._createSecondTab()
        GadgetDetailsTabs.addTab(secondTab, ConstROPChainTabTitle)

        verticalLayout2.addWidget(GadgetDetailsTabs)

        return GadgetDetails_Frame
