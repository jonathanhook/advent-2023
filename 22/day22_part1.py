import os
import numpy as np
import matplotlib.pyplot as plt

class Block:
    def __init__(self, id):
        self.id = id
        self.above = []
        self.below = []

    def addAbove(self, a):
        if not a in self.above:
            self.above.append(a)

    def addBelow(self, b):
        if not b in self.below:
            self.below.append(b)

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    coords = []
    for l in lines:
        split = l.strip().split('~')
        a = [int(c) for c in split[0].split(',')]
        b = [int(c) for c in split[1].split(',')]
        coords.append([(a[0], b[0]), (a[1], b[1]), (a[2], b[2])])

    mX = mY = mZ = 0
    for c in coords:
        if c[0][1] > mX: 
            mX = c[0][1]
        if c[1][1] > mY: 
            mY = c[1][1]
        if c[2][1] > mZ: 
            mZ = c[2][1]

    volume = np.zeros((mX+1, mY+1, mZ+1))
    label = 0
    for c in coords:
        for x in range(c[0][0], c[0][1]+1):
            for y in range(c[1][0], c[1][1]+1):
                for z in range(c[2][0], c[2][1]+1):
                    volume[x, y, z] = label
        label += 1

    return volume

def showVolume(volume):
    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(volume, facecolors='red')
    plt.show()

def drop(volume):
    dims = np.shape(volume)

    somethingMoved = True
    while somethingMoved:
        somethingMoved = False
        for z in range(1, dims[2]):
            supported = {}
            for y in range(dims[1]):
                for x in range(dims[0]):
                    voxel = volume[x, y, z]
                    if voxel != 0.0:
                        if not voxel in supported:
                            supported[voxel] = False
                        
                        below = volume[x, y, z-1]
                        if below != 0:
                            supported[voxel] = True

            for i in range(dims[1]):
                for j in range(dims[0]):
                    voxel = volume[j, i, z]
                    if voxel in supported and not supported[voxel]:
                        volume[j, i, z-1] = voxel
                        volume[j, i, z] = 0.0
                        somethingMoved = True
    return volume

def checkDisintegrate(volume):
    dims = np.shape(volume)
    blocks = {}

    for z in range(dims[2]):
        for y in range(dims[1]):
            for x in range(dims[0]):
                voxel = volume[x, y, z]
                if voxel != 0:
                    if not voxel in blocks:
                        blocks[voxel] = Block(voxel)

                    if z < dims[2] - 1:
                        above = volume[x, y, z+1]
                        if above != 0 and above != voxel:
                            blocks[voxel].addAbove(above)
                    if z > 0:
                        below = volume[x, y, z-1]
                        if below != 0 and below != voxel:
                            blocks[voxel].addBelow(below)

    count = 0
    for b in blocks:
        essential = False
        for a in blocks[b].above:
            if len(blocks[a].below) == 1:
                essential = True
        if not essential:
            count += 1

    return count

def task(input):
    volume = parseInput(input)
    volume = drop(volume)
    # showVolume(volume)

    return checkDisintegrate(volume)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput.txt', 5))
    print(task('input.txt'))
main()



