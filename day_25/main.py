
import re

class Star:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.z = coords[2]
        self.t = coords[3]
        self.neighbors = set()

    def __repr__(self):
        return '<{} {} {} {}>'.format(self.x, self.y, self.z, self.t)

    def manhattan(self, otherStar):
        xAbs = abs(self.x - otherStar.x)
        yAbs = abs(self.y - otherStar.y)
        zAbs = abs(self.z - otherStar.z)
        tAbs = abs(self.t - otherStar.t)
        dist = sum((xAbs, yAbs, zAbs, tAbs))
        return dist

    def isNeighbor(self, otherStar):
        return True if self.manhattan(otherStar) <= 3 else False

class Constellation:
    def __init__(self):
        self.stars = set()

    def __repr__(self):
        return str(self.stars)

    def addStar(self, star):
        self.stars.add(star)

    def combine(self, other):
        for s in other.stars:
            self.stars.add(s)

    def isNeighborCon(self, otherCon):
        for j in otherCon.stars:
            if self.isNeighborStar(j):
                return True
        return False

    def isNeighborStar(self, otherStar):
        for i in self.stars:
            if i.isNeighbor(otherStar):
                return True
        return False

    def isdisjoint(self, other):
        return self.stars.isdisjoint(other.stars)

def getStarsFromFile(filename):
    regex = re.compile('-?\\d+')
    stars = set()
    with open(filename) as data:
        for line in data:
            res = regex.findall(line)
            coords = [int(i) for i in res]
            newStar = Star(coords)
            stars.add(newStar)

    return stars

def countConstellations(filename):
    stars = getStarsFromFile(filename)
    constellations = []
    starList = list(stars)
    for i in range(len(starList)):
        for j in range(i+1,len(starList)):
            if starList[i].isNeighbor(starList[j]):
                starList[i].neighbors.add(starList[j])
                starList[j].neighbors.add(starList[i])
    
    while len(stars) > 0:
        s = stars.pop()
        queue = []
        queue.append(s)
        con = set()
        con.add(s)
        while len(queue) > 0:
            cur = queue.pop(0)
            con.add(cur)
            queue += [n for n in cur.neighbors if n not in con]
        constellations.append(con)
        stars -= con
    

    return len(constellations)


def tests():
    assert countConstellations('sample1') == 2
    assert countConstellations('sample2') == 4
    assert countConstellations('sample3') == 3
    assert countConstellations('sample4') == 8
    print('All tests passed')

    

def main():
    tests()
    print('Part A: {}'.format(countConstellations('input')))

if __name__ == '__main__':
    main()