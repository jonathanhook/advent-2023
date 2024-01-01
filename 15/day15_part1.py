import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    steps = []
    for l in lines:
        [steps.append(s) for s in l.strip().split(',')]

    return steps

def hash(val):
    currentValue = 0
    for c in val:
        currentValue += ord(c)
        currentValue *= 17
        currentValue %= 256
    return currentValue    

def task(input):
    data = parseInput(input)

    result = 0
    for d in data:
        result += hash(d)

    return result

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test('testInput.txt', 1320))
    print(task('input.txt'))

main()