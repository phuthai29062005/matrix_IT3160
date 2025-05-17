import random
from Cost_Matrix import *
from Easy import A_star
from ui import *

def total_dist(start, goal, route, cost_matrix): # cho mỗi route
	#print("route: " + str(route))
	dist = cost_matrix[0][route[0]]
	for i in range(len(route) - 1):
		dist += cost_matrix[i][i + 1]
	dist += cost_matrix[route[-1]][len(cost_matrix) - 1]

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
	cost_matrix = preprocess(maze, start, goal, checkpoints.copy())
	original = list(range(1, len(checkpoints) + 1))
	random.shuffle(original)
	route = original
	dist = total_dist(start, goal, route, cost_matrix)

	while(True):
		neighbors = generate_neighbors(route)
		best_neighbor = min(neighbors, key = lambda x: total_dist(start, goal, x, cost_matrix))
		dist_best_neighbor = total_dist(start, goal, best_neighbor, cost_matrix)
		if (dist_best_neighbor >= dist):
			break
		route = best_neighbor
		dist = dist_best_neighbor

	return route 

def hill_climbing_Astar(maze, start, goal, checkpoints):
	order = hill_climbing(maze, start, goal, checkpoints)
	order = [x - 1 for x in order]  # chuyển đổi từ 1-based index sang 0-based index

	path = A_star(None, maze, start, checkpoints[order[0]], checkpoints, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False)
	for i in range(len(order) - 1):
		path.extend(A_star(None, maze, checkpoints[order[i]], checkpoints[order[i + 1]], None, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False))
	path.extend(A_star(None, maze, checkpoints[order[-1]], goal, None, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False))

	for x in range(len(maze)):
		for y in range(len(maze[x])):
			if maze[x][y] == 2:
				maze[x][y] = 0

	return path
	








