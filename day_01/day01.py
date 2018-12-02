#!/bin/python3

# https://adventofcode.com/2018/day/1

# Part 1: add together all frequency changes in the input file
# Part 2: find first repeated frequency reached after a change

filename = "input"
file = open(filename, "r")

#sum for part 1
sum = 0

#track repeats for part 2
freqs = dict()
repeated = None

#int array for faster parsing if we need to loop later
intLines = []

for line in file:
    num = int(line)
    intLines += [num]
    #calculate part 1
    sum += num
    #see if the sum is repeated for part 2
    if repeated == None:
        if sum not in freqs:
            freqs[sum] = 1
        else:
            freqs[sum] += 1
            repeated = sum

#we already know the end sum
print("Frequency sum: " + str(sum))

#if we don't have the repeated yet, keep cycling until we do
index = 0
while repeated == None:
    #use the int array, because it will be faster
    num = intLines[index]

    sum += num
    if repeated == None:
        if sum not in freqs:
            freqs[sum] = 1
        else:
            freqs[sum] += 1
            repeated = sum
    index += 1
    if index == len(intLines):  index = 0

print("First repeated frequency: " + str(repeated))
