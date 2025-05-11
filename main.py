import pygame
import time
import json
import os
from maze_generation import *
from ui import *
from colors_and_fonts import BLACK
from player_movement import move_player
from Easy import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Đọc target_scores từ JSON chỉ một lần
with open(os.path.join("assets", "config", "points.json"), "r") as file:
    points_data = json.load(file)
TARGET_SCORES = points_data["target_scores"]

TOTAL_LEVELS = 5
FONT = pygame.font.Font("assets/fonts/Tektur-Regular.ttf", 36)

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
            draw_comments(screen)
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

def main():
    running = True
    win = False  
    current_level = 1

    levels = [generate_maze() for _ in range(TOTAL_LEVELS)]
    start_goal_pairs = [find_start_end(maze, i + 1) for i, maze in enumerate(levels)]

    scattered_points_list = [
        scatter_points(levels[i], *start_goal_pairs[i], i + 1, TARGET_SCORES[str(i + 1)])
        for i in range(TOTAL_LEVELS)
    ]

    maze = levels[current_level - 1]
    start_pos, goal_pos = start_goal_pairs[current_level - 1]
    target_score = TARGET_SCORES[str(current_level)]
    scattered_points, ai_scattered_points = scattered_points_list[current_level - 1]

    score = 0  
    player_pos = start_pos
    last_player_pos = start_pos  
    visited_cells = set()
    
    move_delay = 0.05  
    last_move_time = time.time()

    countdown(screen, 6, centered=True)  # Hiển thị giữa màn hình lúc vào game
    countdown(screen, 5, maze=maze, start_pos=start_pos, goal_pos=goal_pos, scattered_points=scattered_points, ai_scattered_points=ai_scattered_points, score=score, target_score=target_score)  # Hiển thị góc phải khi xem map
    
    while running:
        screen.fill(BLACK)
        clock.tick(30)
        blink_state = (pygame.time.get_ticks() // 500) % 2  # Cập nhật trạng thái nhấp nháy mỗi 500ms

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and player_pos == goal_pos:
                if score >= target_score and current_level <= TOTAL_LEVELS:
                    current_level += 1
                    maze = levels[current_level - 1]  
                    start_pos, goal_pos = start_goal_pairs[current_level - 1]  
                    scattered_points, ai_scattered_points = scattered_points_list[current_level - 1]
                    target_score = TARGET_SCORES[str(current_level)]
                    player_pos = start_pos  
                    last_player_pos = start_pos  
                    visited_cells = set()
                    score = 0
                    countdown(screen, 10, maze=maze, start_pos=start_pos, goal_pos=goal_pos, scattered_points=scattered_points, ai_scattered_points=ai_scattered_points, score=score, target_score=target_score)  # Đếm ngược góc phải trước level mới

        keys = pygame.key.get_pressed()
        current_time = time.time()
        if current_time - last_move_time > move_delay:
            last_player_pos = player_pos  
            new_player_pos, last_move_time = move_player(keys, player_pos, maze, visited_cells, last_move_time)
            score += scattered_points.pop(new_player_pos, 0)
            player_pos = new_player_pos  

        draw_headings(screen)
        draw_comments(screen)
        draw_maze(screen, maze, PLAYER_POS, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER, start_pos, goal_pos, player_pos, last_player_pos, visited_cells, scattered_points, blink_state)
        BFS_solve(screen, maze, player_pos, goal_pos, scattered_points, player_pos, BORDER_COLOR_PLAYER, CELL_SIZE_PLAYER)
        draw_score(screen, score, target_score)
        draw_exit_message(screen)
        
        if player_pos == goal_pos:
            if score >= target_score:
                if current_level == 5:
                    win = True
                else:
                    draw_next_level_message(screen, current_level)
            else:
                draw_not_enough(screen)
            
        if win:
            draw_you_win(screen)
            
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()