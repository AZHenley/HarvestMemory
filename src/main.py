from graphics import *
import parser
import player
import os
import random

memorySize = 2**12
memory = [0] * memorySize
drawObjects = []
textObjects = []
columnCount = 8
columnHeight = len(memory) // columnCount
cellHeight = 1
initialSeeds = 20
decay = 0.7
remainingFruit = 0


def initMemory():
    global remainingFruit
    # Randomly pick some starting points
    seeds = []
    for i in range(initialSeeds):
        seeds.append(random.randrange(0, memorySize, 1))
    
    # Add fruit at the random points in memory.
    # Use a decay function, 0.75^x, to add more fruit nearby.
    for seed in seeds:
        remainingFruit = remainingFruit + 1
        memory[seed] = -100
        chance = decay
        i = 1
        while chance > 0.01:
            # Move away from the seed in both directions.
            rLeft = random.random()
            rRight = random.random()
            if rLeft <= chance:
                if seed-i > 0:
                    remainingFruit = remainingFruit + 1
                    memory[seed-i] = -100
            if rRight <= chance:
                if seed+i < len(memory)-1:
                    remainingFruit = remainingFruit + 1
                    memory[seed+i] = -100
            i = i + 1
            chance = decay**i
    return memory

def drawColumns(win):
    xstart = 480
    ystart = 100
    width = 40
    height = 2
    offset = 0
    for j in range (0, columnCount):
        for i in range(0, columnHeight):
            r = Rectangle(Point(xstart+j*8+offset, ystart+i*cellHeight), Point(xstart+width+j*8+offset, ystart+height+i*cellHeight))
            r.setFill("black")
            r.setOutline("black")
            r.draw(win)
            drawObjects.append(r)
        offset = offset + 90


def drawPlayers(win, players):
    xstart = 100
    ystart = 100
    xoffset = 0
    yoffset = 0
    for p in range(1, len(players)+1):
        t = Text(Point(xstart+xoffset, ystart+yoffset), players[p-1].displayName)
        t.setSize(22)
        t.draw(win)
        textObjects.append(t)

        yoffset = yoffset + 45
        if p % 15 == 0:
            xoffset = xoffset + 210
            yoffset = 0


def updateColumns():
    for i in range(0, len(memory), 1):
        if memory[i] == -100:
            drawObjects[i].setFill("red")
            drawObjects[i].setOutline("red")

def createPlayers():
    players = []
    path = os.path.join(os.getcwd(), 'scripts')
    if not os.path.isdir(path):
        print("Error: Scripts folder not found at {}".format(path))
        return None
    for fileName in os.listdir(path):
        try:
            with open(os.path.join(path, fileName), 'r') as f:
                code = f.read()
                p = parser.Parser(fileName, code)
                p.parse()
                players.append(player.Player(fileName.split('.')[0], p.instructions, p.labels))
        except Exception as e:
            print(e)
            
    random.shuffle(players)
    return players


def main():
    initMemory()
    players = createPlayers()
    if players == None:
        return

    win = GraphWin("Harvest Memory", 1280, 800, autoflush=False)
    drawPlayers(win, players)
    drawColumns(win)
    updateColumns()

    print(remainingFruit)

    timer = 0
    while True:
        drawObjects[timer].setFill("red")
        drawObjects[timer].setOutline("red")
        timer = timer + 1
        update(10)
    #win.close()   


main()
