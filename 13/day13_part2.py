import copy
import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = list()
    grid = list()
    for l in lines:
        if l == "\n":
            data.append(grid)
            grid = list()
        else:
            grid.append([c for c in l.strip()])
    
    return data

def rotate(data):
    w = len(data[0])
    h = len(data)

    rotated = []
    for i in range(w-1, -1, -1):
        row = []
        for j in range(h):
            row.append(data[j][i])
        rotated.append(row)
    return rotated

def findReflection(grid, skip):
    w = len(grid[0])
    h = len(grid)

    for i in range(w-1):
        breakout = False
        for j in range(w):
            if breakout:
                break

            for k in range(h):
                l = i-j
                r = i+1+j

                if l < 0 or r >= w:
                    val = i+1
                    if val != skip:
                        return val
                elif grid[k][l] != grid[k][r]:
                    breakout = True
                    break
    return -1

def getLof(grid, original):
    cols = findReflection(grid, original[0])
    rows = findReflection(rotate(grid), original[1])
    return (cols, rows)

def task(input):
    data = parseInput(input)

    summary = 0
    for i in range(len(data)):
        originalLof = getLof(data[i], (-1, -1))
        
        breakout = False
        for j in range(len(data[i])):
            if breakout:
                break

            for k in range(len(data[i][0])):
                fixed = copy.deepcopy(data[i])
                if fixed[j][k] == '#': 
                    fixed[j][k] = '.'
                else: 
                    fixed[j][k] = '#'

                if j == 1 and k == 4:
                    m = 0

                fixedLof = getLof(fixed, originalLof)
                if fixedLof[0] != -1 and fixedLof[0] != originalLof[0]:
                    summary += fixedLof[0]
                    breakout = True
                    break
                elif fixedLof[1] != -1 and fixedLof[1] != originalLof[1]:
                    summary += fixedLof[1] * 100
                    breakout = True
                    break

    return summary

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test('testInput1.txt', 400))
    print(test('testInput2.txt', 1400))
    print(task('input.txt'))

main()