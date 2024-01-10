import os
import sys

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        parts = l.strip().split(' ')
        data.append((parts[0], int(parts[1]), parts[2]))

    return data

def printHole(hole):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, 'output.txt')

    with open(file_path, 'w') as f:
        for i in range(len(hole)):
            for j in range(len(hole[0])):
                f.write(hole[i][j])
            f.write('\n')

def getBounds(data):
    xMax = xMin = 0
    yMax = yMin = 0
    x = y = 0
    for d in data:
        if d[0] == 'R':
            x += d[1]
        elif d[0] == 'L':
            x -= d[1]
        elif d[0] == 'D':
            y += d[1]
        elif d[0] == 'U':
            y -= d[1]
        
        if x > xMax: 
            xMax = x
        elif x < xMin:
            xMin = x
        elif y > yMax:
            yMax = y
        elif y < yMin:
            yMin = y

    return (xMax - xMin + 1, yMax - yMin + 1), (abs(xMin), abs(yMin))

def digHole(data, bounds, start):
    hole = []
    for i in range(bounds[1]):
        hole.append(['.'] *  (bounds[0]))

    x = start[0]
    y = start[1]
    for d in data:
        for j in range(d[1]):
            if d[0] == 'R':
                x += 1
            elif d[0] == 'L':
                x -= 1
            elif d[0] == 'D':
                y += 1
            elif d[0] == 'U':
                y -= 1
            hole[y][x] = '#'

    return hole

def findStart(hole):
    for i in range(len(hole)):
        if hole[i][0] == '#' and hole[i][1] == '.':
            return (1, i)

def fillHole(hole, j, i):
    if i < 0 or i >= len(hole) or j < 0 or j >= len(hole[0]):
        return
    elif hole[i][j] == '#':
        return
    else:
        hole[i][j] = '#'
        fillHole(hole, j-1, i)
        fillHole(hole, j+1, i)
        fillHole(hole, j, i-1)
        fillHole(hole, j, i+1)
        return

def calcArea(hole):
    area = 0
    for i in range(len(hole)):
        for j in range(len(hole[0])):
            if hole[i][j] == '#':
                area += 1
    return area

def task(input):
    data = parseInput(input)
    bounds = getBounds(data)
    hole = digHole(data, bounds[0], bounds[1])
    start = findStart(hole)
    
    fillHole(hole, start[0], start[1])
    printHole(hole)

    return calcArea(hole)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    sys.setrecursionlimit(100000)
    print(test('testInput.txt', 62))
    print(task('input.txt'))

main()