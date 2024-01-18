import os

class Step():
    def __init__(self, x, y, count):
        self.x = x
        self.y = y
        self.count = count

    def hash(self):
        return str(self.count) + ':' + str(self.x) + ':' + str(self.y)

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        data.append([c for c in l.strip()])
    return data

def findStart(data):
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j] == 'S':
                return (j, i)

def findplots(data, steps):
    startPos = findStart(data)
    width = len(data[0])
    height = len(data)
    queue = [Step(startPos[0], startPos[1], 0)]
    explored = {}
    
    found = 0
    while len(queue) > 0:
        step = queue.pop(0)
        nCount = step.count + 1

        if nCount == (steps + 1):
            found += 1
        else:
            for next in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx = step.x + next[0]
                ny = step.y + next[1]
                nextStep = Step(nx, ny, nCount)

                if not nextStep.hash() in explored and nx >= 0 and nx < width and ny >= 0 and ny < height and data[ny][nx] != '#':
                    queue.append(nextStep)
                    explored[nextStep.hash()] = True
    return found
    
def task(input, steps):
    data = parseInput(input)
    return findplots(data, steps)

def test(input, steps, expected):
    result = task(input, steps)
    return result == expected

def main(): 
    print(test('testInput.txt', 6, 16))
    print(task('input.txt', 64))
main()



