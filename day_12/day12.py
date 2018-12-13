from collections import defaultdict
from copy import copy

def parseState(string):
  #parse the initial state out of input
  initialState = defaultdict(lambda:False)
  for i in range(len(string)):
    if string[i] == '#':
      initialState[i] = True
    elif string[i] == '.':
      initialState[i] = False
  return initialState

def nextPlantState(plantNum, state, rules):
  #determine the next plant state based on the current state and rules
  l2 = state[plantNum-2]
  l1 = state[plantNum-1]
  c = state[plantNum]
  r1 = state[plantNum+1]
  r2 = state[plantNum+2]
  nextPlantState = rules[(l2,l1,c,r1,r2)]
  return nextPlantState


def nextOverallState(state, rules, left, right):
  #determine the next state for all plants
  nextState = defaultdict(lambda:False)
  leftmost = None
  rightmost = None
  for i in range(left-2,right+2):
    res = nextPlantState(i, state, rules)
    nextState[i] = res
    if res:
      rightmost = i + 1
      if leftmost is None:
        leftmost = i

  return (nextState, leftmost, rightmost)

def checkAllSame(value, lst):
  #check if all entries in a list are equal to value
  for i in range(len(lst)):
    if lst[i] != value:
      return False
  return True

def main():

  # parse the input
  initialState = None
  leftmost = 0
  rightmost = 0
  rules = {}
  with open('input') as file:
    lines = file.readlines()

    split = lines[0].split(': ')
    initialState = parseState(split[1])
    rightmost = len(list(initialState.keys()))

    for line in lines[2:]:
      line = line.rstrip('\n')
      split = line.split(' => ')
      rule = split[0]
      res = (split[1] == '#')
      l2 = (rule[0] == '#' )
      l1 = (rule[1] == '#')
      c = (rule[2] == '#')
      r1 = (rule[3] == '#')
      r2 = (rule[4] == '#')
      rules[(l2,l1,c,r1,r2)] = res

  # Part A - index-sum after 20 generations
  currentState = copy(initialState)

  for i in range(20):
    currentState,leftmost,rightmost = nextOverallState(currentState, rules, leftmost, rightmost)
    #print(''.join([(lambda x: '#' if x else '.')(currentState[i]) for i in range(leftmost,rightmost)]))

  count = 0
  for i in range(leftmost, rightmost):
    if currentState[i]:
      count += i

  print('Part A: {}'.format(count))


  # Part B - find the pattern before extremely large number

  #reset everything
  currentState = copy(initialState)
  leftmost = 0
  rightmost = len(list(initialState.keys()))
  last20SumDif = [0 for x in range(20)]
  count = 0

  end = 50000000000
  for i in range(0, end):
    #get the new state
    currentState,leftmost,rightmost = nextOverallState(currentState, rules, leftmost, rightmost)

    #determine the difference from the 20 previous states
    oldCount = count
    count = 0
    for j in range(leftmost, rightmost):
      if currentState[j]:
        count += j
    countDif = count - oldCount
    oldCountDif = last20SumDif.pop(0)

    #if they're all the same, assume it will be the the same until the end
    if countDif == oldCountDif and checkAllSame(countDif,last20SumDif):
      dif = (end - 1) - i #how much more we'd have to run this loop
      break
    else:
      last20SumDif.append(countDif)


  #the current count
  count = 0
  for i in range(leftmost, rightmost):
    if currentState[i]:
      count += i

  #answer is (current count) + (number of futher iterations) * (amount of increase per iteration)
  print('Part B: {}'.format(count + dif*countDif))



if __name__ == "__main__":
  main()
