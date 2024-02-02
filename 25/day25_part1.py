import os
import networkx as nx
import networkx.algorithms.connectivity as nxa
import matplotlib.pyplot as plt

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    g = nx.Graph()
    for l in lines:
        parts = l.strip().split(':')
        connected = parts[1].strip().split(' ')
        for c in connected:
            g.add_edge(parts[0], c)
    return g

def drawGraph(g):
    nx.draw(g, with_labels=True)
    plt.show()

def solve(g):
    cut = nxa.stoer_wagner(g)
    return len(cut[1][0]) * len(cut[1][1])

def task(input):
    g = parseInput(input)
    return solve(g)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput.txt', 54))
    print(task('input.txt'))
main()