import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Thiết lập kích thước cửa sổ
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

# Định nghĩa màu sắc theo chủ đề mê cung
BG_COLOR = (30, 35, 111)      # Nền menu: xanh tím tối
GAME_BG_COLOR = (20, 20, 60)   # Nền game: xanh đậm
BTN_COLOR = (65, 105, 225)    # Nút Play: xanh dương
BTN_HOVER = (0, 255, 0)       # Màu khi hover: xanh neon
BTN_BORDER = (0, 255, 0)      # Viền nút: xanh neon
TEXT_COLOR = (240, 240, 240)  # Chữ: trắng nhạt

# Khởi tạo font
font = pygame.font.SysFont(None, 48)

# Tạo nút Play ở giữa màn hình
button_rect = pygame.Rect((WIDTH - 150) // 2, (HEIGHT - 75) // 2, 150, 75)

# Trạng thái hiện tại: MENU hoặc GAME
state = 'MENU'

clock = pygame.time.Clock()

# Hàm vẽ menu chính
def draw_menu():
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()
    # Màu nút khi hover
    color = BTN_HOVER if button_rect.collidepoint(mouse_pos) else BTN_COLOR
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, BTN_BORDER, button_rect, 3)
    text_surface = font.render("PLAY", True, TEXT_COLOR)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)

# Hàm vẽ gameloop (tạm placeholder)
def draw_game():
    screen.fill(GAME_BG_COLOR)
    # TODO: vẽ mê cung và logic game ở đây
    info = font.render("Game Screen - ESC to Menu", True, TEXT_COLOR)
    info_rect = info.get_rect(center=(WIDTH//2, 30))
    screen.blit(info, info_rect)

# Vòng lặp chính
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif state == 'MENU':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    # Chuyển sang màn hình game
                    state = 'GAME'
        elif state == 'GAME':
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Trở về menu chính
                state = 'MENU'

    # Vẽ theo trạng thái
    if state == 'MENU':
        draw_menu()
    elif state == 'GAME':
        draw_game()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
