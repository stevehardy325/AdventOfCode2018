#Part 1 - calculate a checksum with the following formula:
# (count of boxes with exactly 2 of any letter) * (count of boxes with exactly 3 of any letter)

#Part 2 - find common letters shared between the two boxes with only 1 letter difference between ids

class Box:
    def __init__(self, id):
        self.id = id
        self.letterCounts = dict()
        for letter in self.id:
            if letter in self.letterCounts:
                self.letterCounts[letter] += 1
            else:
                self.letterCounts[letter] = 1

        self.hasExactTwo = False
        self.hasExactThree = False
        for letter in self.letterCounts:
            if self.letterCounts[letter] == 2:
                self.hasExactTwo = True
            if self.letterCounts[letter] == 3:
                self.hasExactThree = True

    def compareBoxID(self, other):
        diffs = []
        for i in range(len(self.id)):
            if self.id[i] != other.id[i]:
                diffs += [i]
        if len(diffs) == 1:
            strSame = self.id[0:diffs[0]] + self.id[diffs[0]+1:]
        else:
            strSame = None
        return strSame

class BoxChecker:
    def __init__(self, filename):
        file = open(filename, "r")
        self.boxes = []
        for line in file:
            self.boxes += [Box(line)]
        file.close()

    def checksum(self):
        twos = 0
        threes = 0
        for box in self.boxes:
            if box.hasExactTwo: twos += 1
            if box.hasExactThree: threes += 1
        checksum = twos * threes
        return str(checksum)

    def compareBoxes(self):
        for i in range(len(self.boxes)):
            first = self.boxes[i]
            for j in range(i+1, len(self.boxes)):
                second = self.boxes[j]
                common = first.compareBoxID(second)
                if common != None:
                    return common

def main():
    checker = BoxChecker("input")
    print("Checksum: " + checker.checksum())
    print("Common Letters: " + checker.compareBoxes())

if __name__ == '__main__':
    main()
