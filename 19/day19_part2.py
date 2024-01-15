
import copy
import os
import re

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    rules = {}
    for l in lines:
        if l[0] != '{' and l[0] != '\n':
            bits = l.strip().split('{')
            id = bits[0]
            rule = bits[1][0:-1]
            rules[id] = rule
    return rules

def exploreCombinations(rule, allowedValues, rules):
    if rule == 'A':
        product = 1
        for c in allowedValues.values():
            range = c[1] - (c[0] - 1)
            product *= range
        return product
    elif rule == 'R':
        return 0
    elif rule in rules:
        rule = rules[rule]
    
    ruleBits = rule.split(',')
    positive = ruleBits[0]
    negative = rule[len(ruleBits[0])+1:]

    conditionBits = re.split('([<>] *)', positive)
    category = conditionBits[0]
    operator = conditionBits[1]

    posBits = conditionBits[2].split(':')
    value = int(posBits[0])
    positiveOutcome = posBits[1]

    positiveAllowed = copy.deepcopy(allowedValues)
    negativeAllowed = copy.deepcopy(allowedValues)
    
    if operator == '<':
        positiveAllowed[category] = (positiveAllowed[category][0], value - 1)
        negativeAllowed[category] = (value, negativeAllowed[category][1])
    else:
        positiveAllowed[category] = (value + 1, positiveAllowed[category][1])
        negativeAllowed[category] = (negativeAllowed[category][0], value)

    return exploreCombinations(positiveOutcome, positiveAllowed, rules) + exploreCombinations(negative, negativeAllowed, rules)

def task(input):
    rules = parseInput(input)

    allowedValues = {
        'x':(1,4000),
        'm':(1,4000),
        'a':(1,4000),
        's':(1,4000)
    }

    return exploreCombinations('in', allowedValues, rules)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput.txt', 167409079868000))
    print(task('input.txt'))
main()