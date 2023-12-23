import math
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
    for l in lines[2:]:
        nodes.append(Node(l[0:3], l[7:10], l[12:15]))

    data.append(nodes)

    return data

def findAllEnding(e, map):
    all = list()
    for m in map:
        if m.val[2:3] == e:
            all.append(m)
    return all

def findNode(val, map):
    for m in map:
        if m.val == val:
            return m
    return None

def followPath(start, directions, map):
    steps = 0
    pos = start
    while True:
        for d in directions:
            node = findNode(pos, map)            
            
            if(node.val[2:3] == 'Z'):
                return steps
            
            steps += 1
            if d == 'L':
                pos = node.left
            elif d == 'R':
                pos = node.right

def findLCMs(directions, map):
    multiples = list()
    for t in findAllEnding('A', map):
        multiples.append(followPath(t.val, directions, map))

    return multiples

def main(input):
    data = parseInput(input)
    multiples = findLCMs(data[0], data[1])
    print(math.lcm(*multiples))

main('input.txt')