import os
from enum import Enum
import sys

class Direction(Enum):
    North = 0
    South = 1
    East = 2
    West = 3

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        data.append([c for c in l.strip()])
    
    return data

def countEnergised(energized):
    count = 0
    for i in range(len(energized)):
        for j in range(len(energized[0])):
            if energized[i][j] > 0:
                count += 1

    return count

def visited(x, y, direction, energized):
    mask = 1 << direction.value
    return energized[y][x] & mask

def visit(x, y, direction, energized):
    mask = 1 << direction.value
    energized[y][x] ^= mask

def step(x, y, direction, grid, energized):
    # do the step
    if direction == Direction.North:
        y -= 1
    elif direction == Direction.South:
        y += 1
    elif direction == Direction.East:
        x += 1
    elif direction == Direction.West:
        x -= 1

    # check if in bounds
    if (x < 0 or x >= len(grid[0])) or (y < 0 or y >= len(grid)):
        return
    # check if already visted in this direction
    elif visited(x, y, direction, energized):
        return

    # mark point as visited
    visit(x, y, direction, energized)

    # decide on next steps(s)
    val = grid[y][x]
    if val == '.':
        step(x, y, direction, grid, energized)
    elif val == '/':
        step(x, y, Direction((direction.value + 2) % 4), grid, energized)
    elif val == '\\':
        new = Direction((direction.value + 1) % 4)
        if direction.value % 2 == 0:
            new = Direction((direction.value - 1) % 4)
        step(x, y, new, grid, energized)
    elif val == '-':
        if direction == Direction.East or direction == Direction.West:
            step(x, y, direction, grid, energized)
        else:
            step(x, y, Direction.East, grid, energized)
            step(x, y, Direction.West, grid, energized)
    elif val == '|':
        if direction == Direction.North or direction == Direction.South:
            step(x, y, direction, grid, energized)
        else:
            step(x, y, Direction.North, grid, energized)
            step(x, y, Direction.South, grid, energized)

def resetEnergised(data):
    energized = []
    for i in range(len(data)):
        energized.append([])
        for j in range(len(data[0])):
            energized[i].append(0)
    return energized

def tryEntry(x, y, direction, data, energised, max):
    step(x, y, direction, data, energised)
    val = countEnergised(energised)
    if val > max:
        return val
    return max

def task(input):
    data = parseInput(input)

    w = len(data[0])
    h = len(data)
    max = 0
    for i in range(h):
        max = tryEntry(-1, i, Direction.East, data, resetEnergised(data), max)
        max = tryEntry(w, i, Direction.West, data, resetEnergised(data), max)

    for i in range(w):
        max = tryEntry(i, -1, Direction.South, data, resetEnergised(data), max)
        max = tryEntry(i, h, Direction.North, data, resetEnergised(data), max)
    
    return max

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    sys.setrecursionlimit(100000)
    
    print(test('testInput.txt', 51))
    print(task('input.txt'))

main()