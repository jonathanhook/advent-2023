import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = list()
    for l in lines:
        data.append([int(char) for char in l.split(' ') if char])

    return data

def extrapolate(data):
    diffs = list()
    for i in range(0, len(data) - 1):
        this = data[i]
        next = data[i+1]
        diffs.append(next - this)
        
    if all([v == 0 for v in diffs]):
        return data[-1]
    else:
        return data[-1] + extrapolate(diffs)       

def extrapolateAll(data):
    sum = 0
    for d in data:
        sum += extrapolate(d)
    return sum

def main(input):
    data = parseInput(input)
    result = extrapolateAll(data)
    print(result)

main('input.txt')