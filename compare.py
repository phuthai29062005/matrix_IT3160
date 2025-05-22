import pygame
import copy
import time
from game_state import GameState
from Easy import *
from ui import *
from Hill_Climbing_With_Astar import *
from Simulated_Annealing_With_Astar import *
from Genetic_Algorithm_With_Astar import *

def choose_position(screen, state, events):
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and state.maze is not None:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Tính toán tọa độ tương đối so với góc mê cung
            relative_x = mouse_x - PLAYER_POS[0]
            relative_y = mouse_y - PLAYER_POS[1]
            
            # Chỉ xử lý nếu click trong vùng mê cung
            if 0 <= relative_x < GRID_SIZE * CELL_SIZE_PLAYER and 0 <= relative_y < GRID_SIZE * CELL_SIZE_PLAYER:
                row = int(relative_x // CELL_SIZE_PLAYER)
                col = int(relative_y // CELL_SIZE_PLAYER)
                
                if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                    if state.start_pos is None:
                        state.start_pos = (row, col)
                        state.maze[row][col] = 0
                        print(f"Start position set to: {row}, {col}")
                    elif state.goal_pos is None and (row, col) != state.start_pos:
                        state.goal_pos = (row, col)
                        state.maze[row][col] = 0
                        print(f"Goal position set to: {row}, {col}")
                    
                    if state.start_pos and state.goal_pos:
                        compare_maze(screen, state)
                            
def compare_maze(screen, state):
    if len(state.scattered_points) == 0:
        
        maze_copy_for_bfs = copy.deepcopy(state.maze)
        maze_copy_for_dfs = copy.deepcopy(state.maze)
        maze_copy_for_greedy = copy.deepcopy(state.maze)
        maze_copy_for_Astar = copy.deepcopy(state.maze)

        # Tọa độ để hiển thị thời gian (bên phải màn hình)
        time_display_x = SCREEN_WIDTH - 300  # Điều chỉnh vị trí theo nhu cầu
        time_display_y_start = 100  # Bắt đầu từ vị trí này và tăng dần cho mỗi thuật toán

        
        start = time.perf_counter()
        state.bfs_path = BFS_solve(screen, maze_copy_for_bfs, state.start_pos, state.goal_pos, state.scattered_points, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)
        end = time.perf_counter()
        state.bfs_time = round(end - start, 8)
        
        start = time.perf_counter()
        state.dfs_path = DFS_solve(screen, maze_copy_for_dfs, state.start_pos, state.goal_pos, state.scattered_points, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)
        end = time.perf_counter()
        state.dfs_time = round(end - start, 8)
        
        start = time.perf_counter()
        state.greedy_path = GreedyBestFirst_solve(screen, maze_copy_for_greedy, state.start_pos, state.goal_pos, state.scattered_points, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)
        end = time.perf_counter()
        state.greedy_time = round(end - start, 8)

        start = time.perf_counter()
        state.Astar_path = A_star_solve(screen, maze_copy_for_Astar, state.start_pos, state.goal_pos, state.scattered_points, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER, True)
        end = time.perf_counter()
        state.Astar_time = round(end - start, 8)
        
    else:
        checkpoints = list(state.ai_scattered_points.keys()) 
        state.Astar_path = hill_climbing_Astar(state.maze, state.start_pos, state.goal_pos, checkpoints)
        print("đã chạy xong hill", len(state.Astar_path))
        state.Astar_path = ga_Astar(state.maze, state.start_pos, state.goal_pos, checkpoints)
        print("đã chạy xong a*", len(state.Astar_path))
    
        state.ai_path = simulated_annealing_Astar(state.maze, state.start_pos, state.goal_pos, checkpoints)
        print("đã chạy xong simulated", len(state.Astar_path))
        