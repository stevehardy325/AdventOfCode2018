def powerLevel(x, y, serial):
  #determine the individual power level of one coord
  rack_id = x + 10
  power = ((rack_id * y) + serial) * rack_id
  power = (int(power / 100) % 10) - 5
  return power

def findMax3by3(serial):
  #determine the best 3x3 square for part A
  powers = {}

  maxSum = None
  maxSumLoc = None
  endx = 300-1
  endy = 300-1
  for i in range(1,endx):
    for j in range(1,endy):
      squareSum = 0
      for dx in range(0,3):
        for dy in range(0,3):
          posx = i + dx
          posy = j+dy
          if (posx, posy) not in powers:
            powers[(posx, posy)] = powerLevel(posx, posy, serial)
          squareSum += powers[(posx,posy)]
      if maxSum is None or squareSum > maxSum:
        maxSum = squareSum
        maxSumLoc = (i,j)

  return maxSumLoc

def calcAreaToCorner(serial):
  #calculate the power contained from every coord to the lower right corner
  #we'll use this with area summation formula to speed up calculation

  toCorners = [[0 for y in range(302)] for x in range(302)]
  power = [[None for y in range(301)] for x in range(301)]

  for x in range(300,0,-1):
    for y in range(300,0,-1):
      power[x][y] = powerLevel(x,y,serial)

  for x in range(300,0,-1):
    for y in range(300,0,-1):
      toCorners[x][y] = power[x][y] + toCorners[x+1][y] + toCorners[x][y+1] - toCorners[x+1][y+1]

  return toCorners

def calcPowerNbyN(x,y,n,toCornerArr):
  # use area summation with the known power-to-corner to calculate the power in a square at x,y
  # formula explanation: https://en.wikipedia.org/wiki/Summed-area_table
  power = toCornerArr[x][y] - toCornerArr[x+n][y] - toCornerArr[x][y+n] + toCornerArr[x+n][y+n]
  return power


def areaSumPartB(serial):
  toCorners = calcAreaToCorner(serial)

  maxSum = None
  maxSumLoc = None

  for i in range(1,301):
    for j in range(1,301):
      for size in range(1,301-max(i,j)):
        areaSum = calcPowerNbyN(i,j,size,toCorners)

        if maxSum is None or areaSum > maxSum:
          maxSum = areaSum
          maxSumLoc = (i,j, size)

  return maxSumLoc


#------------TESTS

def test1():
  assert powerLevel(3,5,8) == 4

def test2():
  assert powerLevel(122,79,57) == -5

def test3():
  assert powerLevel(217,196,39) == 0

def test4():
  assert powerLevel(101,153,71) == 4

def test5():
  assert findMax3by3(18) == (33,45)

def test6():
  assert findMax3by3(42) == (21,61)

def test7():
  id = areaSumPartB(18)
  assert id == (90,269,16)

def main(inputSerial):
  print('\nPart A:\n{}'.format(','.join([str(i) for i in findMax3by3(inputSerial)])))
  print('\nPart B:\n{}'.format(','.join([str(i) for i in areaSumPartB(inputSerial)])))

def run_tests():
  test1()
  test2()
  test3()
  test4()
  test5()
  test6()
  test7()
  print("All tests passed")

if __name__ == "__main__":
  run_tests()
  main(9005) #input from puzzle
