# Celeste-Genetic
Genetic algorithm to solve a particular game, in this case Celeste.
Initially, the DNA consists of a random order of the possible moves.

The X and Y co-ordinates of the character sprite are read from the memory and \n
compared with target co-ordinates to determine the fitness of a particular DNA.
The DNA having highest fitness has the highest chance to continue on to the next generation.
The next generation is created by taking half of the genes from both parents and adding some mutation.
When fitness reaches 1, Algorithm stops.

Edit the fitness and mCheck methods to use it for other games.
