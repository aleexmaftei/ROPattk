from capstone import Cs, CsError
from rop_src.ROPGadget.ROPGadget import ROPGadget
from rop_src.architecture.architecture import getArchitecture
from rop_src.loaders.base_loader import BaseLoader
from rop_src.services.capstoneConstants import CapstonePossibleArchitectures, CapstonePossibleModes, \
    CapstonePossibleEndianness


class FileService(object):
    def __init__(self):
        self._file = None

    def deleteFile(self):
        del self._file
        self._file = None

    def addFile(self, filePath, architecture: int, mode: int, endianness: int):
        architectureClass = getArchitecture(architecture, mode, endianness)
        self.file = BaseLoader.loadFileByArchitecture(filePath, architectureClass)

    def isFileLoaded(self):
        return self.file is not None

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, value):
        self._file = value

    @staticmethod
    def writeGadgetsToFile(gadgets: list[list[ROPGadget]], path: str):
        toWrite = ""
        with open(path, "w") as file:
            for gadgetsFromOpenedFile in gadgets:
                for gadget in gadgetsFromOpenedFile:
                    toWrite += gadget.getImageBaseForGadgetParsedInHex() + ": "
                    for instruction in gadget.lines:
                        toWrite += instruction[1] + "; "
                    toWrite += f"~{gadget.gadgetSize} "
                    toWrite += "\n"
            if len(toWrite) > 0:
                file.write(toWrite)

    @staticmethod
    def findFileArchModeAndEndianness(path: str):
        with open(path, "rb") as file:
            binary = file.read()

        fileArch, fileMode = None, None
        for arch in CapstonePossibleArchitectures:
            for mode in CapstonePossibleModes:
                try:
                    cs = Cs(arch, mode)
                    cs.disasm_lite(binary, 0)
                    for endianness in CapstonePossibleEndianness:
                        cs2 = Cs(arch, endianness)
                        cs2.disasm_lite(binary, 0)
                        return arch, mode, endianness
                except CsError:
                    continue

        if fileArch is None or fileMode is None:
            raise "File has no known architecture or mode!"


FileService = FileService()
