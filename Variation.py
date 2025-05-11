import numpy as np
import heapq
import random
import itertools # Vẫn dùng để tính cost ban đầu, nhưng không duyệt hoán vị
# có thêm checkpoint
# A* + GA
def heuristic(a, b): # manhattan
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(maze, start, goal):
    rows, cols = maze.shape
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]
        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            data.append(start)
            return data[::-1], gscore[goal]
        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0]][neighbor[1]] == 1: continue
            else: continue
            tentative_g_score = gscore[current] + 1
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, float('inf')): continue
            if tentative_g_score < gscore.get(neighbor, float('inf')):
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))
    return None, float('inf')

# --- Các thành phần của Thuật toán Di truyền ---

# Hàm tính tổng chi phí cho một thứ tự waypoint (Fitness Function)
def calculate_total_cost(order, start, end, costs):
    """Tính tổng chi phí đi từ start -> waypoints theo thứ tự -> end."""
    current_cost = costs.get((start, order[0]), float('inf'))
    if current_cost == float('inf'): return float('inf')

    for i in range(len(order) - 1):
        segment_cost = costs.get((order[i], order[i+1]), float('inf'))
        if segment_cost == float('inf'): return float('inf')
        current_cost += segment_cost

    end_cost = costs.get((order[-1], end), float('inf'))
    if end_cost == float('inf'): return float('inf')
    current_cost += end_cost
    return current_cost

# Lựa chọn Giải đấu (Tournament Selection)
def tournament_selection(population, fitnesses, k):
    """Chọn cá thể tốt nhất từ k cá thể ngẫu nhiên."""
    selection_ix = random.sample(range(len(population)), k)
    best_ix = selection_ix[0]
    for ix in selection_ix[1:]:
        if fitnesses[ix] < fitnesses[best_ix]: # Chi phí thấp hơn là tốt hơn
            best_ix = ix
    return population[best_ix]

# Lai ghép Thứ tự (Order Crossover - OX1)
def order_crossover(parent1, parent2):
    """Thực hiện lai ghép OX1."""
    size = len(parent1)
    child = [None]*size
    start, end = sorted(random.sample(range(size), 2))

    # Sao chép đoạn gen từ parent1
    child[start:end+1] = parent1[start:end+1]

    # Điền các gen còn lại từ parent2
    p2_idx = 0
    c_idx = 0
    while None in child:
        # Tìm vị trí None tiếp theo trong child
        while child[c_idx] is not None:
            c_idx = (c_idx + 1) % size

        # Tìm gen tiếp theo trong parent2 mà chưa có trong child
        while parent2[p2_idx] in child:
            p2_idx = (p2_idx + 1) % size

        # Đặt gen vào child
        child[c_idx] = parent2[p2_idx]
        p2_idx = (p2_idx + 1) % size # Di chuyển đến gen tiếp theo của p2

    return child


# Đột biến Hoán vị (Swap Mutation)
def swap_mutation(individual):
    """Hoán đổi ngẫu nhiên hai vị trí trong cá thể."""
    size = len(individual)
    if size < 2: return individual # Không thể hoán vị nếu ít hơn 2 phần tử
    idx1, idx2 = random.sample(range(size), 2)
    individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return individual

