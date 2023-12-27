import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    galaxy = 1
    data = list()
    colHasGalaxies = [False] * len(lines[0].strip())

    for l in lines:
        row = list()
        for c in l.strip():
            if c == '.':
                row.append(0)
            else: 
                row.append(galaxy)
                colHasGalaxies[len(row) - 1] = True
                galaxy += 1

        data.append(row)

    return data

def getCoords(data, xf):
    coords = dict()
    yS = 0
    
    for y in range(len(data)):
        rowEmpty = True
        xS = 0
        for x in range(len(data[0])):
            id = data[y][x]
            if id > 0:
                coords[id] = (x + xS, y + yS)
                rowEmpty = False
            else:
                colEmpty = True
                for z in range(len(data)):
                    if data[z][x] != 0:
                        colEmpty = False
                if colEmpty:
                    xS += xf-1
        if rowEmpty:
            yS += xf-1
    return coords

def getDistances(coords):
    pairs = list()
    for i in range(1, len(coords) + 1):
        row = list()
        for j in range(1, len(coords) + 1):
            distance = abs(coords[i][0] - coords[j][0]) + abs(coords[i][1] - coords[j][1])
            row.append(distance)
        pairs.append(row)
    return pairs

def sumDistances(distances):
    sum = 0
    for i in range(len(distances)):
        for j in range(0, i):
            sum += distances[i][j]
    return sum

def task(input, scaleFactor):
    data = parseInput(input)
    coords = getCoords(data, scaleFactor)
    distances = getDistances(coords)
    sum = sumDistances(distances)

    return sum

def test(input, scaleFactor, expected):
    result = task(input, scaleFactor)
    return result == expected

def main():
    print(test("testInput.txt", 2, 374))
    print(test("testInput.txt", 10, 1030))
    print(test("testInput.txt", 100, 8410))
    print(task('input.txt', 1000000))

main()