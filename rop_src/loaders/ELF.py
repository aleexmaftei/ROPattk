import filebytes.elf

from rop_src.architecture.architecture import Architecture, ARMBE, ARM
from rop_src.loaders.base_loader import BaseLoader
import filebytes.elf as elf

from rop_src.loaders.section import Section


class ELF(BaseLoader):
    def __init__(self, filePath: str, architecture: Architecture):
        super().__init__(filePath, architecture)
        self._executableSections = self._findExecutableSections()

    @property
    def executableSections(self):
        return self._executableSections

    def isFileFormatCorrect(self, filePath: str):
        return elf.ELF.isSupportedFile(filePath)

    def _findExecutableSections(self):
        def filterByExecutableSection(dataList: list, isSegmentHeader: bool):
            def isHeaderSegmentExecutable(data: filebytes.elf.PhdrData):
                # p_flags can be 0x1 (X), 0x2 (W), 0x4 (R) and combinations (e.g. 0x3 (XW))
                # we can apply "or" operation to find if it is executable
                return 0 < data.header.p_flags & elf.PF.EXEC

            def isSectionExecutable(data: filebytes.elf.ShdrData):
                # sh_flags can be SHF_WRITE, SHF_ALLOC, SHF_EXECINSTR, SHF_MASKPROC
                return 0 < data.header.sh_flags & elf.SHF.EXECINSTR

            return filter(lambda x: isHeaderSegmentExecutable(x) if isSegmentHeader else isSectionExecutable(x),
                          dataList)

        executableSections = []
        binaryContent: filebytes.elf.ELF = self.binaryContent
        if binaryContent.segments:
            filteredExecutableSegments = filterByExecutableSection(binaryContent.segments, True)
            for phdrData in filteredExecutableSegments:
                executableSections.append(
                    Section(
                        name=str(elf.PT[phdrData.header.p_type]),
                        sectionBytes=phdrData.raw,
                        virtualAddress=phdrData.header.p_vaddr,
                        offset=phdrData.header.p_offset)
                )
        elif binaryContent.sections:
            filteredExecutableSections = filterByExecutableSection(binaryContent.sections, False)
            for shdrData in filteredExecutableSections:
                executableSections.append(
                    Section(
                        name=shdrData.name,
                        sectionBytes=shdrData.raw,
                        virtualAddress=shdrData.header.sh_addr,
                        offset=shdrData.header.sh_offset)
                )
        return executableSections

    def _loadBinaryContent(self, filePath: str):
        return elf.ELF(filePath)

    def _getFileArchitectureModeAndEndianness(self):
        pass

