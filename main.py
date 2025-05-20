import pygame
import copy
from game_state import GameState  # Import GameState chứa toàn bộ trạng thái game
from event_handler import handle_events  # Xử lý sự kiện (nhấn phím)
from game_logic import update_player, update_ai  # Cập nhật di chuyển của người chơi và AI
from draw_manager import *  # Vẽ các thành phần lên màn hình
from ui import *
from maze_generation import *
from colors_and_fonts import BLACK
from player_movement import move_player
from Find_Single_Path import *
from compare import *
from Hill_Climbing_With_Astar import *

pygame.init()  # Khởi tạo Pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)  # Thiết lập cửa sổ game ở chế độ full screen
clock = pygame.time.Clock()  # Tạo đối tượng clock để điều khiển FPS

def main():
    play = True
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
            draw_everything_true(screen, state, blink_state)
        else:
          
            if generate == False:
                state.reset()
                state.maze = generate_maze()
                generate = True
            
            choose_position(screen, state)                  
            screen.fill(BLACK)
            
            if state.maze is not None:
                draw_maze_AI(screen, state.maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)

            draw_everything_false(screen, state)
        pygame.display.flip()

    pygame.quit()
 

if __name__ == "__main__":
    main()  # Chạy game khi chương trình được chạy


