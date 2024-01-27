import copy
import os
import sys

Infinity = -999999

class Node:
    def __init__(self, pos, val):
        self.pos = pos
        self.val = val

    def __eq__(self, other):
        return self.pos == other.pos
    
    def __hash__(self):
        return hash(self.pos)

class Edge:
    def __init__(self, a, b, weight):
        self.a = a
        self.b = b
        self.weight = weight

class DState:
    def __init__(self, shortest=Infinity, previous=None):
        self.shortest = shortest
        self.previous = previous

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
            start = Node((i, 0), '.')

    for i in range(len(data[0])):
        if data[-1][i] == '.':
            end = Node((i, len(data)-1), '.')
    
    return start, end

def makeGraph(x, y, a, visited, edges, nodes, data):
    if x < 0 or y < 0 or x >= len(data[0]) or y >= len(data) or (x, y) in visited:
        return
    
    visited.append((x, y))
    step = data[y][x]

    if step == '#':
        return
    elif step == '.':
        if y == len(data) - 1:
            b = Node((x, y), step)
            nodes[b.pos] = b
            edges.append(Edge(a, b, len(visited) * 1))
            return
        
        for next in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            nx = x + next[0]
            ny = y + next[1]
            makeGraph(nx, ny, a, copy.deepcopy(visited), edges, nodes, data)
    elif step == 'v' or step == '^' or step == '<' or step == '>':
        dx = visited[-2][0] - x
        dy = visited[-2][1] - y
        
        if step == 'v' and dx == 0 and dy == 1:
            return
        elif step == '^' and dx == 0 and dy == -1:
            return
        elif step == '>' and dx == 1 and dy == 0:
            return
        elif step == '<' and dx == -1 and dy == 0:
            return

        if (x, y) in nodes:
            b = nodes[(x, y)]
            edges.append(Edge(a, b, len(visited) * 1))
        else:
            b = Node((x, y), step)
            nodes[b.pos] = b
            edges.append(Edge(a, b, len(visited) * 1))
        
            if step == 'v':
                makeGraph(x, y+1, b, [], edges, nodes, data)
            elif step == '^':
                makeGraph(x, y-1, b, [], edges, nodes, data)
            elif step == '>':
                makeGraph(x+1, y, b, [], edges, nodes, data)
            elif step == '<':
                makeGraph(x-1, y, b, [], edges, nodes, data)

def topologicalSort(nodes, edges):
    sorted = []
    edgeList = copy.deepcopy(edges)
    nodeList = list(nodes.values())

    while len(nodeList) > 0:
        for n in nodeList:
            incoming = list(filter(lambda e: e.b == n, edgeList))
            if len(incoming) == 0:
                sorted.append(n)
                nodeList.remove(n)
                edgeList = list(filter(lambda e: e.a != n, edgeList))
                break

    return sorted

def longestPath(sorted, edges):
    dist = {}
    for s in sorted:
        dist[s] = Infinity
    dist[sorted[0]] = 0

    for s in sorted:
        outgoing = list(filter(lambda e: e.a == s, edges))
        for o in outgoing:
            dist[o.b] = max(dist[o.b], dist[s] + o.weight)   

    longest = 0
    for d in dist.values():
        if d > longest:
            longest = d

    return longest - 1

def task(input):
    data = parseInput(input)
    start, end = findStartEnd(data)

    edges = []
    nodes = {start.pos : start}
    makeGraph(start.pos[0], start.pos[1], start, [], edges, nodes, data)

    sorted = topologicalSort(nodes, edges)
    return longestPath(sorted, edges)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    sys.setrecursionlimit(1000000)
    print(test('testInput.txt', 94))
    print(task('input.txt'))
main()

# def dijkstra(nodes, edges, end):
#     visited = []
#     unvisited = list(nodes.values())
#     state = {}

#     for n in unvisited:
#         state[n] = DState()
    
#     state[unvisited[0]].shortest = 0
#     while len(unvisited) > 0:
#         lowest = Infinity
#         current = None

#         for uv in unvisited:
#             s = state[uv]
#             if s.shortest < lowest:
#                 lowest = s.shortest
#                 current = uv
        
#         currentEdges = list(filter(lambda e: e.a == current, edges))
#         for ce in currentEdges:
#             dist = ce.weight + state[current].shortest
#             if dist < state[ce.b].shortest:
#                 state[ce.b].shortest = dist
#                 state[ce.b].previous = current

#         visited.append(current)
#         unvisited.remove(current)

#     toEnd = state[end]
#     return toEnd.shortest - 1
