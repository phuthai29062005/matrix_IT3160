import random
from Cost_Matrix import *
from Find_Single_Path import A_star

def total_dist(start, goal, checkpoints):
	dist = cost_matrix[0][checkpoints[0]]
	for i in range(len(checkpoints) - 1):
		dist += cost_matrix[checkpoints[i]][checkpoints[i + 1]]
	dist += cost_matrix[checkpoints[-1]][len(checkpoints) + 1]

	return dist

def generate_neighbors(route):
	neighbors = []
	for i in range(len(route) - 1):
		for j in range(i + 1, len(route)):
			original = route.copy()
			original[i], original[j] = original[j], original[i]
			neighbors.append(original)
	return neighbors

def hill_climbing(maze, start, goal, checkpoints):
	global cost_matrix
	cost_matrix = preprocess(maze, start, goal, checkpoints)
	original = list(range(1, len(checkpoints) + 1))
	random.shuffle(original)
	route = original
	dist = total_dist(start, goal, route)

	while(True):
		neighbors = generate_neighbors(route)
		best_neighbor = min(neighbors, key = lambda x: total_dist(start, goal, x))
		dist_best_neighbor = total_dist(best_neighbor)
		if (dist_best_neighbor >= dist):
			break
		route = best_neighbor
		dist = dist_best_neighbor

	return route

def hill_climbing_Astar(maze, start, goal, checkpoints):
	order = hill_climbing(maze, start, goal, checkpoints)
	A_star(maze, start, order[0])
	for i in range(len(order) - 1):
		A_star(maze, order[i], order[i+1])
	A_star(maze, order[-1], goal)
	








