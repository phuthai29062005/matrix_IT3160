# Matrix Game - IT3160 🎮

## Giới thiệu 📜
Matrix Game là một trò chơi giải mê cung có 2 chế độ được phát triển bằng Python và Pygame.
Chế độ 1:
    - Người chơi sẽ thi đấu với AI.
    - Người chơi sẽ điều khiển nhân vật di chuyển trong mê cung và thu thập điểm.
Chế độ 2: 
    - So sánh thời gian các thuật toán cơ bản chạy trong mê cung (bfs, dfs, greedy, astar)
## Cấu trúc dự án 📂

### `main.py`
    - Chứa vòng lặp chính của game.

### `maze_generation.py`
    - Tạo mê cung bằng thuật toán Recursive Backtracking.
    - Chọn điểm **bắt đầu** và **đích**.
    - Rải các điểm số trên mê cung.

### `player_movement.py`
    - Xử lý phím di chuyển (`WASD` hoặc `Arrow keys`).
    - Kiểm tra va chạm với tường, cập nhật vị trí người chơi.

### `ui.py`
    - Hiển thị mê cung, người chơi, AI.
    - Hiển thị điểm số, thời gian, HUD, thông báo chiến thắng/thua.
    - Vẽ đường đi, điểm thưởng trong mê cung.

### `colors_and_fonts.py`
    - Chứa màu sắc, font chữ của game.
    - Load thông tin từ file `colors.json`.

### `compare.py`
    - Kiểm soát các lệnh chạy các thuật toán trong chế độ 2

### `Cost_matrix.py`

### `Draw_manager.py`
    - Tổng hợp các lệnh những thứ xuất hiện trên màn hình ở cả 2 chế độ

### `Easy.py`
    - Tổng hợp các thuật toán cơ bản trong đồ thị (BFS, DFS, Greedy, A*)

### `event_handler.py`
    - Các lệnh để out màn hình, chuyển màn

### `game_logic.py`
    - Tìm chu trình của AI ở chế độ 1
    - Cập nhật vị trí hiện tại của người chơi, AI

### `game_state.py`
    - Quản lý trò chơi bao gồm những biến cần thiết cho trò chơi
    
### `Genetic_Algorithm_With_Astar.py`
    - Thuật toán AI

### `Hill_Climbing_With_Astar.py`
    - Thuật toán AI

### `Simulated_Annealing_With_Astar.py`
    - Thuật toán AI