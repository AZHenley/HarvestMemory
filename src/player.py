class Player(object):
    def __init__(self, name=None, instructions=None, labels=None):
        self.name = self.displayName = name
        if len(self.name) > 6:
            self.displayName = name[0:6]
        self.instructions = instructions
        self.labels = labels
        self.delay = 0 # Number of turns before this player will execute again
        self.next = 0 # Next instruction to be executed.
        self.ran = 0 # Number of instructions executed by this player.
        self.registers = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0, 'rs': 3, 'rf': 0}