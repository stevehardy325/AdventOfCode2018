import re

class Unit:
    def __init__(self, hp):
        self.hp = hp

class Group:
    def __init__(self, units, uhp, weaknesses, immunities, unitPow, unitType, init, army):
        self.units = units
        self.baseHP = uhp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.unitPow = unitPow
        self.unitType = unitType
        self.init = init
        self.armyName = army
        self.target = None

    def __repr__(self):
        #return '<{} units, {} HP, weak to {}, immune to {}, {} {}, {} init>'.format(self.units, self.baseHP, self.weaknesses, self.immunities, self.unitPow, self.unitType, self.init)
        return '{} units'.format(self.units)

    def effectivePow(self):
        return self.units * self.unitPow

    def calculateDamage(self, effectivePower, damageType):
        multiplier = None
        #print(damageType, self.weaknesses)
        if damageType in self.weaknesses:
            multiplier = 2
        elif damageType in self.immunities:
            multiplier = 0
        else:
            multiplier = 1

        damage = multiplier * effectivePower
        #print('Would take ', damage)
        return damage

    def pickTarget(self, possibleTargets):
        self.target = None

        damage = 0
        target = None
        for g in possibleTargets:
            thisDamage = g.calculateDamage(self.effectivePow(), self.unitType)

            if thisDamage > 0:
                if target is None or thisDamage > damage:
                    target = g
                    damage = thisDamage
                elif thisDamage == damage:
                    if g.effectivePow() > target.effectivePow():
                        target = g
                        damage = thisDamage
                    elif g.effectivePow() == target.effectivePow() and g.init > target.init:
                        target = g
                        damage = thisDamage

        self.target = target
        return target

    def takeDamage(self, effectivePower, damageType):
        damage = self.calculateDamage(effectivePower, damageType)
        
        killed = damage // self.baseHP
        self.units = max(0, self.units - killed)


    def attack(self):
        #print("attack")
        if self.target is not None and self.units > 0:
            self.target.takeDamage(self.effectivePow(), self.unitType)

class Army:
    def __init__(self, name):
        self.name = name
        self.groups = []
    
    def append(self, newGroup):
        self.groups.append(newGroup)

    def size(self):
        return len(self.groups)

    def pickTargets(self, otherArmy):
        unchosenTargets = [g for g in otherArmy.groups]
        self.groups.sort(key=lambda g:g.effectivePow(),reverse=True)

        targets = {}
        
        for g in self.groups:
            chosen = g.pickTarget(unchosenTargets)
            if chosen is not None:
                targets[g] = chosen
                unchosenTargets.remove(chosen)
             
        return targets

    



def parseArmy(datastr, armyName, boost):
    findArmy = re.compile('(?<={}:\n)(.+\n)+'.format(armyName))
    findUnits = re.compile('\\d+(?= units)')
    findHP = re.compile('\d+(?= hit points)')
    findWeak = re.compile('((?<=weak to )(\\w+[, ]*)*)')
    findImmune = re.compile('((?<=immune to )(\\w+[, ]*)*)')
    findAttack = re.compile('(?<=that does )(\\d+) (\\w+)(?= damage)')
    findInit = re.compile('(?<=at initiative )\\d+')

    
    armyStr = findArmy.search(datastr).group(0)
    split = armyStr.strip('\n').split('\n')

    army = Army(armyName)

    for line in split:
        units = int(findUnits.search(line).group(0))
        hp = int(findHP.search(line).group(0))

        weaknesses = []
        if findWeak.search(line):
            weaknesses = findWeak.search(line).group(0).split(', ')

        immunities = []
        if findImmune.search(line):
            immunities = findImmune.search(line).group(0).split(', ')

        attackPow = int(findAttack.search(line).group(1)) + boost
        attackType = findAttack.search(line).group(2)
        init = int(findInit.search(line).group(0))

        newGroup = Group(units, hp, weaknesses, immunities, attackPow, attackType, init, armyName)
        army.append(newGroup)
    
    return army

def fight(armyOne, armyTwo):
    #print(armyOne.groups, armyTwo.groups)

    lastArmyOne = None
    lastArmyTwo = None
    infinite = False

    while armyOne.size() > 0 and armyTwo.size() > 0:
        pass
        #target
        lastArmyOne = sum([g.units for g in armyOne.groups])
        lastArmyTwo = sum([g.units for g in armyTwo.groups])
        armyOne.pickTargets(armyTwo)
        armyTwo.pickTargets(armyOne)
        
        #attack
        queue = [g for g in armyOne.groups] + [g for g in armyTwo.groups]
        queue.sort(key = lambda g:g.init, reverse=True)

        for g in queue:
            if g.target is not None:
                tIndex = queue.index(g.target)
                g.attack()
                queue[tIndex] = g.target

        armyOne.groups = []
        armyTwo.groups = []

        for g in queue:
            if g.units > 0:
                if g.armyName == armyOne.name:
                    armyOne.groups.append(g)
                elif g.armyName == armyTwo.name:
                    armyTwo.groups.append(g)

        if lastArmyOne == sum([g.units for g in armyOne.groups]) and lastArmyTwo == sum([g.units for g in armyTwo.groups]):
            print('infinite loop')
            infinite = True
            break

    if infinite:
        survivors = armyTwo
    if armyOne.size() > armyTwo.size():
        survivors = armyOne
    else:
        survivors = armyTwo

    return sum([g.units for g in survivors.groups]), survivors.name

def parseFile(filename, shouldBoost=False):
    fileAsString = ''
    with open(filename) as data:
        fileAsString = data.read()

    deerLoses = True
    boost = 0
    while (boost == 0 or shouldBoost) and deerLoses:
        immuneSys = parseArmy(fileAsString, 'Immune System', boost)
        infection = parseArmy(fileAsString, 'Infection', 0)
        winner, winName = fight(immuneSys, infection)
        if winName != 'Immune System':
            boost += 1
            print(boost, winner, winName)
        else:
            deerLoses = False

    return winner

def main():
    print('Part A: ',parseFile('input'))
    print('Part B: ',parseFile('input', True))

if __name__ == "__main__":
    main()