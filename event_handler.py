import pygame

# Hàm xử lý sự kiện người dùng (nhấn phím ESC để thoát, SPACE để chuyển level)
def handle_events(state):
    for event in pygame.event.get():  # Lặp qua các sự kiện
        # Nếu nhấn ESC hoặc đóng cửa sổ, thoát game
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            return False

        # Nếu nhấn SPACE và người chơi đã tới mục tiêu, chuyển sang level tiếp theo
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and state.player_pos == state.goal_pos:
            if state.score >= state.target_score:
                if state.current_level < 3:
                    state.read_map = False
                    state.ai_move_delay -= 0.05
                    state.current_level += 1  # Chuyển level
                    state.load_level()  # Load level mới
                else:
                    state.win = True  # Nếu thắng ở level cuối cùng
    return True  # Quay lại vòng lặp game nếu game chưa kết thúc
