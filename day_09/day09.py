#for this one, I treated each marble as a node in a circularly linked list
#probably could have used a deque for this, but I wanted to write my own for practice

class Marble:
    def __init__(self, value):
        self.value = value
        self.next = self
        self.prev = self

    def addNext(self, other):
        #add a node next to this one, with correct linkages
        other.next = self.next
        other.prev = self
        self.next.prev = other
        self.next = other
        return other

    def getNthClock(self, n):
        #get the nth to the right
        #if n is negative, get the abs(n) to the left
        if n == 0:
            return self
        elif n > 0:
            return self.next.getNthClock(n-1)
        else:
            return self.prev.getNthClock(n+1)

    def popPrev(self):
        #get the value of the previous node, then remove it and repair linkages
        val = self.prev.value
        self.prev.prev.next = self
        self.prev = self.prev.prev
        return val

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)

    def print(self):
        print('{},{},{},{},{}'.format(self.prev.prev, self.prev, self, self.next, self.next.next))

def game(playcount, last):
    players = [0 for i in range(playcount)]
    currentPlayer = 0
    currentMarble = Marble(0)
    for marbleVal in range(1, last+1):
        if marbleVal % 23 == 0: #special behavior
            #we'll get the one 6 to the left, and pop it's left neighbor
            currentMarble = currentMarble.getNthClock(-6)
            players[currentPlayer] += marbleVal + currentMarble.popPrev()
        else:
            currentMarble = currentMarble.getNthClock(1)
            currentMarble = currentMarble.addNext(Marble(marbleVal))
        currentPlayer = marbleVal % len(players)

    return max(players)

def main():
    with open('input') as file:
        players = 9
        last = 25
        for line in file:
            parse1 = line.split(' players; last marble is worth ')
            players = int(parse1[0])
            parse2 = parse1[1].split()
            last = int(parse2[0])

        highscoreA = game(players, last)
        print('High Score A: {}'.format(highscoreA))
        highscoreB = game(players, last*100)
        print('High Score B: {}'.format(highscoreB))


if __name__ == '__main__':
    main()
