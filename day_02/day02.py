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
