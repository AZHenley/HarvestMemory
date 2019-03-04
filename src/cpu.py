import parser
import player
import random

opcodes = { # Opcodes are keys, number of ticks are values.
    'harvest': 5,
    'plant': 4,
    'peek': 4,
    'poke': 3,
    'goto': 1,
    'ifequal': 2,
    'ifless': 2,
    'ifmore': 2,
    'add': 3,
    'sub': 3,
    'mult': 5,
    'div': 8,
    'mod': 7,
    'random': 6
                }
indirectTicks = 2 # number of ticks for each $
harvestError = 20 # number of ticks if harvest fails

valLimit = 2**16

class CPU(object):
    ticks = 0
    next = 0
    remainingFruit = 0
    fruit = [] # TODO: Get this from main. List of indices where seeds or fruit are.
    registers = {'rw': 0, 'rt': 0}

    def __init__(self, memory=None, players=None):
        self.memory = memory
        self.players = players

    def execute(self):
        self.run(self.players[next])

        self.next = self.next + 1
        if self.next == len(self.players):
            self.next = 0


    def execute(self):
        self.run(self.players[next])

        self.next = self.next + 1
        if self.next == len(self.players):
            self.next = 0


    def getMemoryValue(self, player, addr):
        if addr < 0 or addr >= len(self.memory): # Bounds check.
            player.registers["rf"] = 5
            return 0
        return self.memory[addr]


    def setMemoryValue(self, player, addr, val):
        if addr < 0 or addr >= len(self.memory): # Bounds check.
            player.registers["rf"] = 5
        if val > 0 and val < valLimit:
            self.memory[addr] = val
        elif val < 0:
            self.memory[addr] = val % (valLimit - 1)
            player.registers['rf'] = 3
        elif val > valLimit:
            self.memory[addr] = val % (valLimit - 1)
            player.registers['rf'] = 4


    def getRegister(self, player, reg):
        val = 0
        if reg in player.registers:
            val = player.registers[reg]
        elif reg in self.registers:
            val = self.registers[reg]
        return val


    # Only used for player setting a register.
    def setRegister(self, player, reg, val):
        if reg == 'r0' or reg == 'r1' or reg == 'r2' or reg == 'r3':
            if val > -valLimit and val < valLimit:
                player.registers[reg] = val
            elif val < -valLimit:
                player.registers[reg] = val % (valLimit - 1)
                player.registers['rf'] = 1
            elif val > valLimit:
                player.registers[reg] = val % (valLimit - 1)
                player.registers['rf'] = 2
        else:
            player.registers['rf'] = 10


    def getAddress(self, player, op):
        addr = -1
        if op.opType == "INT":
            addr = int(op.token)
        elif op.opType == "REGISTER":
            addr = self.getRegister(player, op.token)
        return addr


    def getValue(self, player, op):
        val = -1
        if op.opType == "INT":
            val = int(op.token)
        elif op.opType == "REGISTER":
            val = self.getRegister(player, op.token)

        # Handle $ in front of values.
        if op.prefixed:
            val = self.getMemoryValue(player, val)

        return val


    def gotoLabel(self, player, label):
        if label in player.labels:
            player.next = player.labels[label] - 1 # We will add 1 at the end.
        else:
            player.registers['rf'] = 7


    def run(self, player):
        # Check if player's program has ended.
        if player.next == len(player.instructions):
            return

        inst = player.instructions[next]
        op = inst.token
        operands = inst.operands
        dTicks = opcodes[op] # Keep track of ticks this run. Start with the instruction's tick cost.


        for o in operands:
            if o.prefixed:
                dTicks = dTicks + indirectTicks 
        player.next = player.next + 1
        pass