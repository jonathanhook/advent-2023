
import copy
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
    
def dfs(x, y, data, visited, map):
    pos = data[y][x]
    markMap(x, y, map, pos)
    nextSteps = getNextSteps(pos, x, y)

    for n in nextSteps:
        val = data[n[1]][n[0]]
        if val == 'S' and len(visited) > 1:
            #markMap(x, y, map, val)
            return len(visited) + 1
        
        if not n in visited:
            #markMap(x, y, map, val)
            visited.append((x, y))
            return dfs(n[0], n[1], data, visited, map)

def initMap(w, h):
    map = list()
    for i in range(h):
        map.append(['0'] * w)
        
    return map

def markMap(x, y, map, val):
    map[y][x] = val

def expandMap(map):
    eMap = list()
    for i in range(len(map)):
        eRow = list()
        for j in range(len(map[i])):
            eRow.append(map[i][j])

            if j < len(map[i]) - 1:
                a = map[i][j]
                b = map[i][j+1]

                if (a == 'S' or a == '-' or 'F' or 'L') and (b == '-' or b == '7' or b == 'J' or b == 'S'):
                    eRow.append('-')
                else:
                    eRow.append('x')

        eRow.insert(0, 'x')
        eRow.append('x')
        eMap.append(eRow)

    for i in range(1, len(eMap), 2):
        dRow = list()
        for j in range(0, len(eMap[i])):
            a = eMap[i-1][j]
            b = eMap[i][j]

            if(a == 'S' or a == '|' or a == 'F' or a == '7') and (b == '|' or b == 'L' or b == 'J' or b == 'S'):
                dRow.append('|')
            else: 
                dRow.append('x')
        eMap.insert(i, dRow)

    eMap.insert(0, ['x'] * len(eMap[i]))
    eMap.append(['x'] * len(eMap[i]))

    return eMap

def floodFill(i, j, eMap):
    if i < 0 or i >= len(eMap) or j < 0 or j >= len(eMap[0]):
        return 0
    elif eMap[i][j] != '0' and eMap[i][j] != 'x':
        return 0
    else:
        eMap[i][j] = '1'
        floodFill(i-1, j, eMap)
        floodFill(i+1, j, eMap)
        floodFill(i, j+1, eMap)
        floodFill(i, j-1, eMap)
        return 0

def countIsolated(map):
    count = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == '0':
                count += 1
    return count

def dumpMap(map, friendly):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if not friendly:
                print(map[i][j], end="")
            elif map[i][j] == '1':
                print(' ', end="")
            elif map[i][j] == '0' or map[i][j] == 'x':
                print('.', end="")
            else:
                print('#', end="")
        print()

def task(input):
    data = parseInput(input)
    map = initMap(len(data[0]), len(data))
    x, y = findStart(data)
    markMap(x, y, map, 'S')

    firstSteps = findValidFirstSteps(x, y, data)
    assert(len(firstSteps) == 2)

    visited = list()
    visited.append((x, y))
    a = dfs(firstSteps[0][0], firstSteps[0][1], data, visited, map)

    eMap = expandMap(map)
    floodFill(0, 0, eMap)

    #dumpMap(eMap, True)

    return countIsolated(eMap)

def test(input, expected):
    result = task(input)
    print(result)
    return result == expected

def main():
    sys.setrecursionlimit(100000)

    print(test("testInput3.txt", 4))
    print(test("testInput4.txt", 8))
    print(test("testInput5.txt", 10))
    print(task('input.txt'))

main()