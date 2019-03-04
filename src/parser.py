# TODO: Move opcodes, Instruction, and Operand into CPU or its own module.

opcodes = { # Opcodes are keys, number of operands are values.
    'harvest': 1,
    'plant': 1,
    'peek': 2,
    'poke': 2,
    'goto': 1,
    'ifequal': 3,
    'ifless': 3,
    'ifmore': 3,
    'add': 3,
    'sub': 3,
    'mult': 3,
    'div': 3,
    'mod': 3,
    'random': 3
                }

class Instruction(object):
    def __init__(self, token=None, operands=None):
        self.token = token
        self.operands = operands

class Operand(object):
    def __init__(self, token=None, opType=None, prefixed=None):
        self.token = token
        self.type = opType # LABEL or INT or REG.
        self.prefixed = prefixed # Is this prefixed with $?

class Parser:
    lineNumber = None
    fileName = None
    labels = {} # Labels for this program.
    instructions = [] # Instructions for this program.
    input = None

    def __init__(self, name=None, code=None):
        self.input = code
        self.fileName = name

    def parse(self):
        self.input = self.input.lower()
        lines = self.input.split('\n')

        for index, line in enumerate(lines):
            self.lineNumber = index + 1

            # Throw away comments and leading whitespace.
            line = line.split(';')[0].lstrip() 
            # It is much faster to do replace->split than to do re.split.
            tokens = line.replace(',', ' ').replace('\t', ' ').replace('\r', ' ').split(' ')

            # Nothing to see here.
            if len(tokens) == 0 or tokens[0] == '':
                continue
            # Check if this is a label.
            elif ':' in tokens[0]:
                label = tokens[0].split(':')[0]
                if label not in self.labels:
                    self.labels[label] = index
                # If label already exists, return an error.
                #else:
                    #pass

            # Check if this is an instruction.
            elif tokens[0] in opcodes:
                self.instructions.append(self.parseInstruction(tokens))
            # If none of the above, return an error.
            else:
                self.Error("Invalid instruction: {}".format(tokens[0]))
        return


    def parseInstruction(self, tokens):
        inst = tokens[0]
        expectedOperandCount = opcodes[inst]
        operands = []

        for i in range(1, len(tokens)):
            t = tokens[i]
            if t == '':
                continue
            
            addr = False # Check if operand is prefixed for $, signifying address.
            if t[0] == '$':
                addr = True
                t = t[1:]

            # Must either be label, integer, or register.
            if self.isRegister(t):
                operands.append(Operand(t, "REG", addr))
            elif self.isInteger(t):
                operands.append(Operand(t, "INT", addr))
            else:
                # Assume this must be a label (could be an error).
                # Only goto, ifequal, ifmore, ifless allow label as operand.
                # Label can not be prefixed.
                if (inst == 'goto' or inst == 'ifequal' or inst == 'ifmore' or inst == 'ifless') and addr == False:
                    operands.append(Operand(t, "LABEL", False))
                else:
                    self.Error('Invalid operand: {}'.format(t))
        
        # Check if correct number of operands are present.
        if expectedOperandCount != len(operands):
            self.Error('Expected {} operands, but got {}.'.format(expectedOperandCount, len(operands)))
        
        return Instruction(tokens[0], operands)


    def Error(self, str):
        raise Exception('<{}, line {}> {}'.format(self.fileName, self.lineNumber, str))

    def isRegister(self, str):
        if len(str) == 2 and str[0] == 'r':
            if str[1] == '0' or str[1] == '1' or str[1] == '2' or str[1] == '3' or str[1] == 's' or str[1] == 'w' or str[1] == 't' or str[1] == 'f':
                return True
        return False


    def isInteger(self, str):
        if len(str) >= 2 and (str[0] == '+' or str[0] == '-'):
            return str[1:].isdigit()
        return str.isdigit()


p = Parser('azh.txt', 'add 5, 3, 2\nadd 2, r0, r3\nloop:\ngoto loop')
p.parse()
print(p.labels)
print(len(p.instructions))