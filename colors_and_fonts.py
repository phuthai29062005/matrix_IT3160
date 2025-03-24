import os
import json
import pygame
import random

pygame.font.init()

# Đường dẫn thư mục assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
COLOR_FILE = os.path.join(ASSETS_DIR, "config", "colors.json")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
FONT_PATH = os.path.join(FONTS_DIR, "Tektur-Regular.ttf")

# Kiểm tra xem font có tồn tại không
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font file not found: {FONT_PATH}")

# Load font
font = pygame.font.Font(FONT_PATH, 36)
small_font = pygame.font.Font(FONT_PATH, 24)

# Đọc màu từ colors.json
if not os.path.exists(COLOR_FILE):
    raise FileNotFoundError(f"Color config file not found: {COLOR_FILE}")

with open(COLOR_FILE, "r") as file:
    colors = json.load(file)

# Lấy màu sắc từ JSON
index = random.randint(0, 3)
MATRIX_COLOR = tuple(colors["matrix_colors"][index])
BORDER_COLOR_PLAYER = tuple(colors["border_colors_player"][index])
BORDER_COLOR_AI = tuple(colors["border_colors_ai"][index])
PATH_COLOR = tuple(colors["path_colors"][index])

# Màu nền và chữ và vị trí đầu cuối
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
START_COLOR = (255, 165, 0)  # Màu cam
GOAL_COLOR = [139, 69, 19]  # Màu vàng


# Bảng điểm
POINT_COLORS = {
    -100: (255, 0, 0),
    100: (0, 255, 0),
    200: (255, 255, 0),
    500: (255, 192, 203),
}
