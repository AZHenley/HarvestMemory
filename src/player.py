class Player(object):
    fruit = 0
    delay = 0
    name = "knoxville"
    instructions = []
    labels = {}
    next = 0 # Next instruction to be executed.
    registers = {'r0': 0, 'r1': 0, 'r2': 0, 'r3': 0}

    def __init__(self, name=None, instructions=None, labels=None):
        self.name = name
        self.instructions = instructions
        self.labels = labels