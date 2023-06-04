from src.common.constRegisterDetails import ConstRegisters, ConstRegisterModificationMnemonics

GadgetsGroupedByRegister: dict[str, list[dict[str, str]]] = {}


def ParseInstructionLine(line: str, architecture: str):
    gadgetSplitBySize = line.split("~")
    splitLine = gadgetSplitBySize[0].split(":")
    offsetAddress = splitLine[0].strip()
    currentGadgetInstructions = splitLine[1].strip()

    # Look into every instruction and get registers
    splitLineInstructionList = currentGadgetInstructions.split(";")
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
                        gadgetSize = int(gadgetSplitBySize[1].strip())
                        obj = {
                            "offset": offsetAddress,
                            "gadget": currentGadgetInstructions,
                            "size": gadgetSize
                        }
                        GadgetsGroupedByRegister[register.upper()].append(obj)


def InitInstructionGroupedByRegisters(architecture: str):
    GadgetsGroupedByRegister.clear()
    RegistersDictionary = ConstRegisters[architecture]
    for registerKey in RegistersDictionary:
        register: str = RegistersDictionary[registerKey]["name"]
        # Create the object with registers by architecture (e.g. R0, R1 for ARM)
        GadgetsGroupedByRegister.update({register: []})


def sortGadgetsByLength():
    for registerKey in GadgetsGroupedByRegister:
        gadgetList = GadgetsGroupedByRegister[registerKey]
        gadgetList.sort(key=lambda x: x["size"])


def ReadFile(filePath: str, architecture: str):
    InitInstructionGroupedByRegisters(architecture)

    with open(filePath, "r") as file:
        lines = file.readlines()
        for line in lines:
            ParseInstructionLine(line, architecture)

    sortGadgetsByLength()
    return GadgetsGroupedByRegister
