def toHex(number, length=4):
    t = 0xff
    for i in range(length - 1):
        t <<= 8
        t |= 0xff
    number = int(number) & t
    return ('0x%.' + str(length * 2) + 'x') % number
