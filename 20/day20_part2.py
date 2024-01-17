import math
import os

debug = False
last = {}
cycles = {}

class Task:
    def __init__(self, module, pulse, sender):
        self.module = module
        self.pulse = pulse
        self.sender = sender

class Module:
    def __init__(self, name, destinations=None):
        self.name = name
        self.destinations = destinations

    def execute(self, pulse, sender):
        if debug and not sender is None:
            pulseVal = 'low'
            if pulse:
                pulseVal = 'high'
            print(sender.name + ' -' + pulseVal + '-> ' + self.name)
        
class Button(Module):
    def execute(self, pulse, sender):
        super().execute(pulse, sender)
        tasks = []
        for d in self.destinations:
            tasks.append(Task(d, False, self)) 
        return tasks
    
class Broadcaster(Module):
    def execute(self, pulse, sender):
        super().execute(pulse, sender)
        tasks = []
        for d in self.destinations:
            tasks.append(Task(d, pulse, self)) 
        return tasks

class FlipFlop(Module):
    def __init__(self, name, destinations=None, state=False):
        self.state = state
        super().__init__(name, destinations)

    def execute(self, pulse, sender):
        super().execute(pulse, sender)
        tasks = []
        if not pulse:
            self.state = not self.state
            for d in self.destinations:
                tasks.append(Task(d, self.state, self))
        return tasks

class Conjunction(Module):
    def __init__(self, name, destinations=None):
        self.memory = {}
        super().__init__(name, destinations)
    
    def execute(self, pulse, sender):
        super().execute(pulse, sender)
        self.memory[sender.name] = pulse
        tasks = []

        allHigh = True
        for m in self.memory.values():
            allHigh &= m

        for d in self.destinations:
            tasks.append(Task(d, not allHigh, self))        
        return tasks

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modules = {}
    for l in lines:
        name = l.strip().split(' ->')[0]
        module = None
        if name[0] == '%':
            name = name[1:]
            module = FlipFlop(name)
        elif name[0] == '&':
            name = name[1:]
            module = Conjunction(name)
        else:
            module = Broadcaster(name)
        modules[name] = module

    for l in lines:
        split = l.strip().split(' -> ')
        name = split[0]
        if name[0] == '%' or name[0] == '&':
            name = name[1:]
        
        dests = split[1].strip().split(',')
        dList = []
        for d in dests:
            ds = d.strip()
            if not ds in modules:
                modules[ds] = Module(ds)
            dList.append(modules[ds])   
        modules[name].destinations = dList
                      
        for d in modules[name].destinations:
            if type(d) is Conjunction:
                d.memory[name] = False

    return Button('button', [modules['broadcaster']]), modules

def processModules(modules, list):        
    conCount = 0
    for l in list.values():
        if type(l) is Conjunction:
            conCount += 1
   
    for i in range(999999999):
        tasks = []
        tasks.extend(modules.execute(False, None))
        while len(tasks) > 0:
            t = tasks.pop(0)

            if (not t.sender is None) and (type(t.sender) == Conjunction) and (t.pulse == False):
                if t.sender.name in last:
                    diff = (i - last[t.sender.name])
                    if diff > 0:
                        cycles[t.sender.name] = diff
                last[t.sender.name] = i

            if len(cycles) == (conCount - 1):
                return math.lcm(*[cc for cc in cycles.values()]) 

            newTasks = t.module.execute(t.pulse, t.sender)
            if not newTasks is None:
                tasks.extend(newTasks)
    return -1

def task(input):
    modules, list = parseInput(input)
    return processModules(modules, list)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(task('input.txt'))
main()

