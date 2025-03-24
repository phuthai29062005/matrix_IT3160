import pygame
import time
from colors_and_fonts import *

pygame.init()

# Kích thước ô cho người chơi và AI
GRID_SIZE = 70
CELL_SIZE_PLAYER = 12
CELL_SIZE_AI = 10

# Kích thước màn hình
INFO = pygame.display.Info()
SCREEN_WIDTH = INFO.current_w
SCREEN_HEIGHT = INFO.current_h

# Kích thước ma trận
MATRIX_WIDTH_PLAYER = GRID_SIZE * CELL_SIZE_PLAYER
MATRIX_HEIGHT_PLAYER = GRID_SIZE * CELL_SIZE_PLAYER

MATRIX_WIDTH_AI = GRID_SIZE * CELL_SIZE_AI
MATRIX_HEIGHT_AI = GRID_SIZE * CELL_SIZE_AI

# Khoảng cách và căn giữa
BORDER_WIDTH = 6
GAP_BETWEEN_MATRICES = 100
COMMENT_HEIGHT = 120
HEADING_GAP = 40

TOTAL_WIDTH = MATRIX_WIDTH_PLAYER + MATRIX_WIDTH_AI + 2 * BORDER_WIDTH + GAP_BETWEEN_MATRICES
START_X = (SCREEN_WIDTH - TOTAL_WIDTH) // 2
START_Y = (SCREEN_HEIGHT - MATRIX_HEIGHT_PLAYER - 2 * BORDER_WIDTH - COMMENT_HEIGHT) // 2 + HEADING_GAP

PLAYER_POS = (START_X, START_Y)
AI_POS = (START_X + MATRIX_WIDTH_PLAYER + 2 * BORDER_WIDTH + GAP_BETWEEN_MATRICES, 
          START_Y + (MATRIX_HEIGHT_PLAYER - MATRIX_HEIGHT_AI) // 2)

BLINK_INTERVAL = 500  # Nhấp nháy mỗi 500ms


def draw_countdown_corner(screen, remaining_time, font, screen_width, screen_height):
    """Vẽ thời gian đếm ngược ở góc phải dưới màn hình"""
    countdown_text = font.render(f"Time: {remaining_time}s", True, (255, 255, 255))
    screen.blit(countdown_text, (screen_width - 170, screen_height - 50))
    
def draw_countdown_and_start_center(screen, duration, font, screen_width, screen_height):
    """Hiển thị đếm ngược và chữ START! chính giữa màn hình"""
    start_time = time.time()

    while time.time() - start_time < duration:
        remaining_time = int(duration - (time.time() - start_time))

        # Xử lý sự kiện để không làm game bị đơ
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))  # Xóa màn hình trước khi vẽ lại
        countdown_text = font.render(str(remaining_time), True, (255, 255, 255))
        text_rect = countdown_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(countdown_text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  # Delay 1 giây để cập nhật countdown

    # Hiển thị chữ START! chính giữa màn hình trong 2 giây
    screen.fill((0, 0, 0))  # Xóa màn hình
    start_text = font.render("START!", True, (255, 255, 255))
    text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(start_text, text_rect)
    pygame.display.flip()
    time.sleep(1)  # Giữ "START!" trong 2 giây

def draw_countdown_and_start_corner(screen, duration, font, screen_width, screen_height, maze, start_pos, goal_pos, scattered_points, ai_scattered_points, score, target_score):
    """Vẽ đếm ngược & chữ 'START!' ở góc phải dưới màn hình"""
    start_time = time.time()

    while time.time() - start_time < duration:
        remaining_time = int(duration - (time.time() - start_time))

        # Xử lý sự kiện để không làm game bị đơ
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))  # Xóa màn hình trước khi vẽ lại
        draw_maze(screen, maze, (50, 50), (255, 255, 255), 10, start_pos, goal_pos, start_pos, start_pos, set(), scattered_points)  # Vẽ lại bản đồ
        draw_score(screen, score, target_score)  # Hiển thị điểm số

        draw_countdown_corner(screen, remaining_time, font, screen_width, screen_height)  # Hiển thị countdown
        pygame.display.flip()
        pygame.time.delay(1000)  # Delay 1 giây

    # **Sau khi đếm ngược kết thúc, vẽ lại bản đồ để giữ màn hình**
    screen.fill((0, 0, 0))  
    draw_maze(screen, maze, (50, 50), (255, 255, 255), 10, start_pos, goal_pos, start_pos, start_pos, set(), scattered_points)  # Vẽ lại bản đồ
    draw_score(screen, score, target_score)  # Hiển thị điểm số

    # **Hiển thị chữ "START!" mà không xóa màn hình**
    start_text = font.render("START!", True, (255, 255, 255))
    screen.blit(start_text, (screen_width - 120, screen_height - 100))
    pygame.display.flip()
    time.sleep(2)  # Giữ "START!" trong 2 giây

    # **Sau 2 giây, vẽ lại bản đồ để xóa chữ "START!"**
    screen.fill((0, 0, 0))  
    draw_maze(screen, maze, (50, 50), (255, 255, 255), 10, start_pos, goal_pos, start_pos, start_pos, set(), scattered_points)  # Vẽ lại bản đồ
    draw_score(screen, score, target_score)  # Hiển thị điểm số
    pygame.display.flip()


