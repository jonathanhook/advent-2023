import os
import re

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

def dash(boxes, box, label):
    for i in range(len(boxes[box])):
        bl = boxes[box][i][0]
        if bl == label:
            del boxes[box][i]
            return

def equals(boxes, box, label, fl):
    for i in range(len(boxes[box])):
        bl = boxes[box][i][0]
        if bl == label:
            boxes[box][i] = (label, fl)
            return
    boxes[box].append((label, fl))

def doStep(boxes, s):
    parts = re.split('[-=]', s)
    
    label = parts[0]
    box = hash(label)

    if "-" in s:
        dash(boxes, box, label)
    else:
        fl = parts[1]
        equals(boxes, box, label, fl)

    return 0

def getFocussingPower(boxes):
    sum = 0
    for i in range(256):
        box = boxes[i]
        for j in range(len(box)):
            lens = box[j]
            power = (1+i) * (j+1) * int(lens[1])
            sum += power 
    return sum

def task(input):
    data = parseInput(input)

    boxes = {}
    for i in range(256):
        boxes[i] = []

    for d in data:
        doStep(boxes, d)

    return getFocussingPower(boxes)

def test(input, expected):
    result = task(input)
    return result == expected

def main():
    print(test('testInput.txt', 145))
    print(task('input.txt'))

main()