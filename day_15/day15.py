from time import sleep
from os import system

class FloorMap:
    '''
    FloorMap class - holds data for what combatants are where
    Also does most of the heavy lifting
    '''
    def __init__(self, spacesArr, units):
        #the units and map array are parse elsewhere
        self.spaces = spacesArr
        self.units = units

    def __str__(self):
        #print the walls and units
        strRep = '\n'.join(
            [''.join(
                [(lambda x: '  ' if x is None else str(x))(x) for x in line]) 
                for line in self.spaces])

        return strRep


    def sortUnits(self):
        #order units from top to bottom, left to right
        self.units.sort(key=(lambda unit: (unit.y, unit.x)))

    def isEmpty(self, x, y):
        #check if a space is clear to walk through
        return True if self.spaces[y][x] is None else False

    def hasUnitsOfType(self, unitType):
        #check if there are any living units of unitType left
        hasType = False
        for unit in self.units:
            if isinstance(unit, unitType) and not unit.dead:
                #only count units if they're alive
                hasType = True
                break
        return hasType

    def getAdjacentSpaces(self, currentx, currenty, unitType):
        #get a set of all open spaces that are adjacent to an enemy of type unitType

        adjacent = set()

        #get living enemy units of the type we're looking for
        unitArr = [unit for unit in self.units if isinstance(unit, unitType) and not unit.dead]

        for unit in unitArr:
            x = unit.x
            y = unit.y
            
            #add to the set all adjacent (not diagonal) spaces that are empty or are where the current position is
            for spaces in [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2) if (dx == 0 or dy == 0)]:

                if self.isEmpty(spaces[0], spaces[1]) or (spaces[0], spaces[1]) == (currentx, currenty):
                    adjacent.add(spaces)

        return adjacent

    def possibleDestinations(self, startx, starty):
        #get a dictionary of all possible places that one can move from the start position 
        #without traversing a wall or other unit
        #this will also inclue the current space (assuming you don't move)

        #start with the current space and work outwards
        possible = {(startx, starty): 0}
        queue = [(startx, starty)]


        while len(queue) > 0:
            #traverse over breadth first 
            (posx, posy) = queue.pop(0)
            for (x, y) in [(posx+dx, posy+dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx == 0 or dy == 0]:

                if self.isEmpty(x, y) and (x, y) not in possible:
                    possible[(x, y)] = possible[(posx, posy)] + 1
                    queue.append((x, y))

        return possible

    def reachableAdjacent(self, startx, starty, unitType):
        #take the intersection of reachable spaces and places adjacent to an enemy
        #returns a dict of reachable adjacent places mapped to distances

        adj = self.getAdjacentSpaces(startx, starty, unitType)
        possible = self.possibleDestinations(startx, starty)

        result = {}
        for i in adj:
            if i in possible:
                result[i] = possible[i]

        return result

    def findClosestDest(self, startx, starty, targetType):
        #determine the closest destination that we can move to
        #favors reading order on ties (top to bottom, left to right)

        destinations = self.reachableAdjacent(startx, starty, targetType)

        #stay where we are if we can't attack elsewhere
        target = (startx, starty)

        if len(destinations) > 0:
            #if we can move, go to the closest one, favoring "reading" order
            minDist = min(destinations.values())
            closest = [i for i in destinations if destinations[i] == minDist]
            closest.sort(key=lambda tup: (tup[1], tup[0]))
            target = closest[0]

        return target

    def findPath(self, x1, y1, x2, y2):
        #determine the path to take from the start to the end coordinates
        #favors reading order (top to bottom, left to right)

        newPos = (x1, y1) #we only need a new destination if we're actually moving

        if x1 != x2 or y1 != y2:
            #we're confirmed to be moving elsewhere

            #we can only move one space per turn, and only orthagonally
            moves = [(x1+dx, y1+dy) for dx in range(-1,2) for dy in range(-1,2) if (dx == 0 or dy == 0) and self.isEmpty(x1+dx, y1+dy)]

            #get a dict of open tiles and distances from the *target* position
            allDistFromTarget = self.possibleDestinations(x2, y2)

            #take the intersection of the possible moves and the distances to the target position
            movesDistFromTarget = {}
            for i in moves:
                if i in allDistFromTarget:
                    movesDistFromTarget[i] = allDistFromTarget[i]

            #determine the closest space that we can move to, relative to the target position
            minDist = min(movesDistFromTarget.values())
            closest = [
                i for i in movesDistFromTarget if movesDistFromTarget[i] == minDist
            ]
            closest.sort(key=lambda tup: (tup[1], tup[0]))


            newPos = closest[0]
        
        return newPos

    def pathFindToTargetType(self, x, y, targetType):
        #get a path to the nearest target from the current x y position
        # returns the next place to move to as an (x,y) tuple

        #check if we're adjacent to a viable target first
        hasTarget = False
        for nearby in [(x + dx, y + dy) for dx in range(-1, 2) for dy in range(-1, 2) if dx == 0 or dy == 0]:

            if isinstance(self.spaces[nearby[1]][nearby[0]], targetType):
                hasTarget = True
                break

        #only move if we don't have an adjacent target
        if not hasTarget:
            (destx, desty) = self.findClosestDest(x, y, targetType)
            nextMove = self.findPath(x, y, destx, desty)
        else:
            nextMove = (x, y)

        return nextMove

    def attack(self, x, y, attack, targetType):
        #attack a nearby target from the current position, if possible

        #get a list of all viable targets        
        targets = {}
        for nearby in [(x + dx, y + dy) for dx in range(-1, 2)
                       for dy in range(-1, 2) if dx == 0 or dy == 0]:
            if isinstance(self.spaces[nearby[1]][nearby[0]], targetType):
                targets[(nearby[0],nearby[1])] = self.spaces[nearby[1]][nearby[0]].hp
        
        
        targetCoord = None
        if len(targets) == 1:
            targetCoord = list(targets)[0]
            
        elif len(targets) > 1:
            #favor targeting lower health, then by reading order
            minHealth = min(targets.values())
            lowest = [i for i in targets if targets[i] == minHealth]
            lowest.sort(key=lambda tup: (tup[1], tup[0]))
            targetCoord = lowest[0]


        if targetCoord is not None:
            #finally attack
            target = self.spaces[targetCoord[1]][targetCoord[0]]
            target.hp -= attack
            if target.hp <= 0:
                #don't remove dead targets from the unit list yet
                #but we should remove from the map, and mark them for clearance at next loop iteration
                self.spaces[targetCoord[1]][targetCoord[0]] = None
                target.dead = True

    def getCombatResult(self, completedRounds):
        #return the "combat result"
        totalHP = sum([x.hp for x in self.units])
        return completedRounds * totalHP



class EnvObject:
    '''
    a generic item in the environment map
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '# '


class Unit(EnvObject):
    '''
    an object in the environment that can move and attack
    '''

    def __init__(self, x, y, rep):
        EnvObject.__init__(self, x, y)
        self.targetType = Unit
        self.strRep = rep
        self.hp = 200
        self.dead = False
        self.attackPower = 3

    def move(self, floorMap):
        #move 1 space orthagonally toward the nearest unit with an enemy type

        moved = False
        dest = floorMap.pathFindToTargetType(self.x, self.y, self.targetType)
        newx,newy = dest[0],dest[1]
        floorMap.spaces[self.y][self.x] = None
        floorMap.spaces[newy][newx] = self

        if self.x != newx or self.y != newy:
            moved =True

        self.x = newx
        self.y = newy

        return moved

    def attack(self, floorMap):
        #attack if possible

        floorMap.attack(self.x, self.y, self.attackPower, self.targetType)

    def turn(self, floorMap):
        #take a 2-part (move, attac) turn, if not dead


        if not self.dead:
            #if there are more enemy combatants, keep attacking, and return that combat continues
            continues = floorMap.hasUnitsOfType(self.targetType)
            if continues:
                self.move(floorMap)
                self.attack(floorMap)
            return continues
        else: 
            #combat should continue if this unit is dead - others may be alive
            return True
        

    def __str__(self):
        return self.strRep

    def __repr__(self):
      return self.strRep


class Goblin(Unit):
    '''
    Goblins - the natural enemy of Elves
    '''

    def __init__(self, x, y):
        Unit.__init__(self, x, y, 'G ')
        self.targetType = Elf


class Elf(Unit):
    '''
    Elves - the natural enemy of Goblins
    '''
    def __init__(self, x, y):
        Unit.__init__(self, x, y, 'E ')
        self.targetType = Goblin


def parseInput(filename):
    #Construct and return a FloorMap based on the input filename

    floorMapArr = []
    units = []

    with open(filename) as file:
        y = 0
        for line in file:
            x = 0
            noSpaces = line.strip()
            floorRow = []
            for char in noSpaces:
                objAtLocation = None
                if char == '#':
                    objAtLocation = EnvObject(x, y)
                elif char == 'G':
                    objAtLocation = Goblin(x, y)
                    units.append(objAtLocation)
                elif char == 'E':
                    objAtLocation = Elf(x, y)
                    units.append(objAtLocation)
                floorRow.append(objAtLocation)
                x += 1
            floorMapArr.append(floorRow)
            y += 1

    floorMap = FloorMap(floorMapArr, units)
    return floorMap


def run(filename, silent=False):
    #Run the combat simulation based on the input filename for part A

    floorMap = parseInput(filename)
    combatContinues = True
    rounds = 0

    unitMoved = True
    unitDied = True

    while combatContinues:
        
        #run until only one side remains

        if not silent and (unitMoved or unitDied):
            
            strRep = str(floorMap)
            system('clear')  
            print('{}\n{}'.format(rounds, strRep))
            sleep(1)
        unitMoved = False
        unitDied = False


        floorMap.sortUnits() #units act in "read" order
        
        for unit in floorMap.units:

            #if the unit doesn't see any enemies, combat is over
            if not unit.dead:
                #if there are more enemy combatants, keep attacking, and return that combat continues

                combatContinues = floorMap.hasUnitsOfType(unit.targetType)
                if combatContinues:
                    moved = unit.move(floorMap)
                    unit.attack(floorMap)

                if moved: 
                    unitMoved = True
            if not combatContinues:
                break

        #clear dead enemies
        oldNumUnits = len(floorMap.units)
        floorMap.units = [unit for unit in floorMap.units if unit.dead == False]
        if len(floorMap.units) < oldNumUnits:
            unitDied = True

        rounds += 1



    if not silent:
        strRep = str(floorMap)
        system('clear')  
        print('{}\n{}'.format(rounds, strRep))
        for unit in floorMap.units:
            print('{}:{}'.format(unit,unit.hp))

        sleep(3)

    

    return(floorMap.getCombatResult(rounds - 1))

    
def runB(filename, silent=False):
    #Incrementally increase the power of the Elves until they win,
    #then return the result
    
    elvesLose = True
    elfPower = 3
    
    while elvesLose:
        #reset the results after every loss, except increment the power
        floorMap = parseInput(filename)
        elfCount = 0
        for elf in [unit for unit in floorMap.units if isinstance(unit, Elf)]:
            elfCount += 1
            elf.attackPower = elfPower


        combatContinues = True
        rounds = 0
        while combatContinues:
              
            floorMap.sortUnits()
            for unit in floorMap.units:
                combatContinues = unit.turn(floorMap)
                if not combatContinues:
                    break

            floorMap.units = [unit for unit in floorMap.units if unit.dead == False]

            count = 0
            for elf in [unit for unit in floorMap.units if isinstance(unit, Elf) and  not unit.dead]:
                count += 1
            if count < elfCount:
                break
            rounds += 1
      
        count = 0
        for elf in [unit for unit in floorMap.units if isinstance(unit, Elf) and  not unit.dead]:
            count += 1
        if elfCount == count:
            elvesLose = False
        else:
            elfPower += 1
        


    

    return(floorMap.getCombatResult(rounds - 1))

    
def test():
  assert run('test1', False) == 27730
  assert run('test2', True) == 36334
  assert run('test3', True) == 39514
  assert run('test4', True) == 27755
  assert run('test5', True) == 28944
  assert run('test6', True) == 18740
  print('Part A Tests Passed')
  
  assert runB('test1', True) == 4988
  assert runB('test3', True) == 31284
  assert runB('test4', True) == 3478
  assert runB('test5', True) == 6474
  assert runB('test6', True) == 1140
  print('Part B Tests Passed')


def main():
  print('Part A: {}'.format(run('input')))
  #print('Part B: {}'.format(runB('input')))
  

if __name__ == '__main__':
    test()
    print('Tests Passed')
    main()
