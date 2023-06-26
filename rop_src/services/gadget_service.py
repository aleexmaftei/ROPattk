import re

import capstone

from rop_src.enums.gadget_type import GadgetType
from rop_src.services.file_service import FileService
from rop_src.ROPGadget.ROPGadget import ROPGadget


class GadgetService(object):
    def __init__(self):
        super().__init__()

    def _prepareGadget(self, disassembler, architecture, code_str, codeStartAddress, ending, binary=None, section=None):
        disassambledCode = disassembler.disasm(code_str, codeStartAddress)

        ROPGadgetObj = ROPGadget(binary, section, architecture)

        for dissInstr in disassambledCode:
            if re.match(ending[0], dissInstr.bytes):
                ROPGadgetObj.hasGadgetReturnInstruction = True

            ROPGadgetObj.gadgetSize += dissInstr.size
            ROPGadgetObj.append(dissInstr.address, dissInstr.mnemonic, dissInstr.op_str, dissInstr.bytes)

        if ROPGadgetObj.hasGadgetReturnInstruction and len(ROPGadgetObj.lines) > 0:
            return ROPGadgetObj, len(ROPGadgetObj.lines)
        return None, -1

    def _searchForGadgetsInSection(self, section, binaryContent, architecture, gadgetType, instructionCount) \
            -> list[ROPGadget]:
        # main function for gadget findings
        toReturn = []
        code = bytes(bytearray(section.bytes))
        offset = section.offset - (binaryContent.imageBase - (section.virtualAddress - section.offset))

        cp = capstone.Cs(architecture.architectureType, architecture.architectureMode)
        virtualAddresses = set()
        for ending in architecture.gadgetEndings[gadgetType]:
            # ending = tuple of (ROP_instruction, instruction_alignment)
            offset_tmp = 0
            # Copy of the ELF file content
            tmp_code = code[:]

            # Search the code for the ROP possible instructions
            match = re.search(ending[0], tmp_code)
            while match:
                # Search where the instruction is located in the binary
                offset_tmp += match.start()
                index = match.start()

                # Check if the instruction is aligned with the architecture
                if offset_tmp % architecture.instructionAlignment == 0:
                    none_count = 0

                    for x in range(0, index + 1, architecture.instructionAlignment):
                        code_part = tmp_code[(index - x):(index + ending[1])]

                        gadget, leng = self._prepareGadget(cp, architecture, code_part, offset + offset_tmp - x, ending,
                                                           binaryContent, section.name)
                        if gadget:
                            if leng > instructionCount:
                                break
                            gadgetAddress = gadget.getImageBaseForGadget()
                            if gadgetAddress not in virtualAddresses:
                                virtualAddresses.update([gadgetAddress])
                                toReturn.append(gadget)
                            none_count = 0
                        else:
                            none_count += 1
                            if none_count == architecture.maxNumberInvalidInstructions:
                                break

                # Start searching from the next instruction of the previous ROP
                tmp_code = tmp_code[index + architecture.instructionAlignment:]
                offset_tmp += architecture.instructionAlignment

                # Find the next ROP
                match = re.search(ending[0], tmp_code)

        return toReturn

    def _searchForGadgets(self, gadgetType=GadgetType.ALL, instructionCount=5) -> list[list[ROPGadget]]:
        foundGadgets = []
        file = FileService.file
        executableSections = file.executableSections
        if 0 < len(executableSections):
            binaryContent = file.binaryContent
            for section in executableSections:
                gadgets = self._searchForGadgetsInSection(section, binaryContent, file.architecture, gadgetType,
                                                          instructionCount)
                if len(gadgets) > 0:
                    foundGadgets.append(gadgets)
        else:
            raise f"No executable sections for the file {file}"

        return foundGadgets

    def loadGadgets(self):
        if FileService.isFileLoaded():
            return self._searchForGadgets()
        else:
            raise "Can not load gadgets because there is no file loaded!"


GadgetService = GadgetService()
