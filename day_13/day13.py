from collections import defaultdict
from time import sleep


class Track:
  def __init__(self, orientation):
    '''self.x = x
    self.y = y'''
    self.carts = []
    self.orientation = orientation

  def addCart(self, cart):
    self.carts.append(cart)
    ok = True
    if len(self.carts) > 1:
       ok = False
    return ok

  def popCart(self):
    cart = None
    cart = self.carts.pop(0)
      
    return cart

  def __repr__(self):
    if len(self.carts) == 0:
      return self.orientation
    elif len(self.carts) > 1:
      return 'X'
    else:
      return str(self.carts[0])

class TurnTrack(Track):
  rightTurns = set([('lu', 'd'), ('ld', 'r'), ('ru', 'l'), ('rd', 'u')])

  def __init__(self, turnType):
    Track.__init__(self, turnType)
    self.turnType = turnType

  def addCart(self, cart):
    cartDir = cart.getFacing()
    if self.turnType == '\\':
      if cartDir == 'r' or cartDir == 'l': cart.turn('r')
      else: cart.turn('l')
    else:
      if cartDir == 'r' or cartDir == 'l': cart.turn('l')
      else: cart.turn('r')
         
    return Track.addCart(self,cart)
  
  def __repr__(self):
    if len(self.carts) == 0:
      return self.turnType
    else:
      return str(self.carts[0])

class Intersection(Track):
  def __init__(self):
    Track.__init__(self, '+')

  def addCart(self, cart):
    cart.intersectionTurn()
    return Track.addCart(self,cart)
  

class Cart:
  turns = ['l', 's', 'r']
  directions = [(0,-1),(1,0),(0,1),(-1,0)]
  directionMap = {'u':0,'r':1,'d':2,'l':3}

  def __init__(self, x, y, face):
    self.x = x
    self.y = y
    self.face = Cart.directionMap[face]
    self.nextTurn = 0

  def getFacing(self):
    direction = None
    for facing in Cart.directionMap:
      if Cart.directionMap[facing] == self.face:
        direction = facing
        break
    return direction

  def move(self):
    self.x += Cart.directions[self.face][0]
    self.y += Cart.directions[self.face][1]
    return (self.x, self.y)

  def turn(self, turnDir):
    if turnDir == 'l':
      self.face = (self.face - 1) % len(Cart.directions)
    elif turnDir == 'r':
      self.face = (self.face + 1) % len(Cart.directions)

  def intersectionTurn(self):
    self.turn(Cart.turns[self.nextTurn])
    self.nextTurn = (self.nextTurn + 1) % len(Cart.turns)

  def __lt__(self, other):
    res = False
    if self.y < other.y:
      res = True
    elif self.y == other.y and self.x < other.x:
      res = True
    return res

  def __repr__(self):
    return self.getFacing()

  def __str__(self):
    return self.getFacing()


def parseInput(inputFileName):
  tracks = []
  carts = []

  turnChars = set(['\\', '/'])
  straightChars = set(['-', '|'])
  cartChars = {'<':'l', '>':'r', '^':'u', 'v':'d'}
  
  with open(inputFileName) as file:
    y = 0
    for line in file:
      x = 0
      trackRow = []
      for char in line:
        if char in cartChars:
          newCart = Cart(x, y, cartChars[char])
          if char == '<' or char == '>':
            trackDir = '-'
          else:
            trackDir = '|'
          newTrack = Track(trackDir)
          newTrack.addCart(newCart)
          trackRow.append(newTrack)
          carts.append(newCart)
        elif char  in straightChars:
          trackRow.append(Track(char))
        elif char == '+':
          trackRow.append(Intersection())
        elif char in turnChars:
          trackRow.append(TurnTrack(char))
        else:
          trackRow.append(None)
        x += 1
      tracks.append(trackRow)
      y += 1

  return (tracks, carts)

def printTracks(tracks):
  stringRep = '\n'.join([''.join([(lambda unit: unit.__repr__() if unit is not None else ' ')(char) for char in line]) for line in tracks])
  
  return stringRep

def findCrash(tracks, carts):
  x,y = None,None
  iteration = 0
  noCrash = True
  while noCrash:
    carts.sort()
    #print('\n{}\n{}'.format(iteration,printTracks(tracks)))
    
    for cart in carts:
      x,y = cart.x, cart.y
      tracks[y][x].popCart()
      dx,dy = cart.move()
      noCrash = tracks[dy][dx].addCart(cart)
      if not noCrash:
        break
    iteration += 1
  #print('\n{}\n{}'.format(iteration,printTracks(tracks)))
    
  return dx,dy

def runUntilOne(tracks,carts):
  x,y = None,None
  iteration = 0
  noCrash = True
  crashes = 0
  crashedFirst = None
  while len(carts) > 1:
    crashed = []
    carts.sort()
    for cart in carts:
      if cart not in crashed:
        x, y = cart.x, cart.y
        tracks[y][x].popCart()
        dx,dy = cart.move()
        noCrash = tracks[dy][dx].addCart(cart)
        if not noCrash:
          if crashes == 0:
            crashes = 1
            crashedFirst = (dx,dy)
          
          crashed += tracks[dy][dx].carts
          tracks[dy][dx].carts = []
      
    initialLen = len(carts)
    for cart in crashed:
      carts.remove(cart)
    assert len(carts) == initialLen - len(crashed)
    


    iteration += 1
  #print('\n{}\n{}'.format(iteration,printTracks(tracks)))
  x,y = carts[0].x, carts[0].y
  lastStanding = (x,y)
  return (crashedFirst, lastStanding)

def run_tests():
  (tracks,carts) = parseInput("testInput")
  (x, y) = findCrash(tracks, carts)
  assert (x,y) == (7,3)
  (tracks,carts) = parseInput("testInput2")
  (x, y) = runUntilOne(tracks, carts)
  assert y == (6,4)

def main():
  run_tests()
  print('All Tests Passed')
  (tracks,carts) = parseInput("input")
  print('Input Parsed')
  
  (crashedFirst, LastStanding) = runUntilOne(tracks, carts)
  print((crashedFirst, LastStanding))


if __name__ == "__main__":
  main()
