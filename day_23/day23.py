import re
import time
from heapq import *

class Nanobot:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.rad = r

    def __str__(self):
        return '(<{},{},{}>,r={})'.format(self.x, self.y,self.z, self.rad)

    def __repr__(self):
        return self.__str__()

    def __lt__(self, other):
        return True if self.rad < other.rad else False

    def manhattan(self, other):
        xAbs = abs(self.x-other.x)
        yAbs = abs(self.y-other.y)
        zAbs = abs(self.z-other.z)
        return xAbs + yAbs +zAbs

    def manhattanCoord(self, x, y, z):
        xAbs = abs(self.x-x)
        yAbs = abs(self.y-y)
        zAbs = abs(self.z-z)
        return xAbs + yAbs +zAbs

    def reachable(self, bots):
        count = 0
        for bot in bots.values():
            if self.manhattan(bot) <= self.rad:
                count += 1
        return count

    def canReach(self, x, y, z):
        return self.manhattanCoord(x,y,z) <= self.rad

    def getCorners(self):
        corners = []
        corners.append((self.x - self.rad, self.y, self.z))
        corners.append((self.x + self.rad, self.y, self.z))

        corners.append((self.x, self.y - self.rad, self.z))
        corners.append((self.x, self.y + self.rad, self.z))

        corners.append((self.x, self.y, self.z - self.rad))
        corners.append((self.x, self.y, self.z + self.rad))

        return corners


class Cube:
    def __init__(self, x1,y1,z1,x2,y2,z2, bots):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.z1 = z1
        self.z2 = z2
        self.size = x2 - x1 + 1
        self.children = None
        self.overlaps = self.countOverlaps(bots)

    def getCorners(self):
        corners = []

        for x in (self.x1, self.x2):
            for y in (self.y1, self.y2):
                for z in (self.z1, self.z2):
                    corners.append((x,y,z))
        return corners

    def canReach(self, x,y,z):
        if x <= self.x2 and x >= self.x1 and y <= self.y2 and y >= self.y1 and z <= self.z2 and z >= self.z1:
            return True
        
        return False

    def overlapsBot(self, bot):
        if self.x1 > bot.x + bot.rad or self.y1 > bot.y + bot.rad or self.z1 > bot.z + bot.rad:
            return False
        
        elif self.x2 < bot.x - bot.rad or self.y2 < bot.y -bot.rad or self.z2 < bot.z - bot.rad:
            return False

        for x,y,z in self.getCorners():
            if bot.canReach(x,y,z):
                return True

        for x,y,z in bot.getCorners():
            if self.canReach(x,y,z):
                return True
        
        return False

    def countOverlaps(self, bots):
        count = 0
        for b in bots:
            if self.overlapsBot(b):
                count += 1
        return count

    def getChildren(self, bots):
        if self.children is None:
            self.children = []
            newSize = self.size // 2
            midX = newSize + self.x1 - 1
            midY = newSize + self.y1 - 1
            midZ = newSize + self.z1 - 1

            self.children.append(Cube(self.x1, self.y1, self.z1, midX, midY, midZ, bots))
            self.children.append(Cube(midX +1, midY +1, midZ +1, self.x2, self.y2, self.z2, bots))

            self.children.append(Cube(midX +1, self.y1, self.z1, self.x2, midY, midZ, bots))
            self.children.append(Cube(self.x1, midY +1, self.z1, midX, self.y2, midZ, bots))
            self.children.append(Cube(self.x1, self.y1, midZ +1, midX, midY, self.z2, bots))

            self.children.append(Cube(midX +1, midY +1, self.z1, self.x2, self.y2, midZ, bots))
            self.children.append(Cube(midX +1, self.y1, midZ +1, self.x2, midY, self.z2, bots))
            self.children.append(Cube(self.x1, midY +1, midZ +1, midX, self.y2, self.z2, bots))

            self.children = [c for c in self.children if c.size > 0]

        return self.children


    def __lt__(self, other):
        if self.overlaps > other.overlaps:
            return True
        elif self.overlaps == other.overlaps and self.size < other.size:
            return True
        else:
            return False

    def __repr__(self):
        return '<{} {} {} {} {}>'.format(self.x1, self.y1, self.z1, self.size, self.overlaps)


def manhattan(x1, y1, z1, x2, y2, z2):
    xAbs = abs(x1 - x2)
    yAbs = abs(y1 - y2)
    zAbs = abs(z1 - z2)

    return xAbs + yAbs + zAbs

def parseInput(filename):
    bots = {}
    regex = re.compile('-?\\d+')
    with open(filename, 'r') as data:
        for line in data:
            nums = regex.findall(line)
            x = int(nums[0])
            y = int(nums[1])
            z = int(nums[2])
            r = int(nums[3])
            bots[(x,y,z)] = (Nanobot(x,y,z,r))
    return bots

def findStrongest(bots):
    return max(bots.values())

def rangeOfStrongest(filename):
    bots = parseInput(filename)
    strongest = findStrongest(bots)
    return strongest.reachable(bots)

def findDistance(filename):
    bots = parseInput(filename).values()
    
    minX, minY, minZ, maxX, maxY, maxZ = 0,0,0,0,0,0

    for b in bots:
        if b.x < minX: minX = b.x
        if b.x > maxX: maxX = b.x
        
        if b.y < minY: minY = b.y
        if b.y > maxY: maxY = b.y

        if b.z < minZ: minZ = b.z
        if b.z > maxZ: maxZ = b.z

    minCoverage = max((abs(minX - maxX), abs(minY - maxY), abs(minZ - maxZ)))

    size = 1
    while size < minCoverage:
        size *= 2

        
    minOverlap = 0
    minDist = 10000000000

    containerCube = Cube(minX-1, minY-1, minZ-1, minX - 1 + size, minY - 1 + size, minZ - 1 + size, bots)

    heap = []

    heapify(heap)

    heappush(heap, containerCube)

    while len(heap) > 0 and minOverlap <= max([c.overlaps for c in heap]):
        c = heappop(heap)

        if c.size == 1:
            
            overlaps = c.overlaps
            dist = manhattan(c.x1, c.y1, c.z1, 0,0,0) 
            if overlaps >= minOverlap and minDist > dist:
                print("Found Overlap", c)
                print("DIST", dist)
                minOverlap = overlaps
                minDist = dist
        elif c.size > 1:
            children = c.getChildren(bots)
            for child in children:
                heappush(heap, child)


    return minDist


def main():
    assert rangeOfStrongest('test_input') == 7
    print('Part A: {}'.format(rangeOfStrongest('input')))
    print('Part B: {}'.format(findDistance('test2')))
    print('Part B: {}'.format(findDistance('input')))

    

if __name__ == "__main__":
    main()