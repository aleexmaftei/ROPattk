from abc import ABC, abstractmethod

from rop_src.architecture.architecture import Architecture


class BaseLoader(ABC):
    def __init__(self, filePath: str, architecture: Architecture):
        super().__init__()
        self._filePath = filePath
        self._architecture = architecture
        self._binaryContent = self._loadBinaryContent(filePath)

    @classmethod
    def isFileFormatCorrect(cls, filePath):
        pass

    @property
    def imageBase(self):
        return self.binaryContent.imageBase

    @property
    def architecture(self):
        return self._architecture

    @property
    def binaryContent(self):
        return self._binaryContent

    @abstractmethod
    def _findExecutableSections(self):
        pass

    @abstractmethod
    def _loadBinaryContent(self, filePath: str):
        pass

    @abstractmethod
    def _getFileArchitectureModeAndEndianness(self):
        pass

    @classmethod
    def loadFileByArchitecture(cls, filePath: str, architecture: Architecture):
        try:
            childrenClasses = BaseLoader.__subclasses__()
            # Search if the file format is supported with implemented formats
            for childClass in childrenClasses:
                if childClass.isFileFormatCorrect(childClass, filePath):
                    return childClass(filePath, architecture)

            raise OSError()
        except OSError:
            print(f"File {filePath} not supported")

