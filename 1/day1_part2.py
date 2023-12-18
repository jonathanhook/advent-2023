
import os
import re

word_to_number = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9'
}

def words_to_numbers(match):
    if(len(match) == 1):
        return match
    else:
        return str(word_to_number.get(match))

script_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_directory, 'input.txt')

with open(file_path, 'r') as file:
    lines = file.readlines()

sum = 0;
for line in lines:
    numbers = re.findall(r'(?=([1-9]|one|two|three|four|five|six|seven|eight|nine))', line, flags=re.IGNORECASE)   

    cv = words_to_numbers(numbers[0])
    if(len(numbers) > 1):
        cv += words_to_numbers(numbers[-1])
    else:
        cv += words_to_numbers(numbers[0])

    print(line + " " + cv)
    sum += int(cv)

print(sum)
