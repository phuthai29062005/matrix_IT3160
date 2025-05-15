import numpy as np
from queue import PriorityQueue
import random
from Find_Single_Path import A_star

INT_MAX = 2147483647

GRID = 70

def distance_with_BFS(maze, start, checkpoints): # return list
    result = {start: 0}
    level = 0
    stack = []
    stack.append(start)

    while not stack.empty():
        current = stack.pop()
        level += 1
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            neighbor = current[0] + dx, current[1] + dy
            if (neighbor[0] < GRID and neighbor[1] < GRID and maze[current[0]][current[1]] == 0 and current not in stack):
                stack.append(neighbor)
                if (neighbor in checkpoints):
                    result.update({neighbor: level})

    for i in range(len(checkpoints)):
        checkpoints[i] = result[checkpoints[i]]

    return checkpoints

def preprocess(maze, start, goal, checkpoints):
    checkpoints.append(goal)
    checkpoints.insert(0, start)
    total_points = len(checkpoints)
    cost_matrix = np.zeros(total_points, total_points)
    for i in range(total_points):
        cost_matrix[i] = distance_with_BFS(maze, checkpoints[i], checkpoints)
    return cost_matrix

def create_initial_population(population_size, numPoints):
    population = []
    for _ in population_size:
        original = [i for i in range(1, numPoints + 1)]
        original.shuffle(original)
        individual = original
        population.append(individual)
    return population

def cal_fitness(start, goal, chromosome):
    score = 0
    score += cost_matrix[0][chromosome[0]]
    for i in range(len(chromosome) - 1):
        score += cost_matrix[chromosome[i]][chromosome[i+1]]
    score += cost_matrix[chromosome[i+1]][len(chromosome)]
    return score

def selection(population, fitness_score, numElite):
    best_indices = np.argmax(fitness_score, numElite)
    return [population[i] for i in best_indices]

def cross_over(parent1, parent2):
    child = [None] * len(parent1)
    start, end = random.sample(range(len(parent1)), 2)
    child[start:end] = parent1[start:end]
    pointer = 0
    for gene in parent2:
        if gene not in child:
            while child[pointer] is not None:
                pointer += 1
            child[pointer] = gene
    return child

def mutation(chromosome, mutation_rate):
    if random.random() < mutation_rate:
        start, end = random.sample(range(len(chromosome)), 2)
        chromosome[start], chromosome[end] = chromosome[end], chromosome[start]
    return chromosome

def genetic_algorithm(maze, start, goal, checkpoints, mutation_rate, max_iter): 
# trả về list chứa thứ tự các điểm đi qua
    global cost_matrix
    cost_matrix = preprocess(maze, start, goal, checkpoints)
    population_size = len(checkpoints) * 10
    numElite = int(population_size * 10 / 100)
    numHybrid = population_size - numElite
    population = create_initial_population(population_size, len(checkpoints))
    fitness_population = [cal_fitness(start, goal, population[i]) for i in range(population_size)]

    for _ in range(max_iter):
        new_generation = []
        elites = selection(population, fitness_population, numElite)
        new_generation.extend(elites)
        components_hybrid = selection(population, fitness_population, numElite * 5)

        for index in range(numHybrid):
            parent1 = random.choice(components_hybrid)
            parent2 = random.choice(components_hybrid)
            child = cross_over(parent1, parent2)
            child = mutation(child, mutation_rate)
            new_generation.append(child)

        population = new_generation

    best_route = np.argmax(population)
    return population[best_route]

def ga_Astar(maze, start, goal, checkpoints, mutation_rate=0.2, max_iter=1000):
    order = genetic_algorithm(maze, start, goal, checkpoints, mutation_rate, max_iter)
    A_star(maze, start, order[0])
    for i in range(len(order) - 1):
        A_star(maze, order[i], order[i + 1])
    A_star(maze, order[-1], goal)


