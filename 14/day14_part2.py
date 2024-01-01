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

def rotate(data):
    w = len(data[0])
    h = len(data)

    rotated = []
    for i in range(w):
        row = []
        for j in range(h-1, -1, -1):
            row.append(data[j][i])
        rotated.append(row)
    return rotated

def cycle(data):
    north = bubble(data)
    west = bubble(rotate(north))
    south = bubble(rotate(west))
    east = bubble(rotate(south))
    return rotate(east)

def task(input):
    data = parseInput(input)

    memory = dict()
    for i in range(5000):
        data = cycle(data)
        hash = str(data)
        if not hash in memory:
            memory[hash] = [i]
        else:
            memory[hash].append(i)
            gap = memory[hash][1] - memory[hash][0]

            remainder = 1000000000 - i - 1
            divisor = remainder / gap
            
            if divisor.is_integer():
                return score(data)

    return -1

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test('testInput.txt', 64))
    print(task('input.txt'))

main()