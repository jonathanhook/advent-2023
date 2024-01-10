import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        hex = l.strip().split(' ')[2]
        distance = int(hex[2:7], 16)
        dCode = int(hex[7:8])
        direction = 'R'
        if dCode == 1:
            direction = 'D'
        elif dCode == 2: 
            direction = 'L'
        elif dCode == 3: 
            direction = 'U'

        data.append((direction, distance))

    return data

def getVertices(data):
    verts = [(0, 0)]
    x = y = 0
    perimeter = 0
    for d in data:
        if d[0] == 'R':
            x += d[1]
        elif d[0] == 'L':
            x -= d[1]
        elif d[0] == 'D':
            y += d[1]
        elif d[0] == 'U':
            y -= d[1]
        perimeter += d[1]
        verts.append((x, y))
    return verts, perimeter

def shoelace(verts, perim):
    xSum = ySum = 0
    size = len(verts)
    for i in range(size):
        xSum += (verts[i][0] * verts[(i + 1) % size][1])
        ySum += (verts[i][1] * verts[(i + 1) % size][0])
    return int((abs(xSum - ySum) / 2) + (perim / 2) + 1)

def task(input):
    data = parseInput(input)
    verts, perim = getVertices(data)
    area = shoelace(verts, perim)
    return area

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput.txt', 952408144115))
    print(task('input.txt'))

main()