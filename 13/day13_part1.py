import os
import random

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

def findReflection(grid):
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
                    return i+1
                elif grid[k][l] != grid[k][r]:
                    breakout = True
                    break
    return -1

def task(input):
    data = parseInput(input)

    summary = 0
    for i in range(len(data)):
        cols = findReflection(data[i])
        if cols != -1:
            summary += cols
        else:
            rows = findReflection(rotate(data[i]))
            if rows != -1:
                summary += (rows * 100)

    return summary

def randomDebug(input):
    data = parseInput(input)
    r = random.randint(0, len(data))

    for i in range(len(data[r])):
        for j in range(len(data[r][0])):
            print(data[r][i][j], end='')
        print()
    
    print('C ' + str(findReflection(data[r])))
    print('R ' + str(findReflection(rotate(data[r]))))

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    #randomDebug('input.txt')

    print(test('testInput1.txt', 405))
    print(test('testInput2.txt', 709))
    print(test('testInput3.txt', 11))
    print(test('testInput4.txt', 9))
    print(test('testInput5.txt', 400))
    print(task('input.txt'))

main()