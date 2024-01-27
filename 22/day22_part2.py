import copy
import os
import numpy as np
import matplotlib.pyplot as plt

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
    label = 1
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

def getBlocks(volume):
    dims = np.shape(volume)
    blocks = []

    for z in range(dims[2]):
        for y in range(dims[1]):
            for x in range(dims[0]):
                voxel = volume[x, y, z]
                if voxel != 0 and not voxel in blocks:
                    blocks.append(voxel)
    return blocks

def actualDestroy(start, volume):
    v = copy.deepcopy(volume)
    dims = np.shape(v)

    destroyed = {}
    for z in range(dims[2]):
        supported = {}
        for y in range(dims[1]):
            for x in range(dims[0]):
                voxel = v[x, y, z]
                if voxel != 0.0 and z > 0.0:
                    if not voxel in supported:
                        supported[voxel] = False
                        
                    below = v[x, y, z-1]
                    if below > 0.0:
                        supported[voxel] = True

        for i in range(dims[1]):
            for j in range(dims[0]):
                voxel = v[j, i, z]
                if voxel == start:
                    v[j, i, z] = 0.0
                elif voxel in supported and not supported[voxel]:
                    destroyed[voxel] = True
                    v[j, i, z] = 0.0

    return len(destroyed)

def sumFall(volume):
    blocks = getBlocks(volume)

    sum = 0
    for b in blocks:
        sum += actualDestroy(b, volume)

    return sum

def task(input):
    volume = parseInput(input)
    volume = drop(volume)
    # showVolume(volume)

    return sumFall(volume)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput.txt', 7))
    print(task('input.txt'))
main()



