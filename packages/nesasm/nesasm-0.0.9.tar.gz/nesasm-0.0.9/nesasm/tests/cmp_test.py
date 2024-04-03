"""
CMP, Compare with Accumulator Test
"""

import unittest
from nesasm.tests import MetaInstructionCase


class CpmImmTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP #$10'
    lex = [('T_INSTRUCTION', 'CMP'), ('T_HEX_NUMBER', '#$10')]
    syn = ['S_IMMEDIATE']
    code = [0xC9, 0x10]


class CpmImmDecimalTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP #10'
    lex = [('T_INSTRUCTION', 'CMP'), ('T_DECIMAL_NUMBER', '#10')]
    syn = ['S_IMMEDIATE']
    code = [0xC9, 0x0A]


class CpmImmBinaryTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP #%00000100'
    lex = [('T_INSTRUCTION', 'CMP'), ('T_BINARY_NUMBER', '#%00000100')]
    syn = ['S_IMMEDIATE']
    code = [0xC9, 0x04]


class CpmZpTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP $00'
    lex = [('T_INSTRUCTION', 'CMP'), ('T_ADDRESS', '$00')]
    syn = ['S_ZEROPAGE']
    code = [0xC5, 0x00]


class CpmZpxTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP $10,X'
    lex = [
        ('T_INSTRUCTION', 'CMP'),
        ('T_ADDRESS', '$10'),
        ('T_SEPARATOR', ','),
        ('T_REGISTER', 'X'),
    ]
    syn = ['S_ZEROPAGE_X']
    code = [0xD5, 0x10]


class CpmAbsTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP $1234'
    lex = [('T_INSTRUCTION', 'CMP'), ('T_ADDRESS', '$1234')]
    syn = ['S_ABSOLUTE']
    code = [0xCD, 0x34, 0x12]


class CpmAbsxTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP $1234, X'
    lex = [
        ('T_INSTRUCTION', 'CMP'),
        ('T_ADDRESS', '$1234'),
        ('T_SEPARATOR', ','),
        ('T_REGISTER', 'X'),
    ]
    syn = ['S_ABSOLUTE_X']
    code = [0xDD, 0x34, 0x12]


class CpmAbsyTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP $1234, Y'
    lex = [
        ('T_INSTRUCTION', 'CMP'),
        ('T_ADDRESS', '$1234'),
        ('T_SEPARATOR', ','),
        ('T_REGISTER', 'Y'),
    ]
    syn = ['S_ABSOLUTE_Y']
    code = [0xD9, 0x34, 0x12]


class CpmIndxTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP ($20, X)'
    lex = [
        ('T_INSTRUCTION', 'CMP'),
        ('T_OPEN', '('),
        ('T_ADDRESS', '$20'),
        ('T_SEPARATOR', ','),
        ('T_REGISTER', 'X'),
        ('T_CLOSE', ')'),
    ]
    syn = ['S_INDIRECT_X']
    code = [0xC1, 0x20]


class CpmIndyTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CMP ($20),Y'
    lex = [
        ('T_INSTRUCTION', 'CMP'),
        ('T_OPEN', '('),
        ('T_ADDRESS', '$20'),
        ('T_CLOSE', ')'),
        ('T_SEPARATOR', ','),
        ('T_REGISTER', 'Y'),
    ]
    syn = ['S_INDIRECT_Y']
    code = [0xD1, 0x20]
