from abc import abstractmethod, ABCMeta
from py65.devices.mpu6502 import MPU


REGISTERS = {
    'A': 'a',
    'X': 'x',
    'Y': 'y',
    'P': 'p',
    'SP': 'sp',
    'PC': 'pc',
}

FLAGS = {
    'C': MPU.CARRY,
    'Z': MPU.ZERO,
    'I': MPU.INTERRUPT,
    'D': MPU.DECIMAL,
    'B': MPU.BREAK,
    'V': MPU.OVERFLOW,
    'N': MPU.NEGATIVE,
}


class CPUBridge(metaclass=ABCMeta):
    @abstractmethod
    def cpu_pc(self, counter):
        pass

    @abstractmethod
    def memory_set(self, pos, val):
        pass

    @abstractmethod
    def memory_fetch(self, pos):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def cpu_set_register(self, register, value):
        pass

    @abstractmethod
    def cpu_register(self, register):
        pass

    @abstractmethod
    def cpu_flag(self, flag):
        pass

    @abstractmethod
    def cpu_set_flag(self, flag):
        pass

    @abstractmethod
    def cpu_unset_flag(self, flag):
        pass

    @abstractmethod
    def cpu_push_byte(self, byte):
        pass

    @abstractmethod
    def cpu_pull_byte(self):
        pass

    @abstractmethod
    def cpu_push_word(self, word):
        pass

    @abstractmethod
    def cpu_pull_word(self):
        pass


class Py65CPUBridge(CPUBridge):
    def __init__(self):
        self.cpu = MPU()

    def cpu_pc(self, counter):
        self.cpu.pc = counter

    def memory_set(self, pos, val):
        self.cpu.memory[pos] = val

    def memory_fetch(self, pos):
        return self.cpu.memory[pos]

    def execute(self):
        self.cpu.step()
        return self.cpu.processorCycles, None

    def cpu_set_register(self, register, value):
        name = REGISTERS[register]
        setattr(self.cpu, name, value)

    def cpu_register(self, register):
        name = REGISTERS[register]
        return getattr(self.cpu, name)

    def cpu_flag(self, flag):
        bit = FLAGS[flag]
        return not not (self.cpu.p & bit)

    def cpu_set_flag(self, flag):
        bit = FLAGS[flag]
        self.cpu.p |= bit

    def cpu_unset_flag(self, flag):
        mask = ~FLAGS[flag]
        self.cpu.p &= mask

    def cpu_push_byte(self, byte):
        self.cpu.stPush(byte)

    def cpu_pull_byte(self):
        return self.cpu.stPop()

    def cpu_push_word(self, word):
        self.cpu.stPushWord(word)

    def cpu_pull_word(self):
        return self.cpu.stPopWord()
