import evolution_gene as gene
import evolution_entita as parent

class Target(parent.Entita):

    def __init__(self, size, height, width, inputGene):
        super().__init__(size= size, height = height, width  = width)

        for line in inputGene:
            for x1,y1,x2,y2 in line:
                self.geneType += [gene.Gene(height = height, width = width, rnd = False, X1 = x1, Y1 = y1, X2 = x2, Y2 = y2)]

        self.update() 