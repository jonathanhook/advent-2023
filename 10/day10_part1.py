
import os
import sys

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = list()
    for l in lines:
        data.append([char for char in l.strip()])

    return data

def findStart(data):
    for y in range(len(data)):
        for x in range(len(data[y])):
            if data[y][x] == 'S':
                return x, y

def findValidFirstSteps(x, y, data):
    valid = list()

    if y > 0 and (data[y-1][x] == '|' or data[y-1][x] == 'F' or data[y-1][x] == '7'):
        valid.append((x, y-1))
   
    if y < len(data) and (data[y+1][x] == '|' or data[y+1][x] == 'L' or data[y+1][x] == 'J'):
        valid.append((x, y+1))
    
    if x > 0 and (data[y][x-1] == '-' or data[y][x-1] == 'L' or data[y][x-1] == 'F'):
        valid.append((x-1, y))

    if x < len(data[0]) and (data[y][x+1] == '-' or data[y][x+1] == 'J' or data[y][x+1] == '7'):
        valid.append((x+1, y))

    return valid    

def getNextSteps(val, x, y):
    x1 = y1 = x2 = y2 = 0

    if val == '|':
        y1 = 1
        y2 = -1
    elif val == '-':
        x1 = 1
        x2 = -1
    elif val == 'L':
        y1 = -1
        x2 = 1
    elif val == 'J':
        x1 = -1
        y2 = -1
    elif val == '7':
        x1 = -1
        y2 = 1
    elif val == 'F':
        y1 = 1
        x2 = 1

    return (x1 + x, y1 + y),(x2 + x, y2 + y)    
    
def dfs(x, y, data, visited):
    pos = data[y][x]
    nextSteps = getNextSteps(pos, x, y)

    for n in nextSteps:
        val = data[n[1]][n[0]]
        if val == 'S' and len(visited) > 1:
            return len(visited) + 1
        
        if not n in visited:
            visited.append((x, y))
            return dfs(n[0], n[1], data, visited)

def task(input):
    data = parseInput(input)
    x, y = findStart(data)

    firstSteps = findValidFirstSteps(x, y, data)
    assert(len(firstSteps) == 2)

    visited = list()
    visited.append((x, y))
    a = dfs(firstSteps[0][0], firstSteps[0][1], data, visited)
    #b = dfs(firstSteps[0][0], firstSteps[0][1], data, visited)

    return int(a / 2)

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    sys.setrecursionlimit(100000)

    print(test("testInput1.txt", 4))
    print(test("testInput2.txt", 8))
    print(task('input.txt'))

main()