import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        data.append([c for c in l.strip()])

    return data

def bubble(data):
    h = len(data)
    w = len(data[0])
    
    for j in range(w):
        for i in range(h-1, -1, -1):
            if data[i][j] == 'O':
                k=i-1
                while k >= 0 and data[k][j] != '#':
                    if data[k][j] == '.':
                        data[i][j] = '.'
                        data[k][j] = 'O'
                        break
                    k-=1          
    return data

def score(data):
    h = len(data)
    w = len(data[0])
    total = 0

    for i in range(h):
        for j in range(w):
            if data[i][j] == 'O':
                total += h-i

    return total

def task(input):
    data = parseInput(input)
    sorted = bubble(data)
    total = score(sorted)
    
    return total

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test('testInput.txt', 136))
    print(task('input.txt'))

main()