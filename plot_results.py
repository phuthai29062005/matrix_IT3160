import matplotlib.pyplot as plt
import numpy as np
import json
import os

def load_results(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def plot_results(results):
    algorithms = results.keys()
    times = [results[algo]['time'] for algo in algorithms]
    paths = [results[algo]['path_length'] for algo in algorithms]

    x = np.arange(len(algorithms))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Algorithms')
    ax1.set_ylabel('Time (seconds)', color=color)
    ax1.bar(x - width/2, times, width, label='Time', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:red'
    ax2.set_ylabel('Path Length', color=color)  # we already handled the x-label with ax1
    ax2.bar(x + width/2, paths, width, label='Path Length', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    ax1.set_xticks(x)
    ax1.set_xticklabels(algorithms)
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('Comparison of Pathfinding Algorithms')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    results_file = os.path.join(os.path.dirname(__file__), 'results.json')
    results = load_results(results_file)
    plot_results(results)