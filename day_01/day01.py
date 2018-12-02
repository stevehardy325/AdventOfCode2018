#!/bin/python3

# https://adventofcode.com/2018/day/1

# Part 1: add together all frequency changes in the input file
# Part 2: find first repeated frequency reached after a change

class Results:
    #class to abstract the results
    def __init__(self):
        #sum for part 1
        self.sum = 0
        #track repeats for part 2
        self.freqs = dict()
        self.repeated = None

    def changeFreq(self, n):
        #modify the current frequency by an integer amount

        #calculate part 1
        self.sum += num
        #see if the sum is repeated for part 2
        if self.sum not in self.freqs:
            self.freqs[self.sum] = 1
        else:
            self.freqs[self.sum] += 1
            if self.repeated == None:
                self.repeated = self.sum


filename = "input"
file = open(filename, "r")

#object to hold results
res = Results()

#int array for faster parsing if we need to loop later
intLines = []

for line in file:
    num = int(line)
    intLines += [num]
    res.changeFreq(num)

file.close()

#we already know the end sum
print("Frequency sum: " + str(res.sum))

#if we don't have the repeated yet, keep cycling until we do
index = 0
while res.repeated == None:
    #use the int array, because it will be faster
    num = intLines[index]
    res.changeFreq(num)

    index += 1
    if index == len(intLines):  index = 0

print("First repeated frequency: " + str(res.repeated))
