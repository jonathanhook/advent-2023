import math
import os
import numpy as np
import numpy.polynomial.polynomial as poly

class Step():
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.count = count

    def hash(self):
        return str(self.count) + ':' + str(self.x) + ':' + str(self.y)

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        data.append([c for c in l.strip()])
    return data

def findStart(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 'S':
                return (j, i)

def findPlots(data, steps):
    startPos = findStart(data)
    width = len(data[0])
    height = len(data)
    queue = [Step(startPos[0], startPos[1], 0)]
    explored = {}
    found = []

    while len(queue) > 0:
        step = queue.pop(0)
        nCount = step.count + 1

        if nCount == (steps + 1):
            found.append((step.x, step.y))
        else:
            for next in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx = step.x + next[0]
                ny = step.y + next[1]
                nextStep = Step(nx, ny, nCount)

                if not nextStep.hash() in explored and data[ny % height][nx % width] != '#':
                    queue.append(nextStep)
                    explored[nextStep.hash()] = True        
    return len(found)

def task(input, steps):
    data = parseInput(input)
    dim = len(data)
    
    x0 = math.floor(dim / 2)
    x1 = dim + x0
    x2 = x1 + dim

    y0 = findPlots(data, x0)
    y1 = findPlots(data, x1)
    y2 = findPlots(data, x2)
    
    x = np.array([x0, x1, x2])
    y = np.array([y0, y1, y2])
    c = poly.polyfit(x, y, 2)

    return int(poly.polyval(steps, c))

def test(input, steps, expected):
    result = task(input, steps)
    return result == expected

def main():
    print(task('input.txt', 26501365))
main()