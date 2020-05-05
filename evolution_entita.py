class Entita:
    def __init__(self, size, height, width):
        self.size = size
        self.height = height
        self.width = width
        self.geneType = []

    def ToString(self):
        delimiter = '\n'
        out = ''
        out += str(self.size) + delimiter
        out += str(self.height) + delimiter
        out += str(self.width) + delimiter

        for g in self.geneType[:-1]:
            out += g.ToString() + delimiter

        out += self.geneType[-1].ToString()
        
        return out

    def update(self):
        self.geneType.sort(key=lambda g: (g.X1, g.Y1))