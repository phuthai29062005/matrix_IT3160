import time
from player_movement import move_player
from maze_generation import find_shortest_path
from Hill_Climbing_With_Astar import *
from Simulated_Annealing_With_Astar import *
from Genetic_Algorithm_With_Astar import *

# Hàm cập nhật di chuyển của người chơi
def update_player(state, keys):
    current_time = time.time()  # Lấy thời gian hiện tại
    # Kiểm tra xem có đến thời gian di chuyển tiếp theo không
    if current_time - state.last_move_time > state.move_delay:
        state.last_player_pos = state.player_pos  # Lưu lại vị trí người chơi trước đó
        # Di chuyển người chơi, cập nhật thời gian và điểm số
        new_pos, state.last_move_time = move_player(keys, state.player_pos, state.maze, state.visited_cells, state.last_move_time)
        state.score += state.scattered_points.pop(new_pos, 0)  # Cộng điểm nếu người chơi thu thập được điểm
        state.player_pos = new_pos  # Cập nhật vị trí người chơi

def move_ai(maze, ai_pos, goal_pos, ai_path, last_move_time, move_delay):
    current_time = time.time()
    
    # Kiểm tra thời gian và đường đi hợp lệ
    if current_time - last_move_time > move_delay and ai_path:
        next_pos = ai_path.pop(0)
        # Kiểm tra xem bước tiếp theo có hợp lệ không
        if maze[next_pos[0]][next_pos[1]] == 0:
            ai_pos = next_pos
            last_move_time = current_time

    return ai_pos, last_move_time

def update_ai(state):
    # Nếu không có đường đi hoặc đã đi hết đường đi
    if not state.ai_path or state.ai_pos == state.goal_pos:
        # Tìm đường đi mới
        checkpoints = list(state.ai_scattered_points.keys())  # Get the coordinates (x,y) tuples
        if state.current_level == 1:    
            state.ai_path = hill_climbing_Astar(state.maze, state.ai_pos, state.goal_pos, checkpoints)
        elif state.current_level == 2:
            state.ai_path = ga_Astar(state.maze, state.ai_pos, state.goal_pos, checkpoints)
        elif state.current_level == 3:
            state.ai_path = simulated_annealing_Astar(state.maze, state.ai_pos, state.goal_pos, checkpoints)
    # Di chuyển AI
    state.ai_pos, state.ai_last_move_time = move_ai(
        state.maze, 
        state.ai_pos, 
        state.goal_pos, 
        state.ai_path, 
        state.ai_last_move_time, 
        state.ai_move_delay
    )
    
    # Thêm vị trí hiện tại vào danh sách đã đi qua
    state.visited_ai_cells.add(state.ai_pos)