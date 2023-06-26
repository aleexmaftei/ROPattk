from rop_src.architecture.architecture import Architecture
from rop_src.utils.common import toHex


class ROPGadget(object):
    def __init__(self, binary, section: str, architecture: Architecture):
        self._binary = binary  # TODO: is needed?
        self._architecture = architecture
        self._section = section
        self._gadget = ""
        self._lines = []
        self._bytes = bytearray([])
        self._hasGadgetReturnInstruction = False
        self._gadgetSize = 0

    @property
    def gadgetSize(self):
        return self._gadgetSize

    @gadgetSize.setter
    def gadgetSize(self, value):
        self._gadgetSize = value

    @property
    def gadget(self):
        return self._gadget

    @gadget.setter
    def gadget(self, value):
        self._gadget = value

    @property
    def lines(self):
        return self._lines

    @property
    def bytes(self):
        return self._bytes

    @bytes.setter
    def bytes(self, value):
        self._bytes = value

    @property
    def hasGadgetReturnInstruction(self):
        return self._hasGadgetReturnInstruction

    @hasGadgetReturnInstruction.setter
    def hasGadgetReturnInstruction(self, value):
        self._hasGadgetReturnInstruction = value

    def getImageBaseForGadget(self):
        return self._binary.imageBase + self._getAddressFromLine()

    def getImageBaseForGadgetParsedInHex(self):
        return toHex(self._binary.imageBase + self._getAddressFromLine(), self._architecture.instructionSize)

    def _getAddressFromLine(self):
        return self.lines[0][0]

    def append(self, instructionAddress, mnemonic, args='', bytes=None):
        if args:
            self._lines.append(
                (instructionAddress, mnemonic + ' ' + args, mnemonic, args))
            self.gadget += mnemonic + ' ' + args + '; '
        else:
            self._lines.append((instructionAddress, mnemonic, mnemonic, args))
            self.gadget += mnemonic + '; '

        if bytes:
            self.bytes += bytes
