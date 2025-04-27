from ui import *
from colors_and_fonts import BLACK

# Hàm vẽ tất cả các thành phần của game lên màn hình
def draw_everything(screen, state, blink_state):
    screen.fill(BLACK)  # Đặt nền đen

    draw_headings(screen)  # Vẽ tiêu đề game

    # Vẽ ma trận của người chơi (chưa sử dụng)
    draw_maze(screen, state.maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER, state.start_pos, state.goal_pos, state.player_pos, state.last_player_pos, state.visited_cells, state.scattered_points, blink_state)

    # Vẽ ma trận của AI (chưa sử dụng)
    draw_maze(screen, state.maze, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, state.start_pos, state.goal_pos, state.start_pos, state.last_ai_pos, state.visited_ai_cells, state.ai_scattered_points, blink_state)

    draw_exit_message(screen)  # Vẽ thông báo thoát
    draw_score(screen, state.score, state.target_score)  # Vẽ điểm số và điểm mục tiêu

    # Nếu người chơi đến được mục tiêu
    if state.player_pos == state.goal_pos:
        if state.score >= state.target_score:
            if state.current_level == 3:
                state.win = True  # Nếu là level cuối, người chơi thắng
            else:
                draw_next_level_message(screen, state.current_level)  # Chuyển sang level mới
        else:
            draw_not_enough(screen)  # Hiển thị nếu người chơi chưa đủ điểm

    if state.win:
        draw_you_win(screen)  # Hiển thị thông báo thắng game
