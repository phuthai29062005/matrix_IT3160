import time
from maze_generation import generate_maze, find_start_end, random_points
import json
import os

TOTAL_LEVELS = 3

with open(os.path.join("assets", "config", "points.json"), "r") as file:
    points_data = json.load(file)
TARGET_SCORES = points_data["target_scores"]

class GameState:
    def __init__(self):
        #khởi tạo ma trận, đầu cuối, rải điểm
        self.levels = [generate_maze() for _ in range(TOTAL_LEVELS)]
        self.start_goal_pairs = [find_start_end(maze, i + 1) for i, maze in enumerate(self.levels)]
        self.scattered_points_list = [
            random_points(self.levels[i], *self.start_goal_pairs[i], i + 1)
            for i in range(TOTAL_LEVELS)
        ]
        self.current_level = 1
        self.win = False
        self.read_map = False
        self.load_level()

        self.bfs_time = None
        self.dfs_time = None
        self.greedy_time = None
        self.Astar_time = None
        self.bfs_path = 0
        self.dfs_path = 0
        self.greedy_path = 0
        self.Astar_path = 0

    def reset(self):
        self.maze = None
        self.start_pos = None
        self.goal_pos = None
        self.scattered_points = []
        self.ai_scattered_points = []
        self.collected_points = 0
        self.ai_collected_points = 0
        self.current_level = 0
        self.target_score = 0
        self.player_pos = None
        self.ai_pos = None
    
    def reset_game(self):
        """Reset toàn bộ trạng thái game khi quay về menu"""
        self.__init__()  # Gọi lại hàm khởi tạo ban đầu

    def load_level(self):
        # Load dữ liệu cho level hiện tại
        idx = self.current_level - 1
        self.maze = self.levels[idx]
        self.start_pos, self.goal_pos = self.start_goal_pairs[idx]
        self.scattered_points, self.ai_scattered_points = self.scattered_points_list[idx]
        self.target_score = TARGET_SCORES[str(self.current_level)]

        #khởi tạo vị trí của người chơi và ai
        self.player_pos = self.start_pos
        self.last_player_pos = self.start_pos
        self.visited_cells = set()
        self.score = 0

        self.ai_pos = self.start_pos
        self.last_ai_pos = self.start_pos
        self.visited_ai_cells = set()
        self.ai_path = []

        self.last_move_time = time.time()
        self.move_delay = 0.05
        self.ai_last_move_time = time.time()
        self.ai_move_delay = 0.3