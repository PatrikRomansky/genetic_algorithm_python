class X_Man:
  
  def objective(self, target = None):
    return self.obj

  def __init__(self, obj, modifications):
    self.obj = int(obj)
    # [(index, gene, new_dist), ....]
    self.modifications = modifications