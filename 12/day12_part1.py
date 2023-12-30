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

def dtree(record, groups, midGroup, debug):
    # if not enough left to complete, give up
    if sum(groups) > len(record):
        return 0
    elif sum(groups) == 0:
        if '#' in record:
            return 0
        else:
            return 1
    
    # find out if just finished a group
    justFinished = False
    newGroups = groups[:]
    if newGroups[0] == 0:
        justFinished = True
        midGroup = False
        newGroups = newGroups[1:]

    found = 0

    # only skip if slot is ? or .
    if not midGroup and record[0] != '#':
        found += dtree(record[1:], newGroups[:], False, debug[:] + '.')

    # only place one if:
    # - we've not just completed a group
    # - the current slot is not a .
    if not justFinished and record[0] != '.':
        newGroups[0] -= 1
        found += dtree(record[1:], newGroups[:], True, debug[:] + '#')

    return found
   
def task(input):
    data = parseInput(input)

    sum = 0
    for i in range(len(data)):
        sum += dtree(data[i][0], data[i][1], False, '')

    return sum

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test('testInput.txt', 21))
    print(task('input.txt'))
main()