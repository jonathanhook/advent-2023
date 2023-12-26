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
        rowHasGalaxies = False

        for c in l.strip():
            if c == '.':
                row.append(0)
            else: 
                rowHasGalaxies = True
                row.append(galaxy)
                colHasGalaxies[len(row) - 1] = True
                galaxy += 1

        data.append(row)

        if not rowHasGalaxies:
            data.append([0] * (len(lines[0]) - 1))

    for i in range(len(data)):
        for j in range(len(colHasGalaxies) - 1, 0, -1):
            if not colHasGalaxies[j]:
                data[i].insert(j, 0)

    return data

def getCoords(data):
    coords = dict()
    for y in range(len(data)):
        for x in range(len(data[0])):
            id = data[y][x]
            if id > 0:
                coords[id] = (x, y)
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

def task(input):
    data = parseInput(input)
    coords = getCoords(data)
    distances = getDistances(coords)
    sum = sumDistances(distances)

    return sum

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test("testInput.txt", 374))
    print(task('input.txt'))

main()