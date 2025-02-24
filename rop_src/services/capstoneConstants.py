from capstone import CS_ARCH_ARM, CS_ARCH_ARM64, CS_ARCH_MIPS, CS_ARCH_X86, CS_ARCH_PPC, CS_ARCH_SPARC, \
    CS_ARCH_SYSZ, CS_ARCH_XCORE, CS_ARCH_M68K, CS_ARCH_TMS320C64X, CS_ARCH_M680X, CS_ARCH_EVM, CS_ARCH_MAX, \
    CS_MODE_LITTLE_ENDIAN, CS_MODE_ARM, CS_MODE_16, CS_MODE_32, CS_MODE_64, CS_MODE_THUMB, CS_MODE_MCLASS, CS_MODE_V8, \
    CS_MODE_MICRO, CS_MODE_MIPS3, CS_MODE_MIPS32R6, CS_MODE_MIPS2, CS_MODE_V9, CS_MODE_QPX, CS_MODE_M68K_000, \
    CS_MODE_M68K_010, CS_MODE_M68K_020, CS_MODE_M68K_030, CS_MODE_M68K_040, CS_MODE_M68K_060, CS_MODE_BIG_ENDIAN, \
    CS_MODE_MIPS32, CS_MODE_MIPS64, CS_MODE_M680X_6301, CS_MODE_M680X_6309, CS_MODE_M680X_6800, CS_MODE_M680X_6801, \
    CS_MODE_M680X_6805, CS_MODE_M680X_6808, CS_MODE_M680X_6809, CS_MODE_M680X_6811, CS_MODE_M680X_CPU12, \
    CS_MODE_M680X_HCS08

CapstonePossibleArchitectures = [
    CS_ARCH_ARM,
    CS_ARCH_ARM64,
    CS_ARCH_MIPS,
    CS_ARCH_X86,
    CS_ARCH_PPC,
    CS_ARCH_SPARC,
    CS_ARCH_SYSZ,
    CS_ARCH_XCORE,
    CS_ARCH_M68K,
    CS_ARCH_TMS320C64X,
    CS_ARCH_M680X,
    CS_ARCH_EVM,
    CS_ARCH_MAX
]

CapstonePossibleModes = [
    CS_MODE_ARM,
    CS_MODE_16,
    CS_MODE_32,
    CS_MODE_64,
    CS_MODE_THUMB,
    CS_MODE_MCLASS,
    CS_MODE_V8,
    CS_MODE_MICRO,
    CS_MODE_MIPS3,
    CS_MODE_MIPS32R6,
    CS_MODE_MIPS2,
    CS_MODE_V9,
    CS_MODE_QPX,
    CS_MODE_M68K_000,
    CS_MODE_M68K_010,
    CS_MODE_M68K_020,
    CS_MODE_M68K_030,
    CS_MODE_M68K_040,
    CS_MODE_M68K_060,
    CS_MODE_MIPS32,
    CS_MODE_MIPS64,
    CS_MODE_M680X_6301,
    CS_MODE_M680X_6309,
    CS_MODE_M680X_6800,
    CS_MODE_M680X_6801,
    CS_MODE_M680X_6805,
    CS_MODE_M680X_6808,
    CS_MODE_M680X_6809,
    CS_MODE_M680X_6811,
    CS_MODE_M680X_CPU12,
    CS_MODE_M680X_HCS08
]

CapstonePossibleEndianness = [CS_MODE_BIG_ENDIAN, CS_MODE_LITTLE_ENDIAN]
