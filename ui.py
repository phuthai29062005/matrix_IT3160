import pygame
import time
from colors_and_fonts import *

import math
pygame.init()

FONT = pygame.font.Font("assets/fonts/Tektur-Regular.ttf", 36)
clock = pygame.time.Clock()

# Kích thước ô cho người chơi và AI
GRID_SIZE = 70
CELL_SIZE_PLAYER = 13
CELL_SIZE_AI = 9.5

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
BORDER_WIDTH = 10
GAP_BETWEEN_MATRICES = 30
COMMENT_HEIGHT = 120
HEADING_GAP = 80

TOTAL_WIDTH = MATRIX_WIDTH_PLAYER + MATRIX_WIDTH_AI + 2 * BORDER_WIDTH + GAP_BETWEEN_MATRICES
START_X = (SCREEN_WIDTH - TOTAL_WIDTH) // 2
START_Y = (SCREEN_HEIGHT - MATRIX_HEIGHT_PLAYER - 2 * BORDER_WIDTH - COMMENT_HEIGHT) // 2 + HEADING_GAP

PLAYER_POS = (START_X, START_Y)
AI_POS = (START_X + MATRIX_WIDTH_PLAYER + 2 * BORDER_WIDTH + GAP_BETWEEN_MATRICES, 
          START_Y + (MATRIX_HEIGHT_PLAYER - MATRIX_HEIGHT_AI) // 2 + 20)

BLINK_INTERVAL = 500  # Nhấp nháy mỗi 500ms

font_large = pygame.font.SysFont("arial", 40, bold=True)
font_small = pygame.font.SysFont("arial", 14)
                                 
def draw_countdown_corner(screen, remaining_time, font, screen_width, screen_height):
    """Vẽ thời gian đếm ngược ở góc phải dưới màn hình"""
    countdown_text = font.render(f"Time: {remaining_time}s", True, (255, 255, 255))
    screen.blit(countdown_text, (screen_width - 170, screen_height - 50))

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
            elif visited_cells is not None and (x, y) in visited_cells:
                color = WHITE  # Đường đã đi
            else:
                color = PATH_COLOR  # Đường đi

            # Vẽ ô vuông cho mê cung
            pygame.draw.rect(screen, color, cell_rect)

            # Nếu ô này chứa điểm, vẽ điểm lên trên
            if scattered_points is not None and (x, y) in scattered_points:
                point_value = scattered_points[(x, y)]
                point_color = POINT_COLORS.get(point_value, (255, 255, 255))

                cx = cell_rect[0] + cell_size // 2  # Tọa độ trung tâm x
                cy = cell_rect[1] + cell_size // 2  # Tọa độ trung tâm y
                r = int(cell_size * 0.45)           # Độ dài từ tâm đến đỉnh

                # Tọa độ 4 đỉnh hình kim cương (trên, phải, dưới, trái)
                diamond_points = [
                    (cx, cy - r),  # Đỉnh trên
                    (cx + r, cy),  # Đỉnh phải
                    (cx, cy + r),  # Đỉnh dưới
                    (cx - r, cy)   # Đỉnh trái
                ]

                pygame.draw.polygon(screen, point_color, diamond_points)

def draw_maze_AI(screen, maze, pos, border_color, cell_size, scattered_points):
    x_offset, y_offset = pos
    pygame.draw.rect(screen, border_color,
                     (x_offset - BORDER_WIDTH, y_offset - BORDER_WIDTH,
                      GRID_SIZE * cell_size + 2 * BORDER_WIDTH, GRID_SIZE * cell_size + 2 * BORDER_WIDTH))

    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            cell_rect = (x_offset + x * cell_size, y_offset + y * cell_size, cell_size, cell_size)

            if maze[x][y] == 1:
                color = MATRIX_COLOR
            else:
                color = PATH_COLOR

            # Vẽ ô vuông cho mê cung
            pygame.draw.rect(screen, color, cell_rect)
            
            if scattered_points is not None and (x, y) in scattered_points:
                point_value = scattered_points[(x, y)]
                point_color = POINT_COLORS.get(point_value, (255, 255, 255))

                cx = cell_rect[0] + cell_size // 2  # Tọa độ trung tâm x
                cy = cell_rect[1] + cell_size // 2  # Tọa độ trung tâm y
                r = int(cell_size * 0.45)           # Độ dài từ tâm đến đỉnh

                # Tọa độ 4 đỉnh hình kim cương (trên, phải, dưới, trái)
                diamond_points = [
                    (cx, cy - r),  # Đỉnh trên
                    (cx + r, cy),  # Đỉnh phải
                    (cx, cy + r),  # Đỉnh dưới
                    (cx - r, cy)   # Đỉnh trái
                ]

                pygame.draw.polygon(screen, point_color, diamond_points)

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

def countdown(screen, duration, centered=False, maze=None, start_pos=None, goal_pos=None, scattered_points=None, ai_scattered_points=None, score=None, target_score=None):
    """Hàm chung cho đếm ngược trước khi chơi."""
    start_time = time.time()
    
    while time.time() - start_time < duration:
        remaining_time = int(duration - (time.time() - start_time))
        blink_state = (pygame.time.get_ticks() // 500) % 2  # Trạng thái nhấp nháy

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()

        screen.fill(BLACK)
        
        if maze is not None:  # Nếu có bản đồ, hiển thị bản đồ
            draw_headings(screen)
            draw_maze(screen, maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER, start_pos, goal_pos, start_pos, start_pos, set(), scattered_points, blink_state)
            draw_maze(screen, maze, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, start_pos, goal_pos, start_pos, start_pos, set(), ai_scattered_points, blink_state)
            draw_score(screen, score, target_score)
            
            # Đếm ngược góc phải dưới khi xem bản đồ
            countdown_text = FONT.render(f"Time: {remaining_time}s", True, (255, 255, 255))
            screen.blit(countdown_text, (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 50))
        
        if centered:  # Nếu cần hiển thị ở giữa màn hình
            draw_text(screen, str(remaining_time), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 80)

        pygame.display.flip()
        clock.tick(30)
    
    if centered:
        screen.fill(BLACK)
        draw_text(screen, "START!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 80)
        pygame.display.flip()
        time.sleep(1)

def draw_next_level_message(screen, current_level):
    """Hiển thị thông báo khi hoàn thành level"""
    text = f"Level {current_level} Complete! Press SPACE for Next"
    draw_text(screen, text, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 30)


def draw_time(screen, algorithm, time, path, x, y, font_size=30):
    """Hiển thị thời gian thực hiện thuật toán tại vị trí (x, y)"""
    if time != 0:
        text = f"{algorithm}: {time:.8f}s {path}"
    else:
        text = f"{algorithm}: {path}"
    text_surface = pygame.font.Font(FONT_PATH, font_size).render(text, True, WHITE)
    screen.blit(text_surface, (x, y))


class Button:
    def __init__(self, text, x, y, w, h, callback, color=LIGHT_BLUE, hover_color=BLUE, text_color=WHITE, shadow=True):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.callback = callback
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.shadow = shadow
        self.click_effect = False
        self.click_time = 0
        self.border_radius = 15
        self.glow = 0
        
    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        
        if is_hover:
            self.glow = min(self.glow + 0.2, 10)
        else:
            self.glow = max(self.glow - 0.2, 0)
            
        click_offset = 0
        if self.click_effect:
            click_offset = 3
            if pygame.time.get_ticks() - self.click_time > 100:
                self.click_effect = False

        if self.shadow:
            shadow_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5 + click_offset, self.rect.width, self.rect.height)
            pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect, border_radius=self.border_radius)

        current_color = self.hover_color if is_hover else self.color
        if self.click_effect:
            current_color = pygame.Color(*current_color).lerp(WHITE, 0.3)

        pygame.draw.rect(screen, current_color, pygame.Rect(
            self.rect.x, self.rect.y + click_offset, self.rect.width, self.rect.height), border_radius=self.border_radius)

        border_color = pygame.Color(*current_color).lerp(WHITE, 0.7)
        pygame.draw.rect(screen, border_color, pygame.Rect(
            self.rect.x, self.rect.y + click_offset, self.rect.width, self.rect.height), 2, self.border_radius)

        if self.glow > 0:
            glow_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            glow_color = (*current_color[:3], int(self.glow * 10))
            pygame.draw.rect(glow_surf, glow_color, (0, 0, self.rect.width, self.rect.height), border_radius=self.border_radius)
            screen.blit(glow_surf, (self.rect.x, self.rect.y + click_offset))

        text_surf = font_large.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=(self.rect.centerx, self.rect.centery + click_offset))
        text_shadow = font_large.render(self.text, True, (0, 0, 0, 100))
        screen.blit(text_shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(text_surf, text_rect)

        if is_hover:
            pygame.draw.circle(screen, WHITE, (self.rect.left + 20, self.rect.centery + click_offset), 3)
            pygame.draw.circle(screen, WHITE, (self.rect.right - 20, self.rect.centery + click_offset), 3)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.click_effect = True
                self.click_time = pygame.time.get_ticks()
                self.callback()

def draw_path(screen, path, color):
    """Vẽ đường đi dạng các chấm tròn nối liền nhau"""
    if not path:
        return
    
    # Vẽ từng điểm trên path
    for i in range(len(path) - 1):
        x1 = path[i][1] * CELL_SIZE_PLAYER + PLAYER_POS[0] + CELL_SIZE_PLAYER // 2
        y1 = path[i][0] * CELL_SIZE_PLAYER + PLAYER_POS[1] + CELL_SIZE_PLAYER // 2
        x2 = path[i+1][1] * CELL_SIZE_PLAYER + PLAYER_POS[0] + CELL_SIZE_PLAYER // 2
        y2 = path[i+1][0] * CELL_SIZE_PLAYER + PLAYER_POS[1] + CELL_SIZE_PLAYER // 2
        
        # Vẽ đường nối giữa các điểm
        pygame.draw.line(screen, color, (x1, y1), (x2, y2), 3)
        
        # Vẽ chấm tròn tại mỗi điểm
        pygame.draw.circle(screen, color, (x1, y1), 4)
    
    # Vẽ điểm cuối cùng
    last_x = path[-1][1] * CELL_SIZE_PLAYER + PLAYER_POS[0] + CELL_SIZE_PLAYER // 2
    last_y = path[-1][0] * CELL_SIZE_PLAYER + PLAYER_POS[1] + CELL_SIZE_PLAYER // 2
    pygame.draw.circle(screen, color, (last_x, last_y), 4)