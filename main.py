import pygame
from game_state import GameState
from event_handler import handle_events
from game_logic import update_player, update_ai
from draw_manager import *
from ui import *
from maze_generation import *
from colors_and_fonts import BLACK
from player_movement import move_player
from compare import *
from Hill_Climbing_With_Astar import *
from screen import show_main_menu

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

def play_game():
    state = GameState()
    running = True

    while running:
        clock.tick(30)
        blink_state = (pygame.time.get_ticks() // 500) % 2

        events = handle_events(state)
        if events == "quit":
            return "quit"
        elif events == "menu":
            return "menu"

        keys = pygame.key.get_pressed()
        update_player(state, keys)
        update_ai(state)
        draw_everything_true(screen, state, blink_state)
        pygame.display.flip()


def compare_mode():
    state = GameState()
    running = True
    generate = False

    while running:
        clock.tick(30)
        blink_state = (pygame.time.get_ticks() // 500) % 2
  
        if not generate:
            state.reset()
            state.maze = generate_maze()
            generate = True
        
        events = handle_events(state)  
        if events == "quit":
            return "quit"
        elif events == "menu":
            return "menu"
        else:
            choose_position(screen, state, events)
        screen.fill(BLACK)

        if state.maze is not None:
            draw_maze_AI(screen, state.maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER, None)

        draw_everything_false(screen, state)
        pygame.display.flip()  # Đã di chuyển lên trước khi kiểm tra sự kiện lần 2

def compare_ai_mode():
    state = GameState()
    running = True
    state.current_level = 2
    state.load_level()  # Tải dữ liệu level 2
       
    while running:
        state.ai_move_delay = 0.0005
        clock.tick(30)
        blink_state = (pygame.time.get_ticks() // 500) % 2
        if state.visited_cells is None:
            draw_maze(screen, state.maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER, state.start_pos, state.goal_pos, state.start_pos, state.start_pos, state.visited_cells, state.scattered_points, blink_state)
            
        events = handle_events(state)  
        if events == "quit":
            return "quit"
        elif events == "menu":
            return "menu"

        screen.fill(BLACK)
        
        #draw_maze(screen, state.maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER, state.start_pos, state.goal_pos, state.player_pos, state.last_player_pos, state.visited_cells, state.scattered_points, blink_state)
        if state.level <= 3:
            compare_maze(screen, state)
        draw_maze(screen, state.maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER, state.start_pos, state.goal_pos, state.player_pos, state.last_player_pos, state.visited_cells, state.scattered_points, blink_state)

        draw_everything_false(screen, state)

        
        #draw_everything_false(screen, state)
        pygame.display.flip()  # Đã di chuyển lên trước khi kiểm tra sự kiện lần 2

def main():
    while True:
        mode = show_main_menu()  # Hiện menu

        if mode == "play":
            result = play_game()
        elif mode == "compare":
            result = compare_mode()
        elif mode == "compare_ai":
            result = compare_ai_mode()
        else:
            break  # Nhấn ESC trong menu chính để thoát
        
        if result == "quit":
            break  # ESC ở ngoài game -> thoát hẳn
        # Nếu result == "menu" thì vòng lặp tiếp tục và gọi lại show_main_menu()


if __name__ == "__main__":
    main()
    pygame.quit()  