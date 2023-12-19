import os

def scoreCard(card):
    data = card.split(':')[1]
    winning = [int(char) for char in data.split('|')[0].strip().split(' ') if char]
    entries = [int(char) for char in data.split('|')[1].strip().split(' ') if char]

    score = 0
    for e in entries:
        if e in winning:
            if(score == 0):
                score = 1
            else:
                score *= 2

    return score

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    sum = 0
    for l in lines:
        sum += scoreCard(l)

    return sum

def main(input):
    result = parseInput(input)
    print(result)

main('input.txt')