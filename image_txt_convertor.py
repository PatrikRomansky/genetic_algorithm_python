import evolution_gene as gene
import evolution_individual as ind

def convert_file(file):
    f = open(file, 'r') 
    ind = convert_individual(f)
    f.close()
    return ind 

def convert_individual(file):
    count = 0
    size = int(file.readline().rstrip())
    height = int(file.readline().rstrip())
    width = int(file.readline().rstrip())

    geneType = []

    for _ in range(size):
        count += 1
        # Get next line from file
        line = file.readline().rstrip()
        x1, y1, x2, y2 = line.split(';')
        x1 = int(x1)
        y1 = int(y1)
        x2 = int(x2)
        y2 = int(y2)

        geneType.append(gene.Gene(height = height, width = width, rnd = False, X1 = x1, Y1 = y1, X2 = x2, Y2 = y2))
   
    return ind.Individual(size, height= height, width= width, geneType= geneType)