import random
from Cost_Matrix import *
from Easy import A_star
import numpy as np
from ui import *

def total_dist(start, goal, route, cost_matrix): # cho mỗi route
	dist = cost_matrix[0][route[0]]
	for i in range(len(route) - 1):
		dist += cost_matrix[route[i]][route[i + 1]]
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

def simulated_annealing(maze, start, goal, checkpoints, temperature, cooling_rate, max_iter):
	cost_matrix = preprocess(maze, start, goal, checkpoints.copy())
	original = list(range(1, len(checkpoints) + 1))
	random.shuffle(original)
	current_route = original
	current_dist = total_dist(start, goal, original, cost_matrix)
	best_route = current_route
	best_dist = current_dist

	for _ in range(max_iter):
		neighbors = generate_neighbors(current_route) 
		next_route = random.choice(neighbors)
		dist_next_route = total_dist(start, goal,next_route, cost_matrix)

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
	order = [x - 1 for x in order]  # chuyển đổi từ 1-based index sang 0-based index

	# Tạo một bản sao của maze để không ảnh hưởng đến maze gốc
	maze_copy = maze.copy()
	path = A_star(None, maze_copy, start, checkpoints[order[0]], None, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False)

	# Reset maze sau mỗi lần tìm đường
	for x in range(len(maze_copy)):
		for y in range(len(maze_copy[0])):
			if maze_copy[x][y] == 2:
				maze_copy[x][y] = 0

	# Tạo đường đi giữa các checkpoints
	for i in range(len(order) - 1):
		segment = A_star(None, maze_copy, checkpoints[order[i]], checkpoints[order[i + 1]], None, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False)
		path.extend(segment[1:])  # Bỏ phần tử đầu để tránh trùng lặp

		# Reset maze sau mỗi lần tìm đường
		for x in range(len(maze_copy)):
			for y in range(len(maze_copy[0])):
				if maze_copy[x][y] == 2:
					maze_copy[x][y] = 0

	# Tạo đường đi từ checkpoint cuối cùng đến goal
	final_segment = A_star(None, maze_copy, checkpoints[order[-1]], goal, None, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False)
	path.extend(final_segment[1:])  # Bỏ phần tử đầu để tránh trùng lặp

	for x in range(len(maze)):
		for y in range(len(maze[0])):
			if maze[x][y] == 2:
				maze[x][y] = 0
	return path


	








