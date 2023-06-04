class ARMInstructionsROP:
    JOP_INSTR = [(b'[\x10-\x1e]\xff\x2f\xe1', 4),  # bx <reg>
                 (b'[\x30-\x3e]\xff\x2f\xe1', 4),  # blx <reg>
                 (b'[\x00-\x0f]\xf0\xa0\xe1', 4),  # mov pc, <reg>
                 (b'\x00\x80\xbd\xe8', 4)]  # ldm sp!, {pc}

    ROP_INSTR = [(b"[\x00-\xff][\x80-\xff]"
                  b"[\x10-\x1e\x30-\x3e\x50-\x5e\x70-\x7e\x90-\x9e\xb0-\xbe\xd0-\xde\xf0-\xfe]"
                  b"[\xe8\xe9]", 4),  # pop {[reg]*,pc}, ldm [reg], {*,pc}
                 (b"\x04\xf0\x9d\xe4", 4)]  # pop {pc}
