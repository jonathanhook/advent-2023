import os

class Node:
    def __init__(self, val, left, right):
        self. val = val
        self.left = left
        self.right = right

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = list()
    data.append(lines[0].strip())

    nodes = list()
    for l in lines:
        nodes.append(Node(l[0:3], l[7:10], l[12:15]))

    data.append(nodes)

    return data

def fineNode(val, map):
    for m in map:
        if m.val == val:
            return m
    return None

def followDirections(start, directions, map):
    steps = 0
    pos = start
    while True:
        for d in directions:
            node = fineNode(pos, map)            
            
            if(node.val == 'ZZZ'):
                return steps
            
            steps += 1
            if d == 'L':
                pos = node.left
            elif d == 'R':
                pos = node.right

def main(input):
    data = parseInput(input)

    steps = followDirections('AAA', data[0], data[1])
    print(steps)

main('Input.txt')