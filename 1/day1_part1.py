
import os
import re

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'input.txt')

with open(file_path, 'r') as file:
    lines = file.readlines()

sum = 0;
for line in lines:
    numbers = re.findall(r'\d', line)

    cv = numbers[0]
    if(len(numbers) > 1):
        cv += numbers[-1]
    else:
        cv += numbers[0]

    print(cv)

    sum += int(cv)

print(sum)
