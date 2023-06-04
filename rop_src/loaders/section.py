class Section(object):
    # Store details about the executable sections of the application
    def __init__(self, name, sectionBytes, virtualAddress, offset, struct=None):
        if type(name) == bytes:
            name = name.decode('ascii')
        self.name = name
        self.bytes = sectionBytes
        self.virtualAddress = virtualAddress
        self.offset = offset
        self.struct = struct

    @property
    def sectionSize(self):
        return len(self.bytes)
