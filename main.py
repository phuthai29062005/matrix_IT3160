import pygame
import copy
from game_state import GameState  # Import GameState chứa toàn bộ trạng thái game
from event_handler import handle_events  # Xử lý sự kiện (nhấn phím)
from game_logic import update_player, update_ai  # Cập nhật di chuyển của người chơi và AI
from draw_manager import draw_everything  # Vẽ các thành phần lên màn hình
from ui import *
from maze_generation import *
from colors_and_fonts import BLACK
from player_movement import move_player
from Easy import *


pygame.init()  # Khởi tạo Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)  # Thiết lập cửa sổ game ở chế độ full screen
clock = pygame.time.Clock()  # Tạo đối tượng clock để điều khiển FPS

def main():
    play = False
    state = GameState()
    running = True
    maze = None
    start_pos = None
    end_pos = None
    generate = False
    while running:
        clock.tick(30)
        blink_state = (pygame.time.get_ticks() // 500) % 2

        if play:
            running = handle_events(state)
            keys = pygame.key.get_pressed()
            update_player(state, keys)
            update_ai(state)
            draw_everything(screen, state, blink_state)
        else:
          
            if generate == False:
                state.reset()
                state.maze = generate_maze()
                generate = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
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
                                maze_copy_for_bfs = copy.deepcopy(state.maze)
                                maze_copy_for_dfs = copy.deepcopy(state.maze)

                                BFS_path = BFS_solve(screen, maze_copy_for_bfs, state.start_pos, state.goal_pos, None, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)
                                DFS_path = DFS_solve(screen, maze_copy_for_dfs, state.start_pos, state.goal_pos, None, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)
                        
            screen.fill(BLACK)
            
            if state.maze is not None:
                draw_maze_AI(screen, state.maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)
            
        pygame.display.flip()

    pygame.quit()
 

if __name__ == "__main__":
    main()  # Chạy game khi chương trình được chạy


