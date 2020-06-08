import random
import math


def sigmoid(number):
    return 1 / (math.exp(-number) + 1)


class DNA:
    def __init__(self, length=20, components=[]):
        self.components = components
        self.dna = []
        self.length = length
        self.fitness = 0

        for x in range(length):
            self.dna.append(random.choice(components))


    @staticmethod   
    def rescale(xmax, x, xmin=0):
        ## Rescale to linear fitness (0 to 1).
        ## As distance approaches xmax, the scaled output approaches 0.
        ## As distance approaches xmin, the scaled output appreaches 1.
        scaled = (x-xmax)/(xmin-xmax)
        return scaled

    def calcfitness(self, current_pos, target_pos, xmax):
        ## Calculate distance and rescale it. 
        distance = math.sqrt((target_pos[0]-current_pos[0])**2 + (target_pos[1]-current_pos[1])**2)
        self.fitness = DNA.rescale(xmax, distance)
        return self.fitness

    def mutate(self, MutationRate):
        MutationRate_ = MutationRate * 1000
        for x in self.dna:
            rand = random.randrange(0,1000)
            if rand < MutationRate_:
                self.dna[random.randint(0, len(self.dna))] = random.choice(self.components)

    def crossover(self, parent):
        new_child = DNA(self.length, self.components)
        for x in range(self.length):
            if x % 2 == 0:
                new_child.dna[x] = self.dna[x]
            else:
                new_child.dna[x] = parent.dna[x]
        return new_child

    def __str__(self):
        return f"DNA : {self.dna}\nFitness : {self.fitness}"



"""z = DNA(length=10,components=['Z','X','C','L','U','D','R'])
d = DNA(length=10,components=['Z','X','C','L','U','D','R'])
print(d)
d.crossover(z)
print(d)

"""