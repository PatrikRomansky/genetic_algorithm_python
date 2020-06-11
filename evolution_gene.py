import math
import random

# Line representation
class Gene:
  def __init__(self, height = 0, width = 0, rnd= True, X1= 0, Y1= 0, X2= 0, Y2= 0):
    if rnd:

      # line points
      self.X1 = random.randrange(0, width, 1)
      self.X2 = self.X1 + random.randrange(0, 20, 1)

      self.Y1 = random.randrange(0, height, 1)   
      self.Y2 = self.Y1 + random.randrange(0, 20, 1)

    else:
      self.X1 = X1
      self.X2 = X2
      self.Y1 = Y1
      self.Y2 = Y2
  
  # String representaion
  def ToString(self):
    delimiter = ';'
    out = str(self.X1) + delimiter
    out += str(self.Y1) + delimiter
    out += str(self.X2) + delimiter
    out += str(self.Y2)

    return out

  # line points shift
  def get_shift(self, shift):
    result = random.randrange(0, shift)
    return result if random.randint(0, 1) == 1 else -result

  # shift mutation
  def mutate(self, shift):
    x1 = self.X1 + self.get_shift(shift)
    y1 = self.Y1 + self.get_shift(shift)
    x2 = self.X2 + self.get_shift(shift)
    y2 = self.Y2 + self.get_shift(shift)
    return Gene(rnd= False, X1 = x1, Y1 =y1, X2 = x2, Y2 = y2)