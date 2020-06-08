from population import *
import pyautogui


START = (-45, 200)
TARGET = (212, 88)

components = ['left', 'right', 'up', 'down', 'c', 'x', 'up,z', 'right,c,x']

for x in range(5, 0, -1):
	print(x)
	time.sleep(1)

population = Population(components=components, dna_length=10, start=START,target=TARGET, MutationRate=0.01, pop_size=3)
generation = 1
while True:
	print("_____________________________________________________")
	print(f"\nGenerate called for generation {generation}\n\n")
	generation+=1
	population.generate()
	print(f"PopLen : {len(population.population)}")
	population.calcFitness()
	population.printBest()
	print(population.avgFitness())

