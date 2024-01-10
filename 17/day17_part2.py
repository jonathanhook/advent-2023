import os
from enum import Enum
import time

class Direction(Enum):
    North = 0
    South = 1
    East = 2
    West = 3

class Node():
    def __init__(self, x, y, dir, streak=0, prev=None, g=0, h=0):
        self.x = x
        self.y = y
        self.dir = dir
        self.streak = streak
        self.prev = prev
        self.g = g
        self.h = h
        self.f = g + h
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.dir == other.dir and self.streak == other.streak
    
    def sameLocation(self, other):
        return self.x == other.x and self.y == other.y
    
    def __str__(self):
        return str(self.x) + ' ' + str(self.y) + ' ' + str(self.dir) + ' ' + str(self.streak)

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        data.append([int(c) for c in l.strip()])

    return data

def aStar(data):
    closed = {}
    open = {}
    
    target = Node(len(data[0])-1, len(data)-1, None)
    start = Node(0, 0, Direction.East)    
    open[str(start)] = start

    while len(open) > 0:
        current = None
        if len(open) > 0:
            for key in open:
                if current is None:
                    current = open[key]
                elif open[key].f < current.f:
                    current = open[key]

        current = open.pop(str(current))
        closed[str(current)] = current

        if target.sameLocation(current):
            if current.streak >= 4:
                printResult(current, data)
                return current.g
        else:
            possibleMoves = [(0, -1, Direction.North), (0, 1, Direction.South), (1, 0, Direction.East), (-1, 0, Direction.West)]
            for delta in possibleMoves:
                nx = current.x + delta[0]
                ny = current.y + delta[1]

                # out of bounds
                if nx < 0 or ny < 0 or nx >= len(data[0]) or ny >= len(data):
                    continue

                # step backwards
                if (not current.prev is None) and (nx == current.prev.x and ny == current.prev.y):
                    continue

                # ignore any nodes that aren't the same direction if streak below 4
                sameDirection = current.dir == delta[2]
                if not sameDirection and current.streak < 4:
                    continue

                # work out the streak
                streak = 1
                if sameDirection:
                    streak += current.streak

                # ignore 10th node in a row
                if streak > 10:
                    continue

                g = data[ny][nx] + current.g
                h = abs(target.x - nx) + abs(target.y + ny)
                child = Node(nx, ny, delta[2], streak, current, g, h)

                hash = str(child)
                if not hash in closed and not hash in open:
                    open[hash] = child
                #hash = str(child)
                #if not hash in closed and not (hash in open and open[hash].g < g):
                #    open[hash] = child
    return 0

def inPath(x, y, node):
    if node.x == x and node.y == y:
        return True
    elif node.prev is None:
        return False
    else:
        return inPath(x, y, node.prev)

def printResult(node, grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            val = grid[i][j]
            if inPath(j, i, node):
                val = '*'
            print(val, end='')
        print('')

def task(input):
    data = parseInput(input)
    start = time.time()
    result = aStar(data)
    print(time.time() - start)
    return result

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput2.txt', 71))
    print(test('testInput1.txt', 94))
    print(task('input.txt'))

main()