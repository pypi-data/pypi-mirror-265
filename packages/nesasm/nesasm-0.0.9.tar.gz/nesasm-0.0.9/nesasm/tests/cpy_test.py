"""
CPY, Compare with Y Test
"""

import unittest
from nesasm.tests import MetaInstructionCase


class CpyImmTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CPY #$10'
    lex = [('T_INSTRUCTION', 'CPY'), ('T_HEX_NUMBER', '#$10')]
    syn = ['S_IMMEDIATE']
    code = [0xC0, 0x10]


class CpyImmDecimalTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CPY #10'
    lex = [('T_INSTRUCTION', 'CPY'), ('T_DECIMAL_NUMBER', '#10')]
    syn = ['S_IMMEDIATE']
    code = [0xC0, 0x0A]


class CpyImmBinaryTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CPY #%00000100'
    lex = [('T_INSTRUCTION', 'CPY'), ('T_BINARY_NUMBER', '#%00000100')]
    syn = ['S_IMMEDIATE']
    code = [0xC0, 0x04]


class CpyZpTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CPY $00'
    lex = [('T_INSTRUCTION', 'CPY'), ('T_ADDRESS', '$00')]
    syn = ['S_ZEROPAGE']
    code = [0xC4, 0x00]


class CpyAbsTest(unittest.TestCase, metaclass=MetaInstructionCase):

    asm = 'CPY $1234'
    lex = [('T_INSTRUCTION', 'CPY'), ('T_ADDRESS', '$1234')]
    syn = ['S_ABSOLUTE']
    code = [0xCC, 0x34, 0x12]
