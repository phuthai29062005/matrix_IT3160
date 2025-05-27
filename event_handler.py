import pygame

# Hàm xử lý sự kiện người dùng (nhấn phím ESC để thoát, SPACE để chuyển level)
def handle_events(state):
    events = pygame.event.get()  # Lưu sự kiện vào biến
    for event in events:
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            if event.key == pygame.K_SPACE and state.player_pos == state.goal_pos:
                if state.score >= state.target_score:
                    if state.current_level < 3:
                        state.read_map = False
                        state.ai_move_delay -= 0.05
                        state.current_level += 1
                        state.load_level()
                    else:
                        state.win = True
    return events  # Trả về sự kiện thay vì "continue"
