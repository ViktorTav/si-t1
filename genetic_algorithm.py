from random import randint, random, sample
from time import time
import numpy as np
import csv

CAPACITY = 50
CROSSOVER_RATE = 0.6
MUTATION_RATE = 0.01
ELITE_SIZE = 2
TOURNAMENT_SIZE = 3

SELECTED_ITEM_PROBABILITY = 0.05

ITENS_CSV = "itens.csv"
RESULTS_CSV = "results_genetic_algorithm.csv"

EXECUTIONS = 30

GENERATIONS = [25, 50, 100]
POPULATION_SIZES = [50, 100]


def get_itens(filename: str) -> list[tuple[int, int]]:
    with open(filename, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        return [(int(row[0]), int(row[1])) for row in reader]

def generate_chromosome(n: int) -> list[int]:
    return [1 if random() < SELECTED_ITEM_PROBABILITY else 0 for _ in range(n)]

def generate_initial_population(population_size: int, chromosome_size: int) -> list[list[int]]:
    return [generate_chromosome(chromosome_size) for _ in range(population_size)]

def calculate_total_weight(itens: list[tuple[int, int]], selected_itens: list[int]) -> int:
    return sum(item[1] for item, selected in zip(itens, selected_itens) if selected)

def calculate_total_selected_itens(itens: list[tuple[int, int]], selected_itens: list[int]) -> int:
    return sum(1 for _, selected in zip(itens, selected_itens) if selected)

def calculate_total_value(itens: list[tuple[int, int]], selected_itens: list[int]) -> int:
    return sum(item[0] for item, selected in zip(itens, selected_itens) if selected)

def calculate_chromosome_fitness(chromosome: list[int], itens: list[tuple[int, int]], max_capacity: int) -> int:
    weight: int = calculate_total_weight(itens, chromosome)
    value: int = calculate_total_value(itens, chromosome)

    if weight > max_capacity:
        return 0
    
    return value

def chromosome_mutation(chromosome: list[int], mutation_rate) -> list[int]:
    for i in range(len(chromosome)):
        if random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]

    return chromosome

def chromosome_selection(k: int, population: list[list[int]], itens: list[int], max_capacity: int):
    random_chromosomes = sample(population, k)

    return max(random_chromosomes, key=lambda chromosome: calculate_chromosome_fitness(chromosome, itens, max_capacity))

def crossover(chromosome_a: list[int], chromosome_b: list[int]) -> tuple[list[int], list[int]]:
    crossover_point: int = randint(1, len(chromosome_a) - 1)

    child_1: list[int] = chromosome_a[:crossover_point] + chromosome_b[crossover_point:]
    child_2: list[int] = chromosome_b[:crossover_point] + chromosome_a[crossover_point:]

    return child_1, child_2

def get_elite_chromosomes(n:int, population: list[list[int]], itens: list[int], max_capacity: int) -> list[list[int]]:
    sorted_population: list[list[int]] = sorted(population, key=lambda chromosome: calculate_chromosome_fitness(chromosome, itens, max_capacity), reverse=True)

    return sorted_population[:n]

def genetic_algorithm(itens: list[tuple[int, int]], capacity:int, generations: int, population_size: int, crossover_rate: float, mutation_rate: float, elite_size: int, tournament_size: int):
    population: list[list[int]] = generate_initial_population(population_size, len(itens))

    best_chromosome_history: list[list[int]] = []

    for _ in range(generations):
        next_population: list[list[int]] = []
        elite_chromosomes: list[list[int]]  = get_elite_chromosomes(elite_size, population, itens, capacity)

        next_population.extend(elite_chromosomes)

        best_chromosome_history.append(elite_chromosomes[0])

        while len(next_population) < population_size :
            parent_1 = chromosome_selection(tournament_size, population, itens, capacity)
            parent_2 = chromosome_selection(tournament_size, population, itens, capacity)

            if random() <= crossover_rate:
                child_1, child_2 = crossover(parent_1, parent_2)
            else:
                child_1, child_2 = parent_1.copy(), parent_2.copy()

            child_1 = chromosome_mutation(child_1, mutation_rate)
            child_2 = chromosome_mutation(child_2, mutation_rate)

            next_population.append(child_1)

            if len(next_population) < population_size:
                next_population.append(child_2)

        population = next_population
        
    return best_chromosome_history

available_itens: list[tuple[int, int]] = get_itens(ITENS_CSV)

def knapsack_proplem_simulation(generations: int, population_size: int, executions: int) -> None:
    fitness_history = []
    best_weight = 0
    best_selected_items_total = 0
    time_execution_history = []

    for i in range(executions):
        initial_time = time()
        best_chromosome_history = genetic_algorithm(available_itens, CAPACITY, generations, population_size, CROSSOVER_RATE, MUTATION_RATE, ELITE_SIZE, TOURNAMENT_SIZE)
        
        fitness = calculate_chromosome_fitness(best_chromosome_history[-1], available_itens, CAPACITY)
        weight = calculate_total_weight(available_itens, best_chromosome_history[-1])
        selected_items_total = calculate_total_selected_itens(available_itens, best_chromosome_history[-1])

        time_execution_history.append(time() - initial_time)
        fitness_history.append(fitness)

        if weight > best_weight and selected_items_total > best_selected_items_total:
            best_weight = weight
            best_selected_items_total = selected_items_total

        print(f"Generations/Population Size: {generations}/{population_size}")
        print(f"Execution {i}: {time_execution_history[-1]}")
        print(f"Best Fitness: {fitness}\n")
        print(f"Weight/Selected Items: {weight}/{selected_items_total}")


    return {
        "generations": generations,
        "population_size": population_size,
        "mean_fitness": np.mean(fitness_history),
        "best_fitness": np.max(fitness_history),
        "best_weight_item_proportion": f"{best_weight}/{best_selected_items_total}",
        "standard_deviation": np.std(fitness_history),
        "mean_time": np.mean(time_execution_history)
    }

all_results = []

for population_size in POPULATION_SIZES:
    for generation in GENERATIONS:
        result_stats = knapsack_proplem_simulation(generation, population_size, EXECUTIONS)
        all_results.append(result_stats)

with open(RESULTS_CSV, mode="w", encoding="utf-8", newline="") as file:
    fieldnames = ["generations", "population_size", "mean_fitness", "best_fitness", "best_weight_item_proportion", "standard_deviation", "mean_time"]
    writer = csv.DictWriter(file, fieldnames)

    writer.writeheader()
    for row in all_results:
        writer.writerow(row)