# --- Hàm chính sử dụng GA ---
def find_path_genetic_algorithm(grid, start, end, waypoints,
                                 pop_size=100, num_generations=50,
                                 cx_prob=0.8, mut_prob=0.1, tournament_size=5):
    """
    Tìm đường đi gần tối ưu qua waypoints bằng GA.

    Args:
        grid, start, end, waypoints: Như trước.
        pop_size (int): Kích thước quần thể.
        num_generations (int): Số thế hệ GA chạy.
        cx_prob (float): Xác suất lai ghép.
        mut_prob (float): Xác suất đột biến.
        tournament_size (int): Kích thước giải đấu cho lựa chọn.

    Returns:
        tuple: (final_path, best_cost) hoặc (None, float('inf'))
    """
    # --- Bước 1: Tính toán chi phí và đường đi A* ---
    points = [start] + waypoints + [end]
    costs = {}
    paths = {} # Lưu lại đường đi nếu cần tái tạo

    print("Đang tính toán chi phí A* giữa các điểm...")
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1 = points[i]
            p2 = points[j]
            path_segment, cost_segment = a_star_search(grid, p1, p2)
            costs[(p1, p2)] = cost_segment
            costs[(p2, p1)] = cost_segment
            if path_segment is not None:
                paths[(p1, p2)] = path_segment
                paths[(p2, p1)] = path_segment[::-1]
            else:
                # Nếu không có đường nối giữa 2 điểm bất kỳ, GA sẽ khó hoạt động
                # hoặc cần xử lý đặc biệt (chi phí vô cùng)
                 if p1 == start or p2 == end or (p1 in waypoints and p2 in waypoints):
                    print(f"Cảnh báo nghiêm trọng: Không tìm thấy đường đi giữa {p1} và {p2}. Không thể hoàn thành.")
                    # return None, float('inf') # Có thể dừng hẳn ở đây
                    pass # Hoặc để GA chạy với chi phí vô cùng

    print("Tính toán A* hoàn tất.")

    if not waypoints: # Xử lý trường hợp không có waypoint
        final_path, total_cost = a_star_search(grid, start, end)
        return final_path, total_cost

    # --- Bước 2: Khởi tạo quần thể GA ---
    print("Khởi tạo quần thể GA...")
    population = []
    for _ in range(pop_size):
        individual = random.sample(waypoints, len(waypoints)) # Tạo hoán vị ngẫu nhiên
        population.append(individual)

    best_overall_individual = None
    best_overall_cost = float('inf')

    # --- Bước 3: Vòng lặp tiến hóa GA ---
    print("Bắt đầu quá trình tiến hóa GA...")
    for gen in range(num_generations):
        # Tính fitness cho toàn bộ quần thể
        fitnesses = [calculate_total_cost(ind, start, end, costs) for ind in population]

        # Tìm cá thể tốt nhất trong thế hệ hiện tại và cập nhật cá thể tốt nhất toàn cục
        current_best_idx = min(range(len(fitnesses)), key=fitnesses.__getitem__)
        current_best_cost = fitnesses[current_best_idx]

        if current_best_cost < best_overall_cost:
            best_overall_cost = current_best_cost
            best_overall_individual = population[current_best_idx][:] # Copy lại
            print(f"Thế hệ {gen+1}/{num_generations}, Chi phí tốt nhất mới: {best_overall_cost:.2f}")
        elif (gen + 1) % 10 == 0: # In tiến trình định kỳ
             print(f"Thế hệ {gen+1}/{num_generations}, Chi phí tốt nhất hiện tại: {best_overall_cost:.2f}")


        # Tạo thế hệ mới
        new_population = []

        # Giữ lại cá thể tốt nhất (Elitism) - đơn giản nhất là giữ lại 1
        if best_overall_individual is not None:
             new_population.append(best_overall_individual[:]) # Thêm bản sao

        # Tạo các cá thể còn lại bằng lựa chọn, lai ghép, đột biến
        while len(new_population) < pop_size:
            # Lựa chọn cha mẹ
            parent1 = tournament_selection(population, fitnesses, tournament_size)
            parent2 = tournament_selection(population, fitnesses, tournament_size)

            # Lai ghép
            child1, child2 = parent1[:], parent2[:] # Mặc định là bản sao
            if random.random() < cx_prob:
                # Chỉ cần 1 child từ OX1, nhưng hàm trả về 1.
                # Để đơn giản, ta tạo 2 child bằng cách gọi 2 lần hoặc dùng toán tử khác
                # Ở đây ta chỉ lấy 1 child từ 1 lần gọi OX1
                child1 = order_crossover(parent1, parent2)
                # Nếu muốn 2 child, có thể gọi order_crossover(parent2, parent1)

            # Đột biến
            if random.random() < mut_prob:
                child1 = swap_mutation(child1)
            # if random.random() < mut_prob: # Nếu có child2
            #     child2 = swap_mutation(child2)

            new_population.append(child1)
            # if len(new_population) < pop_size: # Nếu có child2
            #     new_population.append(child2)


        population = new_population[:pop_size] # Cập nhật quần thể

    print("Tiến hóa GA hoàn tất.")

    # --- Bước 4: Tái tạo đường đi cuối cùng ---
    if best_overall_individual is None or best_overall_cost == float('inf'):
        print("GA không tìm thấy giải pháp hợp lệ.")
        return None, float('inf')

    print(f"Thứ tự waypoint tối ưu (heuristic) tìm được: {best_overall_individual}")
    print(f"Tổng chi phí ước tính: {best_overall_cost}")

    final_path = []
    current_point = start

    # Nối đoạn từ start đến waypoint đầu tiên
    next_wp = best_overall_individual[0]
    segment_path = paths.get((current_point, next_wp))
    if segment_path is None:
        print(f"Lỗi: Không tìm thấy đường đi đã lưu giữa {current_point} và {next_wp}")
        return None, float('inf') # Lỗi không mong muốn
    final_path.extend(segment_path[:-1])
    current_point = next_wp

    # Nối các đoạn giữa các waypoints
    for i in range(len(best_overall_individual) - 1):
        next_wp = best_overall_individual[i+1]
        segment_path = paths.get((current_point, next_wp))
        if segment_path is None:
            print(f"Lỗi: Không tìm thấy đường đi đã lưu giữa {current_point} và {next_wp}")
            return None, float('inf')
        final_path.extend(segment_path[:-1])
        current_point = next_wp

    # Nối đoạn từ waypoint cuối cùng đến end
    segment_path = paths.get((current_point, end))
    if segment_path is None:
        print(f"Lỗi: Không tìm thấy đường đi đã lưu giữa {current_point} và {end}")
        return None, float('inf')
    final_path.extend(segment_path)

    return final_path, best_overall_cost


