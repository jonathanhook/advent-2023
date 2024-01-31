import os
import sys
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, pos):
        self.pos = pos

    def __eq__(self, other):
        return self.pos == other.pos
    
    def __hash__(self):
        return hash(self.pos)

class Edge:
    def __init__(self, a, b, weight):
        self.a = a
        self.b = b
        self.weight = weight

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        data.append([c for c in l.strip()])
    
    return data

def findStartEnd(data):
    start = end = None
    for i in range(len(data[0])):
        if data[0][i] == '.':
            start = Node((i, 0))

    for i in range(len(data[0])):
        if data[-1][i] == '.':
            end = Node((i, len(data)-1))
    
    return start, end

def makeUndirectedGraph(pos, a, weight, visited, nodes, edges, data):
    if pos in nodes:
        b = nodes[pos]
        # hack?
        check = list(filter(lambda e: e.a == a and e.b == b, edges))
        if len(check) == 0:
            edges.append(Edge(a, b, weight))
            edges.append(Edge(b, a, weight))
        return
    
    if pos in visited and visited[pos] == a:
        return
    visited[pos] = a

    possiblePaths = []
    for pp in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
        px = pos[0] + pp[0]
        py = pos[1] + pp[1]

        visitedFromA = (px, py) in visited and visited[(px, py)] == a
        if not visitedFromA and (px > 0 and px <= len(data[0]) - 1) and (py > 0 and py <= len(data) - 1) and data[py][px] != '#':
            possiblePaths.append((px, py))
        
    if len(possiblePaths) > 1:
        b = Node(pos)
        nodes[b.pos] = b
        edges.append(Edge(a, b, weight))
        edges.append(Edge(b, a, weight))
        visited[pos] = b

        for pp in possiblePaths:
            makeUndirectedGraph(pp, b, 1, visited, nodes, edges, data)

    elif len(possiblePaths) == 1:
        makeUndirectedGraph(possiblePaths[0], a, weight + 1, visited, nodes, edges, data)

def showGraph(edges):
    g = nx.DiGraph()
    for e in edges:
        g.add_edge(e.a.pos, e.b.pos, weight=e.weight)

    nx.draw(g, with_labels=True)
    plt.show()

def dfs(current, length, visited, end, edges):
    if current == end:
        return length - 1

    visited[current] = True
    outgoing = list(filter(lambda e: e.a == current and not (e.b in visited), edges))
    max = 0
    for o in outgoing:
        val = dfs(o.b, length + o.weight, visited, end, edges)
        if val > max:
            max = val

    del visited[current]
    return max

def task(input):
    data = parseInput(input)
    start, end = findStartEnd(data)

    edges = []
    nodes = { end.pos : end }
    makeUndirectedGraph(start.pos, start, 1, {}, nodes, edges, data)

    return dfs(start, 0, {}, end, edges)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    sys.setrecursionlimit(1000000)
    print(test('testInput.txt', 154))
    print(task('input.txt'))
main()
