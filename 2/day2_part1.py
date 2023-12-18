import os
import re

def isPossible(game, red, green, blue):
    data = game.split(': ')[1]
    reveals = re.split(r'[;,]', data)

    for r in reveals:
        parts = r.strip().split(' ')
        count = int(parts[0])
        colour = parts[1]

        limit = blue
        if(colour == "red"):
            limit = red
        elif(colour == "green"):
            limit = green

        if(count > limit):
            return False

    return True

def main(red, green, blue):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, 'input.txt')

    with open(file_path, 'r') as file:
        lines = file.readlines()

    sum = 0
    i = 1
    for line in lines:
        if(isPossible(line, red, green, blue)):
            sum += i

        i += 1

    print(sum)

main(12, 13, 14)

