import os

class Ray:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.m = vy / vx
        self.b = py - self.m * px

    def intersection(self, other):
        md = other.m - self.m
        if md == 0:
            return None

        x = (self.b - other.b) / (other.m - self.m)
        y = (self.m * x) + self.b
        return (x, y)

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    data = []
    for l in lines:
        parts = l.strip().split('@')
        coords = [int(c.strip()) for c in parts[0].strip().split(',')]
        vecs = [int(c.strip()) for c in parts[1].strip().split(',')]
        data.append(Ray(coords[0], coords[1], vecs[0], vecs[1]))
    
    return data

def inFuture(i, ray):
    xs = (i[0] - ray.px) * ray.vx > 0
    ys = (i[1] - ray.py) * ray.vy > 0
    return xs and ys

def intersectinInRange(a, b, b0, b1):
    i = a.intersection(b)
    return (i != None) and inFuture(i, a) and inFuture(i, b) and (i[0] >= b0 and i[0] <= b1) and (i[1] >= b0 and i[1] <= b1)

def countValidIntersects(data, b0, b1):
    count = 0
    i = 0
    for i in range(len(data)):
        a = data[i]
        for j in range(i, len(data)):
            b = data[j]
            if a != b and intersectinInRange(a, b, b0, b1):
                count += 1
    return count

def task(input, b0, b1):
    data = parseInput(input)
    return countValidIntersects(data, b0, b1)

def test(input, b0, b1, expected):
    result = task(input, b0, b1)
    return result == expected

def main(): 
    print(test('testInput.txt', 7, 27, 2))
    print(task('input.txt', 200000000000000, 400000000000000))
main()
