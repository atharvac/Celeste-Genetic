import random
import math



TARGET = (464, -8)
START = (200, 32)


def calcDistance(current_pos, target_pos):
    distance = math.sqrt((target_pos[0]-current_pos[0])**2 + (target_pos[1]-current_pos[1])**2)
    distance2 = abs((target_pos[0]-current_pos[0]) + (target_pos[1]-current_pos[1]))

    r1 = rescale(267, distance)
    r2 = rescale(224, distance2)
    return r1, r2

def rescale(xmax, x, xmin=0):
	scaled = (x-xmax)/(xmin-xmax)
	return scaled

print(calcDistance((400, 60),TARGET))