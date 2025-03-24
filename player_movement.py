import pygame
from colors_and_fonts import WHITE
import time

def move_player(keys, player_pos, maze, visited_cells, last_move_time, move_delay=0.15):
    """Tối ưu di chuyển bằng dictionary"""
    if time.time() - last_move_time < move_delay:
        return player_pos, last_move_time

    moves = {
        pygame.K_UP: (0, -1), pygame.K_w: (0, -1),
        pygame.K_DOWN: (0, 1), pygame.K_s: (0, 1),
        pygame.K_LEFT: (-1, 0), pygame.K_a: (-1, 0),
        pygame.K_RIGHT: (1, 0), pygame.K_d: (1, 0),
    }

    for key, (dx, dy) in moves.items():
        if keys[key]:  # Nếu phím được nhấn
            new_pos = (player_pos[0] + dx, player_pos[1] + dy)
            if 0 <= new_pos[0] < len(maze) and 0 <= new_pos[1] < len(maze[0]) and maze[new_pos[0]][new_pos[1]] == 0:
                visited_cells.add(new_pos)
                return new_pos, time.time()

    return player_pos, last_move_time
