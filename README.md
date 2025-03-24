# Matrix Game - IT3160 🎮

## Giới thiệu 📜
Matrix Game là một trò chơi giải mê cung được phát triển bằng Python và Pygame.
Người chơi sẽ thi đấu với AI.
Người chơi sẽ điều khiển nhân vật di chuyển trong mê cung và thu thập điểm.

## Cấu trúc dự án 📂

### `main.py`
- Chứa vòng lặp chính của game.
- Gọi các hàm để khởi tạo mê cung, điều khiển người chơi, cập nhật giao diện.
- Xử lý sự kiện như nhấn phím, thoát game.

### `maze_generation.py`
- Tạo mê cung bằng thuật toán Recursive Backtracking.
- Chọn điểm **bắt đầu** và **đích**.
- Rải các điểm số trên mê cung.

### `player_movement.py`
- Xử lý phím di chuyển (`WASD` hoặc `Arrow keys`).
- Kiểm tra va chạm với tường, cập nhật vị trí người chơi.

### `ui.py`
- Hiển thị mê cung, người chơi, AI.
- Hiển thị điểm số, HUD, thông báo chiến thắng/thua.
- Vẽ đường đi, điểm thưởng trong mê cung.

### `colors_and_fonts.py`
- Chứa màu sắc, font chữ của game.
- Load thông tin từ file `colors.json`.
