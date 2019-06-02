#!/usr/bin/env python

import random
import math
import argparse
from PIL import Image

WHITE = (255,255,255,255)
BLACK = (0,0,0,255)
RED = (255,0,0,255)
GREEN = (0,255,0,255)
BLUE = (0,0,255,255)


def save(image, gifStore, inputsReceived, scale):
    if inputsReceived['isGif']:
        # these two lines just break things. Goddamnit.
        # for frame in gifStore:
        #     gifStore[frame].resize((inputsReceived['sizeX']*scale,inputsReceived['sizeY']*scale))
        gifStore[0].save('derperder.gif',
                         save_all=True,
                         append_images=gifStore[1:],
                         duration=30,
                         loop=0)
    else:
        image = image.resize((inputsReceived['sizeX']*scale,inputsReceived['sizeY']*scale))
        image.save("ermahgerd.png", "PNG")


def saveGifFrame(inputsReceived, scale, gifStore):
    if inputsReceived['isGif']:
        frame = myimage.copy()
        frame.resize(
            (inputsReceived['sizeX'] * scale, inputsReceived['sizeY'] * scale),
            Image.NEAREST)
        gifStore.append(frame)


def setNextColor(stackLength, color, inputsReceived):
    colorFade = 0
    if inputsReceived['solveColor'] == 1:
        colorFade = 255/(stackLength * 2)
    elif inputsReceived['solveColor'] == 2:
        colorFade = 255*2/(stackLength * 2)
    elif inputsReceived['solveColor'] == 0:
        colorFade = (255*5)/(stackLength * 2)

    if inputsReceived['solveColor'] == 1:
        color[0] += colorFade
        color[2] -= colorFade

    if inputsReceived['solveColor'] == 2 and math.floor(color[0]) <= 0 and math.floor(color[1]) <= 255 and math.floor(color[2]) >= 0:
        color[1] += colorFade
        color[2] -= colorFade
    elif inputsReceived['solveColor'] == 2 and math.floor(color[2]) <= 0 and math.floor(color[0]) <= 255 and math.floor(color[1]) >= 0:
        color[0] += colorFade
        color[1] -= colorFade
    elif inputsReceived['solveColor'] == 2 and math.floor(color[1]) <= 0 and math.floor(color[2]) <= 255 and math.floor(color[0]) >= 0:
        color[2] += colorFade
        color[0] -= colorFade

    if inputsReceived['solveColor'] == 0:
        return
    # print("colorStorage: " + str(colorStorage))
    # print("colorCount: " + str(colorCount))
    return color


def generateMazeSolution(stats, img, solvePosX, solvePosY, stack, scale, gifStore):
    solvingMaze = True
    colorStorage = [0,0,255,255]
    img[solvePosX, solvePosY] = BLUE
    leSolvedStack = stack.copy()
    # it already starts with one filled in, and ends with one that it doesn't move to,
    # but we still need that to calculate colorFade.
    stats['leSavedStack'] = len(leSolvedStack)+2
    while solvingMaze:
        # Once I hit the end, copy the stack, then,
        # go through the whole stack and paint the solution
        # then make the rest of the maze from the regular stack afterwards.
        # print("SOLVING: " + str(stats['solveCount']))
        if solvePosX == 1 and solvePosY == 1:
            print("ending maze solving")
            solvingMaze = False
        else:
            solvePositions = leSolvedStack.pop()

        if solvePositions[0] < solvePosX:
            colorStorage = setNextColor(stats['leSavedStack'], colorStorage, inputsReceived)
            img[solvePosX - 1, solvePosY] = tuple([math.floor(x) for x in colorStorage])
            colorStorage = setNextColor(stats['leSavedStack'], colorStorage, inputsReceived)
            img[solvePosX - 2, solvePosY] = tuple([math.floor(x) for x in colorStorage])

        if solvePositions[0] > solvePosX:
            colorStorage = setNextColor(stats['leSavedStack'], colorStorage, inputsReceived)
            img[solvePosX + 1, solvePosY] = tuple([math.floor(x) for x in colorStorage])
            colorStorage = setNextColor(stats['leSavedStack'], colorStorage, inputsReceived)
            img[solvePosX + 2, solvePosY] = tuple([math.floor(x) for x in colorStorage])

        if solvePositions[1] < solvePosY:
            colorStorage = setNextColor(stats['leSavedStack'], colorStorage, inputsReceived)
            img[solvePosX, solvePosY - 1] = tuple([math.floor(x) for x in colorStorage])
            colorStorage = setNextColor(stats['leSavedStack'], colorStorage, inputsReceived)
            img[solvePosX, solvePosY - 2] = tuple([math.floor(x) for x in colorStorage])

        if solvePositions[1] > solvePosY:
            colorStorage = setNextColor(stats['leSavedStack'], colorStorage, inputsReceived)
            img[solvePosX, solvePosY + 1] = tuple([math.floor(x) for x in colorStorage])
            colorStorage = setNextColor(stats['leSavedStack'], colorStorage, inputsReceived)
            img[solvePosX, solvePosY + 2] = tuple([math.floor(x) for x in colorStorage])

        stats['colorCount'] += 2
        solvePosX = solvePositions[0]
        solvePosY = solvePositions[1]
        saveGifFrame(inputsReceived, scale, gifStore)
        stats['solveCount'] += 1
    return img


