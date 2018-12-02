#!/bin/python3

# https://adventofcode.com/2018/day/1

# add together all frequency changes in the input file

filename = "input"
file = open(filename, "r")
sum = 0

for line in file:
    num = int(line)
    sum += num
    
print(sum)
