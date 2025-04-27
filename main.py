import pygame
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
    play = True
    state = GameState()  # Khởi tạo trạng thái game
    running = True
    # Vòng lặp chính của game
    while running:

        clock.tick(30)  # Đặt FPS cho game (30 FPS)
        blink_state = (pygame.time.get_ticks() // 500) % 2  # Định kỳ cập nhật trạng thái nhấp nháy
        if play == True:
            running = handle_events(state)  # Xử lý sự kiện từ người dùng
            keys = pygame.key.get_pressed()  # Lấy trạng thái phím
            update_player(state, keys)  # Cập nhật di chuyển người chơi
            update_ai(state)  # Cập nhật di chuyển AI
            draw_everything(screen, state, blink_state)  # Vẽ mọi thứ lên màn hình
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        maze = generate_maze()
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            screen.fill(BLACK)
            draw_maze_AI(screen, state.maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)
        pygame.display.flip()  # Cập nhật màn hình
    

    pygame.quit()  # Thoát game

if __name__ == "__main__":
    main()  # Chạy game khi chương trình được chạy


