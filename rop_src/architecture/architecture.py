from capstone.arm import CsArm
from filebytes import elf

from rop_src.architecture.ROP_instructions import ARMInstructionsROP
from rop_src.enums.endianness import Endianness
from rop_src.enums.gadget_type import GadgetType
from capstone import *


class Architecture(object):
    def __init__(self,
                 architecture: int,
                 mode: int,
                 instructionSize: int,
                 instructionAlignment: int,
                 endianness: Endianness = Endianness.LITTLE,
                 architectureName: str = ""):
        self._architecture = architecture
        self._mode = mode  # used for capstone disassemble and assemble
        self._architectureName = architectureName
        self._instructionSize = instructionSize
        self._instructionAlignment = instructionAlignment
        self._endianness = endianness

        self.__initGadgetEndings()
        self.__setGadgetEndingsEndianness(endianness)

        self._maxNumberInvalidInstructions = 1

    def __initGadgetEndings(self):
        self._gadgetEnding = {
            GadgetType.JOP: [],
            GadgetType.ROP: []
        }

    def __setGadgetEndingsEndianness(self, endianness):
        if endianness == Endianness.LITTLE:
            pass  # TODO: ?
        elif endianness == Endianness.BIG:
            pass

    @property
    def instructionSize(self):
        return self._instructionSize

    @property
    def maxNumberInvalidInstructions(self):
        return self._maxNumberInvalidInstructions

    @maxNumberInvalidInstructions.setter
    def maxNumberInvalidInstructions(self, value):
        self._maxNumberInvalidInstructions = value

    @property
    def architectureMode(self):
        return self._mode

    @property
    def architectureType(self):
        return self._architecture

    @property
    def instructionAlignment(self):
        return self._instructionAlignment

    @property
    def gadgetEndings(self):
        return self._gadgetEnding

    def setGadgetEndingsByType(self, gadgetType, value):
        self._gadgetEnding[gadgetType] = value


class ArchARM(Architecture):
    NAME = "ARM"
    INSTRUCTION_ALIGNMENT = 4
    INSTRUCTION_SIZE = 4

    def __init__(self, endianness=Endianness.LITTLE):
        super().__init__(CS_ARCH_ARM,
                         CS_MODE_ARM,
                         self.INSTRUCTION_SIZE,
                         self.INSTRUCTION_ALIGNMENT,
                         endianness,
                         self.NAME)

        self.setGadgetEndingsByType(GadgetType.JOP, ARMInstructionsROP.JOP_INSTR)
        self.setGadgetEndingsByType(GadgetType.ROP, ARMInstructionsROP.ROP_INSTR)
        self.setGadgetEndingsByType(GadgetType.ALL,
                                    self._gadgetEnding[GadgetType.JOP] +
                                    self._gadgetEnding[GadgetType.ROP])


ARM = ArchARM()
ARMBE = ArchARM()

ARCH = {
    (CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_BIG_ENDIAN): ARMBE,
    (CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_LITTLE_ENDIAN): ARM
}


def getArchitecture(arch: int, mode: int, endianness: int):
    arch = ARCH[(arch, mode, endianness)]
    if arch:
        initializedArch = globals().get(arch.NAME, None)

        if isinstance(initializedArch, Architecture):
            return initializedArch
    raise "Architecture is not implemented!"
