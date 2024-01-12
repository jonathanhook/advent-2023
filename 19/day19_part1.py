import os
import re

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    parts = []
    rules = {}
    for l in lines:
        if l == '\n':
            continue
        elif l[0] == '{':
            categories = l.strip()[1:-1].split(',')
            map = {}
            for c in categories:
                cSplit = c.split('=')
                map[cSplit[0]] = int(cSplit[1])
            parts.append(map)
        else:
            rSplit = l.strip().split('{') 
            name = rSplit[0]
            rParts = rSplit[1][0:-1].split(',')
            conditions = []
            for r in rParts:
                bits = r.split(':')
                if len(bits) > 1:
                    cBits = re.split('([<>] *)', bits[0])
                    conditions.append(((cBits[0], cBits[1], int(cBits[2])), bits[1]))
                else:
                    conditions.append((None, bits[0]))
                rules[name] = conditions               
    return parts, rules

def followRule(id, part, rules):
    if id == 'A':
        return True
    elif id == 'R':
        return False
    
    rule = rules[id]
    for r in rule:
        if r[0] == None or (r[0][1] == '>' and part[r[0][0]] > r[0][2]) or (r[0][1] == '<' and part[r[0][0]] < r[0][2]):
            return followRule(r[1], part, rules)

def processParts(parts, rules):
    sum = 0
    for p in parts:
        if followRule('in', p, rules):
            sum += (p['x'] + p['m'] + p['a'] + p['s'])
    return sum

def task(input):
    parts, rules = parseInput(input)
    return processParts(parts, rules)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput.txt', 19114))
    print(task('input.txt'))
main()