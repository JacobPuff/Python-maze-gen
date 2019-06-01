#!/usr/bin/env python

import random
import math
from PIL import Image

# divided by 2, floored, and then multiplied by 2 to make the plus 1 give a border
# without having to make unnecessary if statements.
# Much more elegant, for a possibly smaller number.
print("sizeX")
sizeX = math.floor(int(input())/2) * 2 + 1
print("sizeY")
sizeY = math.floor(int(input())/2) * 2 + 1
print("solve?(1:true,0:false)")
shouldSolve = int(input())
print("gif?(1:true,0:false)")
isGif = int(input())
gifStore = []
# this needs to be done so much better.
if sizeX < 5:
    sizeX = 5
if sizeY < 5:
    sizeY = 5

leStack = []
leSolvedStack = []
count = 0
solveCount = 0
posX = 1
posY = 1
scale = 3
WHITE = (255,255,255,255)
BLACK = (0,0,0,255)
RED = (255,0,0,255)
BLUE = (0,0,255,255)
colorStorage = [0,0,0,255]
colorFade = 0
mazeMade = False
solveMaze = False
myimage = Image.new('RGBA', (sizeX,sizeY), color=BLACK)
img = myimage.load()
img[1,1] = WHITE
while not mazeMade:
    availableDir = []

    if shouldSolve == 1 and posX == sizeX - 2 and posY == sizeY - 2:
        #computer starts at 0, so size is already + 1
        leSolvedStack = leStack.copy()
        solvePosX = posX
        solvePosY = posY
        colorFade = 255/(len(leSolvedStack) * 2)
        colorStorage = [0,0,255,255]
        img[posX, posY] = BLUE
        solveMaze = True

    while solveMaze:
        # Once I hit the end, copy the stack, then,
        # go through the whole stack and paint the solution
        # then make the rest of the maze from the regular stack afterwards.
        print("SOLVING: " + str(solveCount))
        solveCount += 1
        if solvePosX == 1 and solvePosY == 1:
            solveMaze = False
        else:
            solvePositions = leSolvedStack.pop()

        if solvePositions[0] < solvePosX:
            img[solvePosX - 1, solvePosY] = tuple([math.floor(x) for x in colorStorage])
            colorStorage[0] += colorFade
            colorStorage[2] -= colorFade
            img[solvePosX - 2, solvePosY] = tuple([math.floor(x) for x in colorStorage])
            colorStorage[0] += colorFade
            colorStorage[2] -= colorFade

        if solvePositions[0] > solvePosX:
            img[solvePosX + 1, solvePosY] = tuple([math.floor(x) for x in colorStorage])
            colorStorage[0] += colorFade
            colorStorage[2] -= colorFade
            img[solvePosX + 2, solvePosY] = tuple([math.floor(x) for x in colorStorage])
            colorStorage[0] += colorFade
            colorStorage[2] -= colorFade

        if solvePositions[1] < solvePosY:
            img[solvePosX, solvePosY - 1] = tuple([math.floor(x) for x in colorStorage])
            colorStorage[0] += colorFade
            colorStorage[2] -= colorFade
            img[solvePosX, solvePosY - 2] = tuple([math.floor(x) for x in colorStorage])
            colorStorage[0] += colorFade
            colorStorage[2] -= colorFade

        if solvePositions[1] > solvePosY:
            img[solvePosX, solvePosY + 1] = tuple([math.floor(x) for x in colorStorage])
            colorStorage[0] += colorFade
            colorStorage[2] -= colorFade
            img[solvePosX, solvePosY + 2] = tuple([math.floor(x) for x in colorStorage])
            colorStorage[0] += colorFade
            colorStorage[2] -= colorFade

        solvePosX = solvePositions[0]
        solvePosY = solvePositions[1]
        if isGif == 1:
            frame = myimage.copy()
            frame.resize((sizeX*scale,sizeY*scale), Image.NEAREST)
            gifStore.append(frame)

    # Dont want to have them right next to other sections. So move by 2
    if posX - 2 > 0 and img[posX - 2, posY] == BLACK:
        availableDir.append(0)
    if posX + 2 < sizeX and img[posX + 2, posY] == BLACK:
        availableDir.append(1)
    if posY - 2 > 0 and img[posX, posY - 2] == BLACK:
        availableDir.append(2)
    if posY + 2 < sizeY and img[posX, posY + 2] == BLACK:
        availableDir.append(3)

    if len(availableDir) > 0:
        print(count)
        count += 1
        leStack.append((posX,posY))
        randomDir = math.floor(random.random() * (len(availableDir) - 0.01))
        chosenDir = availableDir[randomDir]

        if chosenDir == 0:
            img[posX-1, posY] = WHITE
            img[posX-2, posY] = WHITE
            posX -= 2

        if chosenDir == 1:
            img[posX+1, posY] = WHITE
            img[posX+2, posY] = WHITE
            posX += 2

        if chosenDir == 2:
            img[posX, posY-1] = WHITE
            img[posX, posY-2] = WHITE
            posY -= 2

        if chosenDir == 3:
            img[posX, posY+1] = WHITE
            img[posX, posY+2] = WHITE
            posY += 2

        if isGif == 1:
            frame = myimage.copy()
            frame.resize((sizeX*scale,sizeY*scale), Image.NEAREST)
            gifStore.append(frame)

    elif posX == 1 and posY == 1:
        mazeMade = True
    else:
        positions = leStack.pop(len(leStack)-1)
        posX = positions[0]
        posY = positions[1]

if isGif == 1:
    # these two lines just break things. Goddamnit.
    # for frame in gifStore:
    #     gifStore[frame].resize((sizeX*scale,sizeY*scale))
    gifStore[0].save('derperder.gif',
                     save_all=True,
                     append_images=gifStore[1:],
                     duration=30,
                     loop=0)
else:
    myimage = myimage.resize((sizeX*scale,sizeY*scale))
    myimage.save("ermahgerd.png", "PNG")

print("count: " + str(count))
print("solveCount: " + str(solveCount))
print("totalSteps: " + str(count+solveCount))
