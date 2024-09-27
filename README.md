# Python-maze-gen
Tis a thing.
This is a maze generator. It can produce mazes of various sizes. You can produce mazes with solutions as well.
Gifs are available. To use the program, you need to run it with python in the command line. It requires two numbers
at for the sizeX and sizeY values. For an unsolved maze you can use `python ProbablyPython.py 100 100`. For a
solved maze you can use `python ProbablyPython.py 100 100 --shouldSolve --solveColor 2`. To make either of these
into a gif, just add `--isGif` to the end. The solve colors are `1:red&blue, 2:RGB, 3:random, 0:rainbow`.

Example PNG:

![An example solved maze PNG](https://raw.githubusercontent.com/JacobPuff/Python-maze-gen/master/exampleMaze.png)

Example GIF:

![An example maze getting generated and solved as a gif](https://raw.githubusercontent.com/JacobPuff/Python-maze-gen/master/exampleGif.gif)