import time
import matplotlib.pyplot as plt
from game_state import GameState
from Hill_Climbing_With_Astar import hill_climbing_Astar
from Simulated_Annealing_With_Astar import simulated_annealing_Astar
from Genetic_Algorithm_With_Astar import ga_Astar
from compare import compare_maze

def run_experiments(num_runs=10):
    algorithms = {
        "Hill Climbing": hill_climbing_Astar,
        "Simulated Annealing": simulated_annealing_Astar,
        "Genetic Algorithm": ga_Astar
    }
    
    results = {name: [] for name in algorithms.keys()}
    
    for run in range(num_runs):
        state = GameState()  # Initialize a new game state for each run
        state.initialize_maze()  # Assuming there's a method to initialize the maze
        
        for name, algorithm in algorithms.items():
            start_time = time.perf_counter()
            path = algorithm(state.maze, state.player_pos, state.goal_pos, state.scattered_points)
            end_time = time.perf_counter()
            execution_time = end_time - start_time
            
            results[name].append((len(path), execution_time))  # Store path length and execution time
            
    return results

def plot_results(results):
    for name, data in results.items():
        path_lengths, execution_times = zip(*data)
        plt.plot(path_lengths, label=f"{name} Path Length")
        plt.plot(execution_times, label=f"{name} Execution Time")
    
    plt.title("Algorithm Performance Comparison")
    plt.xlabel("Run Number")
    plt.ylabel("Value")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    num_runs = 10  # You can change this to run more or fewer experiments
    results = run_experiments(num_runs)
    plot_results(results)