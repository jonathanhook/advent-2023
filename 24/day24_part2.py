import os
import sympy

class Ray:
    def __init__(self, x, y, z, vx, vy, vz):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

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
        data.append(Ray(coords[0], coords[1], coords[2], vecs[0], vecs[1], vecs[2]))
    
    return data

def solver(data):
    xr, yr, zr, vxr, vyr, vzr = sympy.symbols('xr, yr, zr, vxr, vyr, vzr')
    eqs = []
    for s in data:
        eqs.append((xr - s.x) * (s.vy - vyr) - (yr - s.y) * (s.vx - vxr))
        eqs.append((yr - s.y) * (s.vz - vzr) - (zr - s.z) * (s.vy - vyr))
    
    result = sympy.solve(eqs)
    return result[0][xr] + result[0][yr] + result[0][zr]

def task(input):
    data = parseInput(input)
    return solver(data)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput.txt', 47))
    print(task('input.txt'))
main()