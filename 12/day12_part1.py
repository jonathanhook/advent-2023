import os

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = list()
    for l in lines:
        parts = l.strip().split(' ')
        record = parts[0]
        groups = [int(g) for g in parts[1].split(',')]
        data.append((record, groups))

    return data

def decisionTree(record, groups, place, debug):
    #if len(groups) == 0:
    #    return 1
    if groups[0] > len(record):
        return 0
    
    if place:
        toPlace = groups[0]
        for i in range(toPlace):
            slot = record[i]
            if slot == '.':
                return 0
            else:
                debug += '#'

        if ((i+1) > len(record) and len(groups) > 1) and record[i+1] == '#':
            return 0

        if len(groups) > 1:
            debug += '.'
            return decisionTree(record[toPlace + 1:], groups[1:], True, debug) + decisionTree(record[toPlace + 1:], groups[1:], False, debug)
        else:
            return 1
    else:
        debug += '.'
        return decisionTree(record[1:], groups, True, debug) + decisionTree(record[1:], groups, False, debug)

def task(input):
    data = parseInput(input)

    i = 1
    result = decisionTree(data[i][0], data[i][1], True, '')
    result += decisionTree(data[i][0], data[i][1], False, '')
    print(result)

    return result

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test('testInput.txt', 21))
main()