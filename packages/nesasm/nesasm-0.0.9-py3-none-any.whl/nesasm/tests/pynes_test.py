from unittest import TestCase
from nesasm.compiler import lexical, syntax, semantic
from nesasm.cartridge import Cartridge
from nesasm.tests.bridge import Py65CPUBridge


class PyNESTest(TestCase):
    def setUp(self):
        self.cpu = Py65CPUBridge()

    def compile(self, asm, labels=None):
        code = '\n'.join(asm)
        tokens = lexical(code)
        ast = syntax(tokens)
        cart = Cartridge()
        return semantic(ast, False, cart=cart, labels=labels)

    def execute(self, opcodes):
        addr = 0
        start_addr = 0xC000
        self.cpu.cpu_pc(start_addr)
        for addr, val in enumerate(opcodes, start=start_addr):
            self.cpu.memory_set(addr, val)
        stop_addr = addr + 1

        while self.cpu.cpu.pc < stop_addr:
            self.cpu.execute()

    def test_assign(self):
        asm = ['var_q .rs 1', 'LDA #1', 'STA var_q', 'LDA #2', 'STA var_q']
        opcodes = self.compile(asm)
        self.execute(opcodes)

        var_q = self.cpu.memory_fetch(0)
        self.assertEqual(var_q, 2)

    def test_assign_three_values(self):
        asm = [
            'var_q .rs 1',
            'var_w .rs 1',
            'var_e .rs 1',
            'LDA #1',
            'STA var_q',
            'STA var_w',
            'STA var_e',
            'LDA #2',
            'STA var_q',
            'STA var_w',
            'STA var_e',
        ]
        opcodes = self.compile(asm)
        self.execute(opcodes)

        var_q = self.cpu.memory_fetch(0)
        var_w = self.cpu.memory_fetch(1)
        var_e = self.cpu.memory_fetch(2)

        self.assertEqual(var_q, 2)
        self.assertEqual(var_w, 2)
        self.assertEqual(var_e, 2)

    def test_assign_without_rs_directive(self):
        asm = [
            'LDA #1',
            'STA var_q',
            'LDA #2',
            'STA var_q',
        ]
        opcodes = self.compile(asm, labels=dict(var_q=0))
        self.execute(opcodes)

        var_q = self.cpu.memory_fetch(0)

        self.assertEqual(var_q, 2)
