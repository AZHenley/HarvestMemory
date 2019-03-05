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
harvestError = 15 # number of ticks if harvest fails

valLimit = 2**16 # Registers and memory values are signed 32-bit numbers

class CPU(object):
    def __init__(self, memory=None, fruit=None, players=None):
        self.memory = memory
        self.players = players
        self.fruit = fruit
        self.ticks = 0
        self.next = 0
        self.registers = {'rw': 0, 'rt': 0}

    def execute(self):
        nextPlayer = self.players[self.next]
        if nextPlayer.delay == 0:
            #try:
            self.run(nextPlayer)
            #except Exception as e:
                #print("Exception thrown by " + nextPlayer.displayName)
        else:
            nextPlayer.delay = nextPlayer.delay - 1

        self.next = self.next + 1
        if self.next == len(self.players):
            self.next = 0

        # Update fruits
        for f in self.fruit:
            self.memory[f] = self.memory[f] - 1
            if self.memory[f] < -100:
                self.memory[f] = -100
        
        # Update global registers
        self.registers['rt'] = self.ticks
        self.registers['rw'] = max(p.registers['rs'] for p in self.players)


    def getMemoryValue(self, player, addr):
        if addr < 0 or addr >= len(self.memory): # Bounds check.
            player.registers["rf"] = 5
            return 0
        return self.memory[addr]


    def plantMemory(self, player, addr):
        if addr < 0 or addr >= len(self.memory): # Bounds check.
            player.registers["rf"] = 5
            return

        if self.getMemoryValue(player, addr) < 0:
            self.fruit.remove(addr)

        self.memory[addr] = -1
        self.fruit.add(addr)


    def setMemoryValue(self, player, addr, val):
        if addr < 0 or addr >= len(self.memory): # Bounds check.
            player.registers["rf"] = 5
            return

        # Update fruit.
        if self.getMemoryValue(player, addr) < 0:
            self.fruit.remove(addr)

        # Set value and wrap if needed.
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
        if op.type == "INT":
            addr = int(op.token)
        elif op.type == "REGISTER":
            addr = self.getRegister(player, op.token)
        return addr


    def getValue(self, player, op):
        val = -1
        if op.type == "INT":
            val = int(op.token)
        elif op.type == "REGISTER":
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
        if player.next >= len(player.instructions):
            return

        inst = player.instructions[player.next]
        op = inst.token
        operands = inst.operands
        dTicks = opcodes[op] # Keep track of ticks this run. Start with the instruction's tick cost.
        player.registers['rf'] = 0 # Reset error flag

        # For debugging:
        #print(player.displayName + "  " + op + "  " + str(player.next) + " of " + str(len(player.instructions)))

        if op == "harvest":
            addr = self.getAddress(player, operands[0])
            if self.getMemoryValue(player, addr) == -100:
                self.setMemoryValue(player, addr, 0)
                player.registers['rs'] = player.registers['rs'] + 5
                self.fruit.remove(addr)
            else:
                dTicks = dTicks + harvestError
                player.registers['rf'] = 9

        elif op == "plant":
            if player.registers['rs'] > 0:
                addr = self.getAddress(player, operands[0])
                #self.setMemoryValue(player, addr, -1)
                self.plantMemory(player, addr)
                player.registers['rs'] = player.registers['rs'] - 1
            else:
                player.registers['rf'] = 8

        elif op == "peek":
            addr = self.getAddress(player, operands[1])
            self.setRegister(player, operands[0].token, addr)

        elif op == "poke":
            val = self.getValue(player, operands[1])
            addr = self.getAddress(player, operands[0])
            self.setMemoryValue(player, addr, val)

        elif op == "goto":
            self.gotoLabel(player, operands[0].token)

        elif op == "ifequal":
            val1 = self.getValue(player, operands[0])
            val2 = self.getValue(player, operands[1])
            if val1 == val2:
                self.gotoLabel(player, operands[2])
                
        elif op == "ifless":
            val1 = self.getValue(player, operands[0])
            val2 = self.getValue(player, operands[1])
            if val1 < val2:
                self.gotoLabel(player, operands[2])

        elif op == "ifmore":
            val1 = self.getValue(player, operands[0])
            val2 = self.getValue(player, operands[1])
            if val1 > val2:
                self.gotoLabel(player, operands[2])

        elif op == "add":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setRegister(player, operands[0].token, val1+val2)

        elif op == "sub":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setRegister(player, operands[0].token, val1-val2)

        elif op == "mult":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setRegister(player, operands[0].token, val1*val2)

        elif op == "div":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setRegister(player, operands[0].token, val1//val2)

        elif op == "mod":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setRegister(player, operands[0].token, val1%val2)

        elif op == "random":
            val1 = self.getValue(player, operands[1])
            val2 = self.getValue(player, operands[2])
            self.setRegister(player, operands[0].token, random.randint(val1, val2+1)) 

        else: # Should never happen.
            pass

        # Add in time for using $ prefix
        for o in operands:
            if o.prefixed:
                dTicks = dTicks + indirectTicks 

        self.ticks = self.ticks + dTicks
        player.delay = dTicks # Set delay based on instruction ticks
        player.next = player.next + 1 # Next instruction to be executed