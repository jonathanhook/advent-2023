import os

def getDistance(held, time):
    return held * (time - held)

def findWinningWays(time, record):
    min = 0
    max = 0

    for i in range(0, time):
        if getDistance(i, time) > record:
            min = i
            break

    for j in range(time, 0, -1):
        if getDistance(j, time) > record:
            max = j
            break

    return max - min + 1

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    time = int(lines[0].split(':')[1].strip().replace(' ', ''))
    record = int(lines[1].split(':')[1].strip().replace(' ', ''))

    return findWinningWays(time, record)

def main(input):
    result = parseInput(input)
    print(result)

main("input.txt")