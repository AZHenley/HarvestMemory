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