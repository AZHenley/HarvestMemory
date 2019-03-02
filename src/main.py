from graphics import *
import parser
import player
import os

memory = [0] * (2**12)
drawObjects = []
columnCount = 8
columnHeight = len(memory) // columnCount
cellHeight = 1

def drawColumns(win):
    initial = 100
    width = 40
    offset = 0
    for j in range (0, columnCount):
        for i in range(0, columnHeight):
            r = Rectangle(Point(initial+j*8+offset, 50+i*cellHeight), Point(initial+width+j*8+offset, 52+i*cellHeight))
            r.setFill("black")
            r.setOutline("black")
            r.draw(win)
            drawObjects.append(r)
        offset = offset + 90

def createPlayers():
    players = []
    path = os.path.join(os.getcwd(), 'scripts')
    if not os.path.isdir(path):
        print("Error: Scripts folder not found.")
        return None
    for fileName in os.listdir(path):
        try:
            with open(fileName, 'r') as f:
                code = f.read()
                p = parser.Parser(fileName, code)
                p.parse()
                players.append(player.Player(p.instructions, p.labels))
        except Exception as e:
            print(e)
    return players


def main():
    players = createPlayers()
    #if players == None:
    #    return

    win = GraphWin("Harvest Memory", 1280, 800, autoflush=False)
    drawColumns(win)

    timer = 0
    while True:
        #drawObjects[timer].setFill("red")
        #drawObjects[timer].setOutline("red")
        timer = timer + 1
        update(10)
    #win.close()   

main()
