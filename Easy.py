from collections import deque
from queue import PriorityQueue
import numpy as np
from colors_and_fonts import WHITE
from ui import *

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def BFS_solve(screen, maze, start, goal, scattered_points, pos, border_color, cell_size):

    queue = deque([start])
    visited = {start: None}  # dùng dict để lưu cha
    visited_cells = set()
    
    while queue:
        current = queue.popleft()
        visited_cells.add(current)

        # Cập nhật maze: đánh dấu đã đi
        maze[current[0]][current[1]] = 2  # Giả sử 2 là đường trắng

        # Vẽ lại màn hình
        draw_maze(screen, maze, pos, border_color, cell_size, start, goal, current, current, visited_cells, scattered_points, blink_state=True)
        pygame.display.update()
        pygame.time.delay(20)  # Delay 50ms cho đẹp mắt

        if current == goal:
            break

        # Duyệt các ô lân cận
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                queue.append(neighbor)
                visited[neighbor] = current

    # Truy ngược để tìm path
    path = []
    while current is not None:
        path.append(current)
        current = visited[current]
    return len(path) 

def DFS_solve(screen, maze, start, goal, scattered_points, pos, border_color, cell_size):
    stack = [start]
    visited = {start: None}
    visited_cells = set()

    while stack:
        current = stack.pop()
        visited_cells.add(current)
        maze[current[0]][current[1]] = 2  # Giả sử 2 là đường trắng

        draw_maze(screen, maze, pos, border_color, cell_size, start, goal, current, current, visited_cells, scattered_points, blink_state=True)
        pygame.display.update()
        pygame.time.delay(20)  # Delay 50ms cho đẹp mắt
        if current == goal:
            break

        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                stack.append(neighbor)
                visited[neighbor] = current

    # Truy vết path và vẽ
    path = []
    current = goal
    while current is not None:
        path.append(current)
        current = visited[current]
    return len(path)  

def GreedyBestFirst_solve(screen, maze, start, goal, scattered_points, pos, border_color, cell_size):
    queue = PriorityQueue()
    queue.put((0, start))
    visited = {start: None}
    visited_cells = set()

    while not queue.empty():
        _, current = queue.get()
        visited_cells.add(current)
        maze[current[0]][current[1]] = 2
        draw_maze(screen, maze, pos, border_color, cell_size, start, goal, current, current, visited_cells, scattered_points, blink_state=True)
        pygame.display.update()
        pygame.time.delay(20)  # Delay 50ms cho đẹp mắt

        if current == goal:
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                priority = heuristic(neighbor, goal)
                queue.put((priority, neighbor))
                visited[neighbor] = current

    path = []
    while current is not None:
        path.append(current)
        current = visited[current]
    return len(path)


def A_star_solve(screen, maze, start, goal, scattered_points, pos, border_color, cell_size, draw):
    fringe = PriorityQueue()
    fringe.put((0, start))
    visited = {start: None} # dùng dict để lưu cha
    visited_cells = set()
    cost = {start: 0} # lưu chi phí thực từ start đến neighbor

    while not fringe.empty():
        _, current = fringe.get()
        visited_cells.add(current)
        maze[current[0]][current[1]] = 2
        if draw == True:
            draw_maze(screen, maze, pos, border_color, cell_size, start, goal, current, current, visited_cells, scattered_points, blink_state=True)
            pygame.display.update()
            pygame.time.delay(20)  # Delay 50ms cho đẹp mắt

        if current == goal:
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                new_cost = cost[current] + 1
                cost[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                fringe.put((priority, neighbor))
                visited[neighbor] = current

    current = goal 
    path = []
    while current is not None:
        path.append(current)
        current = visited.get(current)
    return len(path)  # Trả về đường đi từ start đến goal

def A_star(maze, start, goal):
    fringe = PriorityQueue()
    fringe.put((0, start))
    visited = {start: None} # dùng dict để lưu cha
    cost = {start: 0} # lưu chi phí thực từ start đến một nút

    while not fringe.empty():
        _, current = fringe.get()
        if current == goal:
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and maze[neighbor[0]][neighbor[1]] == 0 and neighbor not in visited:
                new_cost = cost[current] + 1
                cost[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                fringe.put((priority, neighbor))
                visited[neighbor] = current

    current = goal 
    path = []
    while current is not None:
        path.append(current)
        current = visited.get(current)
    return path[::-1]  # Trả về đường đi từ start đến goal



