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




def distribute_points(size_path, target_score):
    """Tính toán số lượng `a, b, c, d` nhanh nhất mà không cần while"""
    
    # Chia tỷ lệ ban đầu (25% -100, 35% 100, 25% 200, 15% 500)
    a = int(size_path * 0.25)  # Điểm -100
    b = int(size_path * 0.35)  # Điểm 100
    c = int(size_path * 0.25)  # Điểm 200
    d = size_path - (a + b + c)  # Điểm 500 còn lại

    # Tính tổng điểm
    total_score = a * (-100) + b * 100 + c * 200 + d * 500

    # Điều chỉnh tăng dần để đạt `target_score`
    missing_score = target_score - total_score
    if missing_score > 0:
        increase_d = min(missing_score // 500, size_path - d)  # Tăng số điểm 500
        d += increase_d
        missing_score -= increase_d * 500

        increase_c = min(missing_score // 200, size_path - (d + c))  # Tăng số điểm 200
        c += increase_c
        missing_score -= increase_c * 200

        increase_b = min(missing_score // 100, size_path - (d + c + b))  # Tăng số điểm 100
        b += increase_b
        missing_score -= increase_b * 100

    return a, b, c, d


def scatter_points(maze, start, goal, level, target_score):
    if level > 1:
        target_score += 5000  # Tăng độ khó cho level cao hơn

    path = find_shortest_path(maze, start, goal)  # Đường đi BFS
    all_path = [(x, y) for x in range(len(maze)) for y in range(len(maze[0])) if maze[x][y] == 0]  # Toàn bộ ô có thể đi
    scattered_point = {}
    points = [-100, 100, 200, 500]

    """ 🔹 TH1: Level 1, 4 → Rải điểm trên đường BFS + Xác suất trên toàn bản đồ """
    if level == 1 or level == 4:
        size_path = int(len(path) * PERCENT[str(level)])  # Số ô cần rải điểm trên đường BFS
        total_score = 0
        a, b, c, d = distribute_points(size_path, target_score)

        """ 🔹 Gán điểm vào đường đi BFS """
        number_point = [-100] * a + [100] * b + [200] * c + [500] * d
        random.shuffle(number_point)

        for i, (x, y) in enumerate(path[1:size_path+1]):  # Bỏ ô Start
            if (x, y) != start and (x, y) != goal:
                scattered_point[(x, y)] = number_point[i]

        """ 🔹 Rải điểm trên toàn bản đồ nhưng với xác suất `>= 0.95` """
        for x, y in all_path:
            if (x, y) not in scattered_point and (x, y) != start and (x, y) != goal and random.random() >= 0.95:
                scattered_point[(x, y)] = random.choice(points)

    """ 🔹 TH2: Level 2, 3, 5 → Rải điểm trên toàn bản đồ (dùng `all_path`) """
    if level in [2, 3, 5]:
        size_path = int(len(all_path) * PERCENT[str(level)])# Số ô cần rải điểm trên toàn bản đồ
        print(len(all_path), PERCENT[str(level)], size_path)
        a, b, c, d = distribute_points(size_path, target_score)
        number_point = [-100] * a + [100] * b + [200] * c + [500] * d
        random.shuffle(number_point)

        valid_cells = [(x, y) for x, y in all_path if (x, y) != start and (x, y) != goal]
        random.shuffle(valid_cells)

        for i in range(min(len(number_point), len(valid_cells))):  # Không vượt quá số ô hợp lệ
            scattered_point[valid_cells[i]] = number_point[i]

    scattered_point_AI = scattered_point.copy()  # Đồng bộ điểm cho AI
    return scattered_point, scattered_point_AI
