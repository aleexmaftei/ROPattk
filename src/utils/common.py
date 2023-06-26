from PyQt6 import sip
from PyQt6.QtWidgets import QFrame, QWidget

from src.common.constRegisterDetails import ConstRegisters, ConstRegisterModificationMnemonics


def BeautifyAssemblyCodeFromText(assmString: str) -> str:
    toReturn = ""
    splitLineInstructionList = assmString.split(";")
    for singleInstruction in splitLineInstructionList:
        toReturn += singleInstruction.strip()
        toReturn += "\n"

    return toReturn


def ExtractUsedRegistersFromAssemblyCode(assmString: str, architecture: str) -> list[str]:
    usedRegisters = []
    RegistersDictionary = ConstRegisters[architecture]
    for registerKey in RegistersDictionary:
        registerName = RegistersDictionary[registerKey]["name"].lower()
        lowerAssmString = assmString.lower()

        if registerName in lowerAssmString:
            usedRegisters.append(registerName)

    return usedRegisters


def ExtractNeededDataForRegisters(assmString: str, architecture: str) -> list[str]:
    registersThatNeedDataOnStack = []
    # Look into every instruction and get registers
    splitLineInstructionList = assmString.split(";")
    for singleInstruction in splitLineInstructionList:
        strippedSingleInstruction = singleInstruction.strip()
        # Find instructions that modifies the registers by architecture
        for modificationInstruction in ConstRegisterModificationMnemonics[architecture]:
            if modificationInstruction in strippedSingleInstruction:
                # Find the register used in the single instruction that modifies it
                RegistersDictionary = ConstRegisters[architecture]
                for registerKey in RegistersDictionary:
                    register = RegistersDictionary[registerKey]["name"]
                    if register.lower() in strippedSingleInstruction \
                            or register.upper() in strippedSingleInstruction:
                        registersThatNeedDataOnStack.append(register.lower())

    return registersThatNeedDataOnStack


def DeleteUILayout(self, layout, deleteParent=True):
    if layout is not None:
        if not isinstance(layout, QFrame) and not isinstance(layout, QWidget):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                elif hasattr(self, "deleteLayout"):
                    self.deleteLayout(item.layout())
        if deleteParent is True:
            sip.delete(layout)
