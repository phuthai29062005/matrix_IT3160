import pygame
import copy
import time
from game_state import GameState
from Easy import *
from ui import *
from Hill_Climbing_With_Astar import *
from Simulated_Annealing_With_Astar import *
from Genetic_Algorithm_With_Astar import *
from game_logic import *

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
        if len(state.ai_path) == 0 or state.player_pos == state.goal_pos:
            checkpoints = list(state.ai_scattered_points.keys())
            if state.level == 1:
                state.ai_path = hill_climbing_Astar(state.maze, state.player_pos, state.goal_pos, checkpoints)
                state.Hill_path = len(state.ai_path)
            elif state.level == 2:
                state.ai_path = ga_Astar(state.maze, state.player_pos, state.goal_pos, checkpoints, 130, 0.15, 0.2)
                state.Star_path = len(state.ai_path)
            elif state.level == 3:
                state.ai_path = simulated_annealing_Astar(state.maze, state.player_pos, state.goal_pos, checkpoints, 1400, 0.99, 100000)
                state.Simulated_path = len(state.ai_path)
        state.player_pos, state.ai_last_move_time = move_ai(
            state.maze, 
            state.player_pos, 
            state.goal_pos, 
            state.ai_path, 
            state.ai_last_move_time, 
            state.ai_move_delay
        )
        #print(state.level)
        state.visited_cells.add(state.player_pos)
        
        # In compare_maze, modify the level transition:
        if len(state.ai_path) == 0:
            state.level += 1
            state.visited_cells = set()  # Reset properly
            state.player_pos = state.start_pos
            state.ai_path = []  # Clear old path