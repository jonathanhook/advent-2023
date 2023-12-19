import os

class Card:
    def __init__(self, id, line):
        data = line.split(':')
        self.id = id
        self.winning = [int(char) for char in data[1].split('|')[0].strip().split(' ') if char]
        self.entries = [int(char) for char in data[1].split('|')[1].strip().split(' ') if char]

def processCard(c, cards):
    score = len(set(c.winning) & set(c.entries))

    total = 1
    for i in range(c.id + 1, c.id + score + 1):
        total += processCard(cards[i], cards)

    return total

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    i = 0;
    cards = list()
    for l in lines:
        cards.append(Card(i, l))
        i += 1
    
    sum = 0
    for c in cards:
        sum += processCard(c, cards)

    return sum

def main(input):
    result = parseInput(input)
    print(result)

main('input.txt')