import os

class Hand:
    def __init__(self, str):
        parts = str.strip().split()
        self.bid = int(parts[1])

        self.asStr = parts[0]
        self.cards = list()
        for c in parts[0]:
            if c == 'A': self.cards.append(13)
            elif c == 'K': self.cards.append(12)
            elif c == 'Q': self.cards.append(11)
            elif c == 'T': self.cards.append(10)
            elif c == 'J': self.cards.append(1)
            else: self.cards.append(int(c))

        self.typeId = self.getTypeId()

    def isOfAKind(self, val):
        for i in range(1, 14): #bug?
            withJoker = [i if item == 1 else item for item in self.cards]
            if withJoker.count(i) == val:
                return True
        return False
    
    def isFullHouse(self):
        for i in range(1, 14):
            withThisJoker = [i if item == 1 else item for item in self.cards]
            hasPair = False
            hasThree = False
            for j in range(1, 14):
                if withThisJoker.count(j) == 2: hasPair = True
                elif withThisJoker.count(j) == 3: hasThree = True

                if hasPair and hasThree:
                    return True
        return False

    def isTwoPair(self):
        for i in range(1, 14):
            pairCount = 0
            withThisJoker = [i if item == 1 else item for item in self.cards]
            for j in range(1, 14):
                if withThisJoker.count(j) == 2:
                    pairCount += 1
                if pairCount == 2:
                    return True
        
        return False
    
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