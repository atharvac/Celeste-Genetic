import random
from dna import *
from memCheck import *
import pyautogui
import time

PROCESS_NAME = "Celeste"
MEMORY_X = 0x497573EC
MEMORY_Y = 0x497573F0
DEATH_CTR = 0x72282FA8



read = ReadMemory()
read.createProcessHandler(PROCESS_NAME)

def keypress(key, delay=0.1, verbose=True):
    key = key.split(',')
    if verbose:
        print(f"Pressing keys: {key}")

    for x in key:
        pyautogui.keyDown(x)
    time.sleep(delay)
    for x in key:
        pyautogui.keyUp(x)

def getCurrentPos():
    x = read.readMemory(MEMORY_X, dtype='float')
    y = read.readMemory(MEMORY_Y, dtype='float')
    return (x, y)

def getDeathCount():
    return read.readMemory(DEATH_CTR, dtype='int')


def resetStage():
    keypress('esc')
    keypress('down')
    keypress('enter')
    time.sleep(1.5)



class Population:
    def __init__(self, dna_length, start, target, MutationRate, pop_size=1000, components=[]):
        self.population = [DNA(components=components, length=dna_length) for x in range(pop_size)]
        self.pop_size = pop_size
        self.dna_len = dna_length
        self.MatingPool = []
        self.generations = 0
        self.best = ''
        self.target = target
        self.start = start
        self.MutationRate = MutationRate
        self.maxDist = Population.calcDistance(start, target)

        self.fitnessWeights = []
        self.calcFitness()


    @staticmethod
    def calcDistance(start_pos, target_pos):
        distance = math.sqrt((target_pos[0]-start_pos[0])**2 + (target_pos[1]-start_pos[1])**2)
        return distance


    def calcFitness(self):
        bestfit = 0
        for i,x in enumerate(self.population):
            death_ct = getDeathCount()
            pos = []
            print(f"DNA length : {len(x.dna)}")
            for inp in x.dna:
                keypress(inp)
                
                if getDeathCount() > death_ct:
                    death_ct += 1 
                    break
                new_pos = getCurrentPos()
                #print(str(new_pos[0]).split('.'))
                if new_pos != self.start and int(str(new_pos[0]).split('.')[1]) == 0: 
                    pos.append(new_pos)
                else:
                    print(new_pos)

            if len(pos)==0:
                pos.append(self.start)
            time.sleep(1)
            resetStage()
            death_ct += 1


            fitness = x.calcfitness(pos[-1], self.target, self.maxDist)
            print(f"Fitness for {i}: {fitness}\t For {pos[-1]}")
            self.fitnessWeights.append(fitness)
            if fitness > bestfit:
                bestfit = fitness
                self.best = x

    def generate(self):
        self.MatingPool.clear()
        for x in range(self.pop_size):
            parents = random.choices(self.population, weights=self.fitnessWeights, k=2)
            child = parents[0].crossover(parents[1])
            child.mutate(self.MutationRate)
            self.MatingPool.append(child)
        self.population.clear()
        self.fitnessWeights.clear()
        self.population = self.MatingPool.copy()

    def printBest(self):
        print(f"Current Best: {self.best}")

    def avgFitness(self):
        total = 0
        for x in self.fitnessWeights:
            total += x
        return total/self.dna_len


#p = Population(components=['L', 'R', 'X'], dna_length=100, target=(276,32),MutationRate=0.001)