from graphics import *

memory = [0] * (2**12)
drawObjects = []
columnCount = 8
columnHeight = len(memory) // columnCount
cellHeight = 1

def drawColumns(win):
    for j in range (0, columnCount):
        for i in range(0, columnHeight):
            r = Rectangle(Point(100+j*8, 50+i*cellHeight), Point(200+j*8, 52+i*cellHeight))
            r.setFill("black")
            r.setOutline("black")
            r.draw(win)
            drawObjects.append(r)

def main():
    win = GraphWin("Harvest Memory", 1280, 800, autoflush=False)
    drawColumns(win)
    timer = 0
    while True:
        drawObjects[timer].setFill("red")
        drawObjects[timer].setOutline("red")
        timer = timer + 1
        update(10)
    #win.close()   

# for each file in directory
    # create Player object
    # catch errors, report to console and skip that player


main()