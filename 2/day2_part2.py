import os
import re

def getPower(game):
    data = game.split(': ')[1]
    reveals = re.split(r'[;,]', data)

    max = {'red': 0, 'green': 0, 'blue': 0}

    for r in reveals:
        parts = r.strip().split(' ')
        count = int(parts[0])
        colour = parts[1]

        if(count > max[colour]):
            max[colour] = count

    return max['red'] * max['green'] * max['blue']

def main(red, green, blue):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, 'input.txt')

    with open(file_path, 'r') as file:
        lines = file.readlines()

    sum = 0
    for line in lines:
        sum += getPower(line)

    print(sum)

main(12, 13, 14)

