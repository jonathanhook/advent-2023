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

def unfold(data):
    unfolded = list()
    for i in range(len(data)):
        uRecord = ''
        for j in range(5):
            uRecord += data[i][0]
            if j < 4:
                uRecord += '?'
        
        uGroups = data[i][1] * 5
        unfolded.append((uRecord, uGroups))
    return unfolded

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
    if groups[0] == 0:
        justFinished = True
        midGroup = False
        newGroups = groups[1:]
    else:
        justFinished = False
        newGroups = groups[:]

    found = 0

    # only skip if slot is ? or .
    if not midGroup and record[0] != '#':
        found += dtree(record[1:], newGroups, False, debug + '.')
    
    # only place one if:
    # - we've not just completed a group
    # - the current slot is not a .
    if not justFinished and record[0] != '.':
        newGroups[0] -= 1
        found += dtree(record[1:], newGroups, True, debug + '#')

    return found
   
def task(input):
    data = parseInput(input)
    unfolded = unfold(data)

    sum = 0
    for i in range(len(unfolded)):
        print(str(i) + ' of ' + str(len(unfolded)) + ': ' + unfolded[i][0])
        sum += dtree(unfolded[i][0], unfolded[i][1], False, '')

    return sum

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test('testInput.txt', 525152))
    print(task('input.txt'))
main()