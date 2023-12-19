import os

def getDistance(held, time):
    return held * (time - held)

def findWinningWays(time, record):
    wins = 0
    for i in range(0, time):
        if getDistance(i, time) > record:
            wins += 1

    return wins

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    times = [int(s) for s in lines[0].split(':')[1].strip().split(' ') if s]
    records = [int(s) for s in lines[1].split(':')[1].strip().split(' ') if s]

    product = 1
    for i in range(0, len(times)):
        product *= findWinningWays(times[i], records[i])

    return product

def main(input):
    result = parseInput(input)
    print(result)

main("input.txt")