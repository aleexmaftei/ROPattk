from PyQt6 import sip
from PyQt6.QtWidgets import QFrame

from src.common.constRegisterDetails import ConstRegisters


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


def DeleteUILayout(self, layout):
    if layout is not None:
        if not isinstance(layout, QFrame):
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
        sip.delete(layout)
