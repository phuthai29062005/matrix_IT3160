import random
from Cost_Matrix import *
from Easy import A_star
import numpy as np

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

def simulated_annealing(maze, start, goal, checkpoints, temperature, cooling_rate, max_iter):
	global cost_matrix
	cost_matrix = preprocess(maze, start, goal, checkpoints)
	original = list(range(1, len(checkpoints) + 1))
	random.shuffle(original)
	current_route = original
	current_dist = total_dist(start, goal, original)
	best_route = current_route
	best_dist = current_dist

	for _ in range(max_iter):
		neighbors = generate_neighbors(current_route) 
		next_route = random.choice(neighbors)
		dist_next_route = total_dist(start, goal,next_route)

		if (dist_next_route < current_dist or random.random() < np.exp((current_dist - dist_next_route) / temperature)):
			current_route = next_route
			current_dist = dist_next_route
			if (current_dist < best_dist):
				best_route = current_route
				best_dist = current_dist
		
		temperature *= cooling_rate

	return best_route 

def simulated_annealing_Astar(maze, start, goal, checkpoints, temperature = 300, cooling_rate = 0.99, max_iter = 1000):
	order = simulated_annealing(maze, start, goal, checkpoints, temperature, cooling_rate, max_iter)
	A_star(maze, start, order[0])
	for i in range(len(order) - 1):
		A_star(maze, order[i], order[i+1])
	A_star(maze, order[-1], goal)








