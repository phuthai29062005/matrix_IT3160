import pygame
import sys
import os
from ui import *
from colors_and_fonts import *

pygame.init()

# Kích thước màn hình
INFO = pygame.display.Info()
SCREEN_WIDTH = INFO.current_w
SCREEN_HEIGHT = INFO.current_h

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Màn hình mở đầu")

# Lấy đường dẫn thư mục chứa file hiện tại
current_dir = os.path.dirname(__file__)  # thư mục của screen.py

# Ghép đường dẫn ảnh tương đối với thư mục hiện tại
image_path = os.path.join(current_dir, "assets", "image", "ma trận.jpg")

# Load ảnh
background = pygame.image.load(image_path)
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Đường dẫn assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
FONT_PATH = os.path.join(ASSETS_DIR, "fonts", "Tektur-Regular.ttf")

# Font
title_font = pygame.font.Font(FONT_PATH, 60)

# Biến chế độ
selected_mode = None

def play_game():
    global selected_mode
    selected_mode = "play"

def compare_mode():
    global selected_mode
    selected_mode = "compare"
    
def compare_ai_mode():
    global selected_mode
    selected_mode = "compare_ai"

def show_intro():
    print("Giới thiệu trò chơi: MATRIX MAZE - IT3160")

buttons = [
    
    Button("Compare", SCREEN_WIDTH//2 - 150, 200, 300, 70, compare_mode, color=LIGHT_BLUE, hover_color=BLUE),
    Button("Compare_AI", SCREEN_WIDTH//2 - 150, 300, 300, 70, compare_ai_mode, color=LIGHT_PURPLE, hover_color=PURPLE),
    Button("Play", SCREEN_WIDTH//2 - 150, 400, 300, 70, play_game, color=LIGHT_GREEN, hover_color=GREEN),  
]

title_text = title_font.render("MATRIX MAZE - IT3160", True, WHITE)
title_shadow = title_font.render("MATRIX MAZE - IT3160", True, (50, 50, 50))

def show_main_menu():
    global selected_mode
    selected_mode = None
    running = True
    while running:
        screen.blit(background, (0, 0))
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title_shadow.get_width()//2 + 3, 80 + 3))
        screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 80))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "play"
                elif event.key == pygame.K_2:
                    return "compare"
                elif event.key == pygame.K_ESCAPE:
                    return "quit"
            for button in buttons:
                button.check_click(event)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()

        if selected_mode is not None:
            return selected_mode
