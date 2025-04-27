import numpy as np
import random
import json
import os
from collections import deque

def load_points():
    with open(os.path.join("assets", "config", "percent.json"), "r") as file:
        return json.load(file)

percent_data = load_points()
PERCENT = percent_data["percent"]
GRID_SIZE = 70  # Kích thước mê cung

def find_shortest_path(maze, start, goal):
    """Tìm đường đi ngắn nhất từ start đến goal bằng BFS"""
    queue = deque([(start, [start])])
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path  # Trả về danh sách các ô trên đường đi

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and maze[nx][ny] == 0 and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(nx, ny)]))

    return []  # Nếu không có đường đi hợp lệ
    
def find_start_end(maze, current_level):
   
    path_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if maze[x][y] == 0]
    
    while True:
        start = random.choice(path_cells)
        goal_candidates = [cell for cell in path_cells if cell != start]
        random.shuffle(goal_candidates)

        for goal in goal_candidates:
            path = find_shortest_path(maze, start, goal)
            if current_level <= 2 and len(path) >= 20 and len(path) <= 30:
                return start, goal
            if current_level > 2 and len(path) >= 30:
                return start, goal

def add_extra_paths(maze):
    """Randomly add some extra paths to increase connectivity"""
    for _ in range(GRID_SIZE * 5):  
        x, y = random.randint(1, GRID_SIZE - 2), random.randint(1, GRID_SIZE - 2)
        if maze[x][y] == 1:  
            neighbors = sum(maze[nx][ny] == 0 for nx, ny in 
                            [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])
            if neighbors >= 2:  
                maze[x][y] = 0

def generate_maze():
    """Tạo mê cung bằng thuật toán Recursive Backtracking"""
    maze = np.ones((GRID_SIZE, GRID_SIZE), dtype=int)  # Khởi tạo toàn bộ là tường
    stack = [(random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))]
    visited = set(stack)

    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]

    while stack:
        x, y = stack[-1]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in visited:
                maze[x][y] = 0
                maze[nx][ny] = 0
                maze[x + dx // 2][y + dy // 2] = 0
                stack.append((nx, ny))
                visited.add((nx, ny))
                break
        else:
            stack.pop()

    add_extra_paths(maze)
    return maze

def random_points(maze, start, goal, level):
    all_path = [(x, y) for x in range(len(maze)) for y in range(len(maze[0])) if maze[x][y] == 0]  # Toàn bộ ô có thể đi
    point = {}
    number_point = 0
    
    for i in range(level): 
        number_point += 10
    
    # Bỏ start và goal ra khỏi path
    middle_path = all_path

    # Chọn ngẫu nhiên size_path ô trong số đó
    selected_positions = random.sample(middle_path, number_point)

    # Chuẩn bị danh sách điểm đã được phân phối và xáo trộn

    # Gán điểm vào các vị trí đã chọn
    for i, (x, y) in enumerate(selected_positions):
        point[(x, y)] = 1

    point_AI = point.copy()  # Đồng bộ điểm cho AI
    return point, point_AI
