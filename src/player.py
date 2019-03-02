class Player(object):
    fruit = 0
    delay = 0
    instructions = []
    labels = {}
    next = 0 # Next instruction to be executed.
    registers = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0}

    def __init__(self, instructions=None, labels=None):
        self.instructions = instructions
        self.labels = labels