def draw_you_win(screen):
    """Hiển thị YOU WIN! nhấp nháy"""
    current_time = pygame.time.get_ticks()
    if (current_time // BLINK_INTERVAL) % 2 == 0:  # Nhấp nháy mỗi 500ms
        draw_text(screen, "YOU WIN!", screen.get_width() // 2, screen.get_height() // 2, 80)
        
def draw_maze(screen, maze, pos, border_color, cell_size, start, end, player_pos, last_player_pos, visited_cells, scattered_points, blink_state):
    """Vẽ mê cung, bao gồm vị trí người chơi, vị trí cuối cùng, tường, đường đi và điểm"""
    x_offset, y_offset = pos
    pygame.draw.rect(screen, border_color,
                     (x_offset - BORDER_WIDTH, y_offset - BORDER_WIDTH,
                      GRID_SIZE * cell_size + 2 * BORDER_WIDTH, GRID_SIZE * cell_size + 2 * BORDER_WIDTH))

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_rect = (x_offset + x * cell_size, y_offset + y * cell_size, cell_size, cell_size)

            # Xác định màu ô
            if (x, y) == start:
                color = START_COLOR if blink_state else MATRIX_COLOR  # **Nhấp nháy vị trí bắt đầu**
            elif (x, y) == end:
                color = GOAL_COLOR if blink_state else PATH_COLOR  # **Nhấp nháy vị trí đích**
            elif maze[x][y] == 1:
                color = MATRIX_COLOR  # Tường
            elif (x, y) == player_pos:
                color = (255, 0, 0) if blink_state else PATH_COLOR  # Nhấp nháy vị trí người chơi
            elif (x, y) == last_player_pos:
                color = (0, 255, 255) if blink_state else PATH_COLOR  # Nhấp nháy vị trí cuối cùng
            elif (x, y) in visited_cells:
                color = WHITE  # Đường đã đi
            else:
                color = PATH_COLOR  # Đường đi

            # Vẽ ô vuông cho mê cung
            pygame.draw.rect(screen, color, cell_rect)

            # Nếu ô này chứa điểm, vẽ điểm lên trên
            if (x, y) in scattered_points:
                point_value = scattered_points[(x, y)]
                point_color = POINT_COLORS.get(point_value, (255, 255, 255))
                pygame.draw.circle(screen, point_color,
                                   (cell_rect[0] + cell_size // 2, cell_rect[1] + cell_size // 2),
                                   int(cell_size * 0.45))  # Kích thước điểm


def draw_text(screen, text, x, y, font_size=36):
    """Vẽ chữ"""
    text_surface = pygame.font.Font(FONT_PATH, font_size).render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_headings(screen):
    """Vẽ tiêu đề PLAYER và AI"""
    human_x = PLAYER_POS[0] + MATRIX_WIDTH_PLAYER // 2
    ai_x = AI_POS[0] + MATRIX_WIDTH_AI // 2
    heading_human = START_Y - 30
    heading_ai = START_Y + 110
    draw_text(screen, "PLAYER", human_x, heading_human)
    draw_text(screen, "AI", ai_x, heading_ai)

def draw_comments(screen):
    """Vẽ chú thích điểm"""
    x_offset = START_X
    y_offset = SCREEN_HEIGHT - COMMENT_HEIGHT + 40
    for i, (points, color) in enumerate(POINT_COLORS.items()):
        text = small_font.render(f"{points}", True, WHITE)
        screen.blit(text, (x_offset, y_offset))
        pygame.draw.rect(screen, color, (x_offset + 60, y_offset + 8, 20, 20))
        x_offset += 100

def draw_next_level_message(screen, current_level):
    """Hiển thị thông báo khi hoàn thành level"""
    text = f"Level {current_level} Complete! Press SPACE for Next"
    draw_text(screen, text, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 30)

def draw_exit_message(screen):
    """Hiển thị thông báo thoát game"""
    draw_text(screen, "Press ESC to exit", 100, 30, 20)
    
def draw_score(screen, score, target_score):
    """Hiển thị điểm số"""
    text = f"Score: {score} / {target_score}"
    draw_text(screen, text, SCREEN_WIDTH - 300, 50, 30)
    
def draw_not_enough(screen):
    """Hiển thị thông báo không đủ điểm"""
    text = f"Score is not enough!!!"
    draw_text(screen, text, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 30)
