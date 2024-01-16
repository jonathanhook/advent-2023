import os

debug = False

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

    return Button('button', [modules['broadcaster']])

def processModules(modules):
    low = high = 0
    
    for i in range(1000):
        tasks = []
        tasks.extend(modules.execute(False, None))
        while len(tasks) > 0:
            t = tasks.pop(0)
            if t.pulse:
                high += 1
            else:
                low += 1

            newTasks = t.module.execute(t.pulse, t.sender)
            if not newTasks is None:
                tasks.extend(newTasks)

    return low * high

def task(input):
    modules = parseInput(input)
    return processModules(modules)

def test(input, expected):
    result = task(input)
    return result == expected

def main(): 
    print(test('testInput1.txt', 32000000))
    print(test('testInput2.txt', 11687500))
    print(task('input.txt'))
main()

