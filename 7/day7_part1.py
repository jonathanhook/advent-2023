import os

class Hand:
    def __init__(self, str):
        parts = str.strip().split()
        self.bid = int(parts[1])

        self.asStr = parts[0]
        self.cards = list()
        for c in parts[0]:
            if c == 'A': self.cards.append(14)
            elif c == 'K': self.cards.append(13)
            elif c == 'Q': self.cards.append(12)
            elif c == 'J': self.cards.append(11)
            elif c == 'T': self.cards.append(10)
            else: self.cards.append(int(c))

        self.typeId = self.getTypeId()

    def isOfAKind(self, val):
        for i in range(2, 15):
            if self.cards.count(i) == val:
                return True
        return False
    
    def isFullHouse(self):
        return self.isOfAKind(3) and self.isOfAKind(2)
    
    def isTwoPair(self):
        pairCount = 0
        for i in range(2, 15):
            if self.cards.count(i) == 2:
                pairCount += 1
        return pairCount == 2
    
    def getHighestCard(self):
        return max(self.cards)
    
    def getTypeId(self):
        if self.isOfAKind(5): return 6
        elif self.isOfAKind(4): return 5
        elif self.isFullHouse(): return 4
        elif self.isOfAKind(3): return 3
        elif self.isTwoPair(): return 2
        elif self.isOfAKind(2): return 1
        else: return 0
    
    def secondary(self, other):
        for i in range(0, len(self.cards)):
            if self.cards[i] != other.cards[i]:
                return self.cards[i] > other.cards[i]
        return False

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        if self.typeId == other.typeId:
            return self.secondary(other)
        else:
            return self.typeId > other.typeId

def parseInput(input):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_directory, input)
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    hands = list()
    for l in lines:
        hands.append(Hand(l))

    return hands

def main(input):
    data = parseInput(input)
    data.sort()

    winnings = 0
    score = len(data)
    for d in data:
        winnings += (score * d.bid)
        score -= 1

    print(winnings)

main('input.txt')