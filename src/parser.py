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
    'random': 3
                }

class Instruction(object):
    def __init__(self, token=None, operands=None):
        self.token = token
        self.operands = operands

class Operand(object):
    def __init__(self, token=None, opType=None):
        self.token = token
        self.type = opType # LABEL or INT or REG

lineNumber = -1
fileName = ""

def parse(name, input):
    global lineNumber, fileName
    fileName = name

    labels = {} # Labels for this program.
    instructions = [] # Instructions for this program.

    input = input.lower()
    lines = input.split('\n')

    for index, line in enumerate(lines):
        lineNumber = index

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
            if label not in labels:
                labels[label] = index
            # If label already exists, return an error.
            #else:
                #pass

        # Check if this is an instruction.
        elif tokens[0] in opcodes:
            instructions.append(parseInstruction(tokens))
        # If none of the above, return an error.
        else:
            Error("Invalid instruction: {}".format(tokens[0]))
    return (labels, instructions)


def parseInstruction(tokens):
    instToken = tokens[0]
    expectedOperandCount = opcodes[instToken]
    operands = []

    for i in range(1, len(tokens)):
        if tokens[i] == '':
            continue
        # Must either be label, integer, or register.
        if isRegister(tokens[i]):
            operands.append(Operand(tokens[i], "REG"))
        elif isInteger(tokens[i]):
            operands.append(Operand(tokens[i], "INT"))
        else:
            # Assume this must be a label (could be an error).
            # Only goto allows label as operand.
            if tokens[0] == 'goto':
                operands.append(Operand(tokens[i], "LABEL"))
            else:
                Error('Invalid operand: {}'.format(tokens[i]))
    
    # Check if correct number of operands are present.
    if expectedOperandCount != len(operands):
        Error('Expected {} operands, but got {}.'.format(expectedOperandCount, len(operands)))
    
    return Instruction(tokens[0], operands)

def Error(str):
    raise Exception('<{}, line {}> {}'.format(fileName, lineNumber, str))

def isRegister(str):
    if len(str) == 2 and str[0] == 'r':
        if str[1] == '0' or str[1] == '1' or str[1] == '2' or str[1] == '3':
            return True
    return False


def isInteger(str):
    if len(str) >= 2 and (str[0] == '+' or str[0] == '-'):
        return str[1:].isdigit()
    return str.isdigit()


a = parse('azh.txt', 'add 5, 3, 2\nadd 2, r0, r3 ')
print(a[0])
print(len(a[1]))