def generateMaze(image, inputsReceived):
    gifStore = []
    leStack = []
    img = image.load()
    scale = 3
    stats = {'count': 0, 'solveCount': 0, 'colorCount': 0, 'leSavedStack': 0}
    mazeMade = False
    posX = 1
    posY = 1
    img[posX,posY] = WHITE
    while not mazeMade:
        availableDir = []

        if stats['solveCount'] == 0 and inputsReceived['shouldSolve'] and posX == inputsReceived['sizeX'] - 2 and posY == inputsReceived['sizeY'] - 2:
            # computer starts at 0, so size is already + 1
            print("Solving maze starts now " + str(posX) + "," + str(posY) + "," + str(inputsReceived['sizeX'] - 2) + "," + str(inputsReceived['sizeY'] - 2))
            img = generateMazeSolution(stats, img, posX, posY, leStack, scale, gifStore)

        # Dont want to have them right next to other sections. So move by 2
        if posX - 2 > 0 and img[posX - 2, posY] == BLACK:
            availableDir.append(0)
        if posX + 2 < inputsReceived['sizeX'] and img[posX + 2, posY] == BLACK:
            availableDir.append(1)
        if posY - 2 > 0 and img[posX, posY - 2] == BLACK:
            availableDir.append(2)
        if posY + 2 < inputsReceived['sizeY'] and img[posX, posY + 2] == BLACK:
            availableDir.append(3)

        if len(availableDir) > 0:
            # print(count)
            stats['count'] += 1
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

            saveGifFrame(inputsReceived, scale, gifStore)

        elif posX == 1 and posY == 1:
            mazeMade = True
        else:
            positions = leStack.pop(len(leStack)-1)
            posX = positions[0]
            posY = positions[1]
    printStats(stats)
    save(image, gifStore, inputsReceived, scale)


def printStats(stats):
    print("colorCount: " + str(stats['colorCount']))
    print("leSavedStack: " + str(stats['leSavedStack']))
    print("count: " + str(stats['count']))
    print("solveCount: " + str(stats['solveCount']))
    print("totalSteps: " + str(stats['count']+stats['solveCount']))


def getInputs():
    parser = argparse.ArgumentParser()
    parser.add_argument("sizeX", help="int, set size on the 'x' axis", type=int)
    parser.add_argument("sizeY", help="int, set size on the 'y' axis", type=int)
    parser.add_argument("--shouldSolve", help="sets whether or not to solve the maze, needs solveColor",
                        default=False, action='store_true')
    parser.add_argument("--solveColor", help="0:rainbow,1:red&blue,2:RGB, sets which colors are used for the solution",
                        default=None, type=int)
    parser.add_argument("--isGif", help="sets if maze should be saved as gif", default=False, action='store_true')
    args = parser.parse_args()
    if args.shouldSolve and not args.solveColor:
        parser.error('need --solveColor when using --shouldSolve')
    if args.solveColor and not args.shouldSolve:
        parser.error('cant use --solveColor when shouldSolve == False')
    if args.solveColor < 0 or args.solveColor > 2:
        parser.error('--solveColor needs to be between 0 and 2')
    inputsReceived= {'sizeX': args.sizeX, 'sizeY': args.sizeY, 'shouldSolve': args.shouldSolve,
                     'solveColor': args.solveColor, 'isGif': args.isGif}
    # divided by 2, floored, and then multiplied by 2 to make the plus 1 give a border
    # without having to make unnecessary if statements.
    # Much more elegant, for a possibly smaller number.
    inputsReceived['sizeX'] = (math.floor(inputsReceived['sizeX']/2) * 2) + 1
    inputsReceived['sizeY'] = (math.floor(inputsReceived['sizeY']/2) * 2) + 1

    if inputsReceived['sizeX'] < 5:
        inputsReceived['sizeX'] = 5
    if inputsReceived['sizeY'] < 5:
        inputsReceived['sizeY'] = 5
    return inputsReceived


if __name__ == "__main__":
    inputsReceived = getInputs()
    myimage = Image.new('RGBA', (inputsReceived['sizeX'],inputsReceived['sizeY']), color=BLACK)
    generateMaze(myimage, inputsReceived)
