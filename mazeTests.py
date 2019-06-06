import unittest
import ProbablyPython

class mazeUnitTests(unittest.TestCase):

    def test_setNextColor(self):
        inputs = {"sizeX": 50, "sizeY": 50, "shouldSolve": None, "solveColor": 1, "isGif": None}
        color = ProbablyPython.setNextColor(1, [0,0,255,255], [0,0,0,255], inputs)
        color = ProbablyPython.setNextColor(1, color, [0,0,0,255], inputs)
        self.assertEqual([255,0,0,255], color)

class mazeIntegrationTests(unittest.TestCase):
    def test_mazeGen(self):
        data = {"sizeX": 51, "sizeY": 51, "shouldSolve": None, "solveColor": None, "isGif": None}
        image = ProbablyPython.generateMaze(data)
        img = image.load()
        testArray = []
        for x in range(image.size[0] - 1):
            for y in range(image.size[1] - 1):
                if x % 2 != 0 and y % 2 != 0:
                    testArray.append(img[x, y])
                    self.assertEqual(img[x, y], (255, 255, 255, 255))


    def test_mazeGenWithSolution(self):
        inputsRecieved = {"sizeX": 51, "sizeY": 51, "shouldSolve": True, "solveColor": 1, "isGif": None}
        image = ProbablyPython.generateMaze(inputsRecieved)
        img = image.load()
        testArray = []
        for x in range(image.size[0]-1):
            for y in range(image.size[1]-1):
                if x % 2 != 0 and y % 2 != 0:
                    testArray.append(img[x,y])
                    self.assertNotEqual(img[x,y], (0,0,0,255))


if __name__ == '__main__':
    unittest.main()