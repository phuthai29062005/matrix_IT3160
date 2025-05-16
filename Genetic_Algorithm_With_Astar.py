import numpy as np
from collections import deque
import random
from Easy import A_star
from Cost_Matrix import *
from ui import *

INT_MAX = 2147483647

GRID = 70

def create_initial_population(population_size, numPoints):
    population = []
    for _ in range(population_size):
        individual = list(range(1, numPoints + 1))
        random.shuffle(individual)
        population.append(individual)
    return population

def cal_fitness(start, goal, chromosome, cost_matrix):
    score = 0
    score += cost_matrix[0][chromosome[0]]
    for i in range(len(chromosome) - 1):
        score += cost_matrix[chromosome[i]][chromosome[i+1]]
    score += cost_matrix[chromosome[i+1]][len(chromosome)]
    return score

def selection(population, fitness_score, numElite):
    best_indices = np.argsort(fitness_score)[:numElite]
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
    cost_matrix = preprocess(maze, start, goal, checkpoints.copy())
    population_size = len(checkpoints) * 10
    numElite = int(population_size * 10 / 100)
    numHybrid = population_size - numElite
    population = create_initial_population(population_size, len(checkpoints))
    fitness_population = [cal_fitness(start, goal, population[i], cost_matrix) for i in range(population_size)]

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

    best_route = np.argmin(fitness_population)
    return population[best_route]

def ga_Astar(maze, start, goal, checkpoints, mutation_rate=0.2, max_iter=1000):
    order = genetic_algorithm(maze, start, goal, checkpoints, mutation_rate, max_iter)
    order = [x - 1 for x in order]  # chuyển đổi từ 1-based index sang 0-based index
    path = A_star(None, maze, start, checkpoints[order[0]], checkpoints, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False)

    for i in range(len(order) - 1):
        path.extend(A_star(None, maze, checkpoints[order[i]], checkpoints[order[i + 1]], None, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False))
    path.extend(A_star(None, maze, checkpoints[order[-1]], goal, None, AI_POS, BORDER_COLOR_AI, CELL_SIZE_AI, False))
    return path
	


