from enum import Enum

from capstone import CS_MODE_BIG_ENDIAN, CS_MODE_LITTLE_ENDIAN


class Endianness(Enum):
    BIG = CS_MODE_BIG_ENDIAN,
    LITTLE = CS_MODE_LITTLE_ENDIAN