# --- Ví dụ sử dụng ---
grid = np.array([
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
])

start_point = (0, 0)
end_point = (6, 7)
waypoints_to_visit = [(2, 2), (4, 6), (6, 1), (0, 3), (4, 1)] # Thêm waypoint để GA có ý nghĩa hơn

# Kiểm tra điểm hợp lệ (như code trước)
def is_valid(p, grid_shape):
    r, c = p
    rows, cols = grid_shape
    return 0 <= r < rows and 0 <= c < cols and grid[r, c] == 0

if not is_valid(start_point, grid.shape) or \
   not is_valid(end_point, grid.shape) or \
   any(not is_valid(wp, grid.shape) for wp in waypoints_to_visit):
    print("Lỗi: Có điểm không hợp lệ.")
else:
    # Tìm đường đi bằng GA
    optimal_path_ga, total_cost_ga = find_path_genetic_algorithm(
        grid, start_point, end_point, waypoints_to_visit,
        pop_size=100,         # Kích thước quần thể
        num_generations=100,  # Số thế hệ
        cx_prob=0.8,         # Xác suất lai ghép
        mut_prob=0.15,        # Xác suất đột biến (có thể cần cao hơn một chút cho TSP)
        tournament_size=5    # Kích thước giải đấu
    )

    if optimal_path_ga:
        print(f"\nTìm thấy đường đi (GA) với chi phí ước tính: {total_cost_ga}")

        # In grid đường đi (tùy chọn)
        path_grid_ga = np.copy(grid).astype(str)
        path_grid_ga[path_grid_ga == '0'] = '.'
        path_grid_ga[path_grid_ga == '1'] = '#'
        for r, c in optimal_path_ga:
            if (r, c) == start_point: path_grid_ga[r, c] = 'S'
            elif (r, c) == end_point: path_grid_ga[r, c] = 'E'
            elif (r, c) in waypoints_to_visit: path_grid_ga[r, c] = 'W'
            else: path_grid_ga[r, c] = '*'
        print("Đường đi GA trên lưới:")
        print('\n'.join(' '.join(row) for row in path_grid_ga))
        # print(optimal_path_ga) # In tọa độ
    else:
        print("\nKhông tìm thấy đường đi hợp lệ bằng GA.")