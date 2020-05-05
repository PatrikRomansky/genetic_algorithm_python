import sys
import random
import evolution_gene as gene
import evolution_entita as parent
import evolution_mutant as mutant
import evolution_objective as objective

class Individual(parent.Entita):

  def __init__(self, size, height, width, geneType = None):
    super().__init__(size= size, height = height, width  = width)
    if geneType == None:
      self.geneType = [gene.Gene(height = height, width = width) for i in range(size)]
    else:
      self.geneType = geneType
      
    self.obj = None
    self.obj_values = []
    self.update()

  def modify(self, modifications):

    for m in modifications:
        # structure : [(index, gene, new_dist), ....]
        index, gene, new_dist = m

        self.geneType[index] = gene
        target, old_dist = self.obj_values[index]
        
        self.obj_values[index] = target, int(new_dist)
        self.obj -= int(old_dist)
        self.obj += int(new_dist)
  
  def mutate(self, number_of_mutations, shift):

    if self.obj_values != []:
      o = self.obj
      modifications = []

      mut = random.sample(range(0, self.size), number_of_mutations)

      for index in mut:

        g = self.geneType[index].mutate(shift)

        t, dist = self.obj_values[index]
        new_dist = objective.two_lines_distance(g, t)

        o -= int(dist)
        o += int(new_dist)
        modifications.append((index, g, new_dist))

      
      return mutant.X_Man(o, modifications)