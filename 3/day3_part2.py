import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    return [list(line.strip()) for line in lines]

def checkPosition(data, rows, cols, i, j):
    if(i > 0 and i < rows and j > 0 and j < cols):
        return not data[i][j].isdigit() and data[i][j] == '*'
    
    return False

def processData(data):
    rows = len(data)
    cols = len(data[0])

    gears = dict()
    currentNumer = ''
    currentStarPos = ''
    hasStar = False

    for i in range(0, rows):
        for j in range(0, cols):
            char = data[i][j]

            if(not char.isdigit()):
                if(hasStar):
                    if(not currentStarPos in gears):
                        gears[currentStarPos] = list()

                    gears[currentStarPos].append(currentNumer)

                hasStar = False
                currentNumer = ''
                currentStarPos = ''
            else:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        foundStarHere = checkPosition(data, rows, cols, i + k, j + l)
                        if(foundStarHere):
                            currentStarPos = str(i + k) + ',' + str(j + l)
                            hasStar = hasStar or foundStarHere

                currentNumer += char

    sum = 0;
    for g in gears:
        if(len(gears[g]) > 1):
            product = 1
            for n in gears[g]:
                product *= int(n)
            sum += product

    return sum

def main(input):
    data = parseInput(input)
    result = processData(data)

    print(result)

main('input.txt')