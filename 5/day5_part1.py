import os

class Mapping:
    def __init__(self, ds, ss, rl):
        self.ds = ds
        self.ss = ss
        self.rl = rl

    def convert(self, val):
        return val + (self.ds - self.ss)
    
    def isInRange(self, val):
        return val >= self.ss and val < self.ss + self.rl


def processSeed(seed, maps):
    val = seed
    for map in maps:
        for mapping in map:
            if mapping.isInRange(val):
                val = mapping.convert(val)
                break

    return val

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    seeds = list()
    maps = list()
    i = -1

    for l in lines:
        if 'seeds' in l:
            seeds = [int(s) for s in lines[0].split(':')[1].strip().split(' ') if s]
        elif 'map' in l:
            i += 1
            maps.append(list())
        elif l != '\n':
            items = [int(s) for s in l.strip().split(' ') if s]
            maps[i].append(Mapping(items[0], items[1], items[2]))

    lowest = 99999999999
    for s in seeds:
        val = processSeed(s, maps)
        if val < lowest:
            lowest = val
        
    return lowest

def main(input):
    print(parseInput(input))

    return 0

main("testInput.txt")