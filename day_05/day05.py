import string
import operator

def react(polymerList):
    currentIndex = 0
    while currentIndex < len(polymerList) - 1:
        nextIndex = currentIndex + 1
        currentPoly = polymerList[currentIndex]
        nextPoly = polymerList[nextIndex]
        if currentPoly != nextPoly and currentPoly.upper() == nextPoly.upper():
            polymerList.pop(currentIndex)
            polymerList.pop(currentIndex)
            currentIndex = max(currentIndex - 1, 0)
        else:
            currentIndex += 1
    return polymerList

def removeReactant(polymerList, lower):
    upper = lower.upper()
    return [poly for poly in polymerList if poly != lower and poly != upper]

def main():
    filename='input'
    polymer = ''

    with open(filename, 'r') as file:
        for line in file:
            polymer += line

    polymerList = list(polymer[:-1])

    print("Part A: " + str(len(react(polymerList))))

    variants = dict()
    for lower in string.ascii_lowercase:
        variants[lower] = len(react(removeReactant(polymerList, lower)))

    shortest = min(variants.items(), key=operator.itemgetter(1))[1]
    print('Part B: ' + str(shortest))



if __name__ == '__main__':
    main()
