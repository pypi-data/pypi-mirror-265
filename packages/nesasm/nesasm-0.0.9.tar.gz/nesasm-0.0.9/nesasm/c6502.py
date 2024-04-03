address_mode_def = {}
address_mode_def['S_IMPLIED'] = dict(size=1, short='sngl')
address_mode_def['S_IMMEDIATE'] = dict(size=2, short='imm')
address_mode_def['S_IMMEDIATE_WITH_MODIFIER'] = dict(size=2, short='imm')
address_mode_def['S_ACCUMULATOR'] = dict(size=1, short='acc')
address_mode_def['S_IMMEDIATE'] = dict(size=2, short='imm')
address_mode_def['S_ZEROPAGE'] = dict(size=2, short='zp')
address_mode_def['S_ZEROPAGE_X'] = dict(size=2, short='zpx')
address_mode_def['S_ZEROPAGE_Y'] = dict(size=2, short='zpy')
address_mode_def['S_ABSOLUTE'] = dict(size=3, short='abs')
address_mode_def['S_ABSOLUTE_X'] = dict(size=3, short='absx')
address_mode_def['S_ABSOLUTE_Y'] = dict(size=3, short='absy')
address_mode_def['S_INDIRECT_X'] = dict(size=2, short='indx')
address_mode_def['S_INDIRECT_Y'] = dict(size=2, short='indy')
address_mode_def['S_RELATIVE'] = dict(size=2, short='rel')

opcodes = {}
opcodes['ADC'] = dict(
    imm=0x69,
    zp=0x65,
    zpx=0x75,
    abs=0x6D,
    absx=0x7D,
    absy=0x79,
    indx=0x61,
    indy=0x71,
)
opcodes['AND'] = dict(
    imm=0x29,
    zp=0x25,
    zpx=0x35,
    abs=0x2D,
    absx=0x3D,
    absy=0x39,
    indx=0x21,
    indy=0x31,
)
opcodes['ASL'] = dict(
    acc=0x0A, imm=0x0A, zp=0x06, zpx=0x16, abs=0x0E, absx=0x1E
)
opcodes['BCC'] = dict(rel=0x90)
opcodes['BCS'] = dict(rel=0xB0)
opcodes['BEQ'] = dict(rel=0xF0)
opcodes['BIT'] = dict(zp=0x24, abs=0x2C)
opcodes['BMI'] = dict(rel=0x30)
opcodes['BNE'] = dict(rel=0xD0)
opcodes['BPL'] = dict(rel=0x10)
opcodes['BVC'] = dict(rel=0x50)
opcodes['BVS'] = dict(rel=0x70)
opcodes['CLC'] = dict(sngl=0x18)
opcodes['CLD'] = dict(sngl=0xD8)
opcodes['CLI'] = dict(sngl=0x58)
opcodes['CLV'] = dict(sngl=0xB8)
opcodes['CMP'] = dict(
    imm=0xC9,
    zp=0xC5,
    zpx=0xD5,
    abs=0xCD,
    absx=0xDD,
    absy=0xD9,
    indx=0xC1,
    indy=0xD1,
)
opcodes['CPX'] = dict(imm=0xE0, zp=0xE4, abs=0xEC)
opcodes['CPY'] = dict(imm=0xC0, zp=0xC4, abs=0xCC)
opcodes['DEC'] = dict(zp=0xC6, zpx=0xD6, abs=0xCE, absx=0xDE)
opcodes['DEX'] = dict(sngl=0xCA)
opcodes['DEY'] = dict(sngl=0x88)
opcodes['EOR'] = dict(
    imm=0x49,
    zp=0x45,
    zpx=0x55,
    abs=0x4D,
    absx=0x5D,
    absy=0x59,
    indx=0x41,
    indy=0x51,
)
opcodes['INC'] = dict(zp=0xE6, zpx=0xF6, abs=0xEE, absx=0xFE)
opcodes['INX'] = dict(sngl=0xE8)
opcodes['INY'] = dict(sngl=0xC8)
opcodes['JMP'] = dict(abs=0x4C)
opcodes['JSR'] = dict(abs=0x20)
opcodes['LDA'] = dict(
    imm=0xA9,
    zp=0xA5,
    zpx=0xB5,
    abs=0xAD,
    absx=0xBD,
    absy=0xB9,
    indx=0xA1,
    indy=0xB1,
)
opcodes['LDX'] = dict(imm=0xA2, zp=0xA6, zpy=0xB6, abs=0xAE, absy=0xBE)
opcodes['LDY'] = dict(imm=0xA0, zp=0xA4, zpx=0xB4, abs=0xAC, absx=0xBC)
opcodes['LSR'] = dict(
    acc=0x4A, imm=0x4A, zp=0x46, zpx=0x56, abs=0x4E, absx=0x5E
)
opcodes['NOP'] = dict(sngl=0xEA)
opcodes['ORA'] = dict(
    imm=0x09,
    zp=0x05,
    zpx=0x15,
    abs=0x0D,
    absx=0x1D,
    absy=0x19,
    indx=0x01,
    indy=0x11,
)
opcodes['PHA'] = dict(sngl=0x48)
opcodes['PHP'] = dict(sngl=0x08)
opcodes['PLA'] = dict(sngl=0x68)
opcodes['PLP'] = dict(sngl=0x28)
opcodes['SBC'] = dict(
    imm=0xE9,
    zp=0xE5,
    zpx=0xF5,
    abs=0xED,
    absx=0xFD,
    absy=0xF9,
    indx=0xE1,
    indy=0xF1,
)
opcodes['SEC'] = dict(sngl=0x38)
opcodes['SED'] = dict(sngl=0xF8)
opcodes['SEI'] = dict(sngl=0x78)
opcodes['STA'] = dict(
    zp=0x85, zpx=0x95, abs=0x8D, absx=0x9D, absy=0x99, indx=0x81, indy=0x91
)
opcodes['STX'] = dict(zp=0x86, zpy=0x96, abs=0x8E)
opcodes['STY'] = dict(zp=0x84, zpx=0x94, abs=0x8C)
opcodes['ROL'] = dict(imm=0x2A, zp=0x26, zpx=0x36, abs=0x2E, absx=0x3E)
opcodes['ROR'] = dict(imm=0x6A, zp=0x66, zpx=0x76, abs=0x6E, absx=0x7E)
opcodes['RTI'] = dict(sngl=0x40)
opcodes['RTS'] = dict(sngl=0x60)
opcodes['TAX'] = dict(sngl=0xAA)
opcodes['TAY'] = dict(sngl=0xA8)
opcodes['TSX'] = dict(sngl=0xBA)
opcodes['TXA'] = dict(sngl=0x8A)
opcodes['TXS'] = dict(sngl=0x9A)
opcodes['TYA'] = dict(sngl=0x98)
