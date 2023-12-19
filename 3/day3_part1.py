
import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    return [list(line.strip()) for line in lines]

def checkPosition(data, rows, cols, i, j):
    if(i > 0 and i < rows and j > 0 and j < cols):
        return not data[i][j].isdigit() and data[i][j] != '.'
    
    return False

def processData(data):

    rows = len(data)
    cols = len(data[0])

    sum = 0;
    currentNumer = ''
    hasSymbol = False

    for i in range(0, rows):
        for j in range(0, cols):
            char = data[i][j]

            if(not char.isdigit()):
                if(hasSymbol):
                    sum += int(currentNumer)

                hasSymbol = False
                currentNumer = ''
            else:
                for k in range(-1, 2):
                    for l in range(-1, 2):
                        hasSymbol = hasSymbol or checkPosition(data, rows, cols, i + k, j + l)

                currentNumer += char
        
    return sum

def main(input):
    data = parseInput(input)
    result = processData(data)

    print(result)

main('input.txt')