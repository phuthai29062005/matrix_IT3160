from collections import deque
import numpy as np

GRID = 70

def distance_with_BFS(maze, start, checkpoints): # return list
    result = {start: 0}
    queue = deque([(start, 0)])
    visited = set()
    visited.add(start)

    while queue:
        current, dist = queue.popleft()
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            neighbor = current[0] + dx, current[1] + dy
            if (neighbor[0] < GRID and neighbor[1] < GRID and maze[current[0]][current[1]] == 0 and current not in visited):
                queue.append((neighbor, dist + 1))
                visited.add(neighbor)
                if (neighbor in checkpoints):
                    result.update({neighbor: dist})

    for i in range(len(checkpoints)):
        checkpoints[i] = result[checkpoints[i]]

    return checkpoints

def preprocess(maze, start, goal, checkpoints):
    checkpoints.append(goal)
    checkpoints.insert(0, start)
    total_points = len(checkpoints)
    cost_matrix = np.zeros((total_points, total_points))
    for i in range(total_points):
        cost_matrix[i] = distance_with_BFS(maze, checkpoints[i], checkpoints)
    return cost_matrix