#Part 1 - calculate a checksum with the following formula:
# (count of boxes with exactly 2 of any letter) * (count of boxes with exactly 3 of any letter)

filename = "input"
file = open(filename, "r")

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



boxes = []
for line in file:
    boxes += [Box(line)]
file.close()

twos = 0
threes = 0
for box in boxes:
    if box.hasExactTwo: twos += 1
    if box.hasExactThree: threes += 1
checksum = twos * threes

print("Checksum: " + str(checksum))

for i in range(len(boxes)):
    first = boxes[i]
    for j in range(i+1, len(boxes)):
        second = boxes[j]
        common = first.compareBoxID(second)
        if common != None:
            print("Common Letters: " + common)
