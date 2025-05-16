from collections import deque
import numpy as np

GRID = 70

def distance_with_BFS(maze, start, checkpoints): # return list
    
    result = {start: 0}
    queue = deque([(start, 0)])
    visited = set([start])

    while queue:
        current, dist = queue.popleft()
        if current in checkpoints:
            result[current] = dist
            if len(result) == len(checkpoints):
                break
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if (0 <= neighbor[0] < GRID and 0 <= neighbor[1] < GRID and maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited):                
                queue.append((neighbor, dist + 1))
                visited.add(neighbor)
            
                    
    row_dist = []

    for checkpoint in checkpoints:
        if checkpoint in result:
            row_dist.append(result[checkpoint])
        else:
            # If a checkpoint is unreachable, you might want to handle it
            # For example, use -1 or float('inf') to indicate unreachable
            row_dist.append(-1)  # or float('inf')
    
    return row_dist

def preprocess(maze, start, goal, checkpoints):
    checkpoints.append(goal)
    checkpoints.insert(0, start)
    total_points = len(checkpoints)
    cost_matrix = np.zeros((total_points, total_points))
    for i in range(total_points):
        cost_matrix[i] = distance_with_BFS(maze, checkpoints[i], checkpoints)
    return cost_matrix