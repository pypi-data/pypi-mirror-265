"""
LDX, Load Register X

This is one of the memory operations on the 6502
"""
import unittest
from nesasm.tests import MetaInstructionCase


class LdxImmTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'LDX #$10'
    lex = [('T_INSTRUCTION', 'LDX'), ('T_HEX_NUMBER', '#$10')]
    syn = ['S_IMMEDIATE']
    code = [0xA2, 0x10]


class LdxImmDecimalTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'LDX #10'
    lex = [('T_INSTRUCTION', 'LDX'), ('T_DECIMAL_NUMBER', '#10')]
    syn = ['S_IMMEDIATE']
    code = [0xA2, 0x0A]


class LdxImmBinaryTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'LDX #%00000100'
    lex = [('T_INSTRUCTION', 'LDX'), ('T_BINARY_NUMBER', '#%00000100')]
    syn = ['S_IMMEDIATE']
    code = [0xA2, 0x04]


class LdxZpTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'LDX $00'
    lex = [('T_INSTRUCTION', 'LDX'), ('T_ADDRESS', '$00')]
    syn = ['S_ZEROPAGE']
    code = [0xA6, 0x00]


class LdxZpyTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'LDX $10,Y'
    lex = [
        ('T_INSTRUCTION', 'LDX'),
        ('T_ADDRESS', '$10'),
        ('T_SEPARATOR', ','),
        ('T_REGISTER', 'Y'),
    ]
    syn = ['S_ZEROPAGE_Y']
    code = [0xB6, 0x10]


class LdxAbsTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'LDX $1234'
    lex = [('T_INSTRUCTION', 'LDX'), ('T_ADDRESS', '$1234')]
    syn = ['S_ABSOLUTE']
    code = [0xAE, 0x34, 0x12]


class LdxAbsyTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'LDX $1234,Y'
    lex = [
        ('T_INSTRUCTION', 'LDX'),
        ('T_ADDRESS', '$1234'),
        ('T_SEPARATOR', ','),
        ('T_REGISTER', 'Y'),
    ]
    syn = ['S_ABSOLUTE_Y']
    code = [0xBE, 0x34, 0x12]
