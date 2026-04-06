from random import randint, random
import math
import csv
from time import time
import numpy as np

ITENS_CSV = "itens.csv"
RESULTS_CSV = "results.csv"

INITIAL_TEMPERATURE = 10000
FINAL_TEMPERATURE = 1
CAPACITY = 50

EXECUTIONS = 50

ALPHAS = [0.85, 0.90, 0.95, 0.99]

def calculate_total_weight(itens: list[tuple[int, int]], selected_itens: list[int]):
    return sum(item[1] for item, selected in zip(itens, selected_itens) if selected)

def calculate_total_value(itens: list[tuple[int, int]], selected_itens: list[int]):
    return sum(item[0] for item, selected in zip(itens, selected_itens) if selected)

def get_itens(filename: str) -> list[tuple[int, int]]:
    with open(filename, mode="r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        return [(int(row[0]), int(row[1])) for row in reader]

def simulated_annealing(itens: list[tuple[int, int]], capacity: int, initial_temperature: int, final_temperature: int, alpha: float) -> list[int]:
    current_solution = [0] * len(itens)
    current_total_value = calculate_total_value(itens, current_solution)
    
    best_solution = list(current_solution)
    best_total_value = current_total_value

    t = initial_temperature

    history: list[int] = []

    while t > final_temperature:
        
        # Gerar um vizinho/solução alterando um bit da solução atual (flip)
        neighbor = list(current_solution)
        random_index: int = randint(0, len(itens) - 1)
        neighbor[random_index] = 1 - neighbor[random_index]
        
        neighbor_total_weight = calculate_total_weight(itens, neighbor)

        if (neighbor_total_weight <= capacity):
            neighbor_total_value = calculate_total_value(itens, neighbor)
            delta = neighbor_total_value - current_total_value

            if (delta > 0 or random() < math.exp(delta/t)):
                current_solution = list(neighbor)
                current_total_value = neighbor_total_value

                if (current_total_value > best_total_value):
                    best_solution = list(current_solution)
                    best_total_value = current_total_value

        history.append(best_total_value)
        t *= alpha

    return history

def knapsack_proplem_simulation(alpha: float, executions: int) -> None:
    iterations_history = []
    value_history = []
    time_execution_history = []

    for i in range(executions):
        initial_time = time()
        history: list[int] = simulated_annealing(available_itens, CAPACITY, INITIAL_TEMPERATURE, FINAL_TEMPERATURE, alpha)
        
        time_execution_history.append(time() - initial_time)
        iterations_history.append(len(history))
        value_history.append(history[-1])

    return {
        "alpha": alpha,
        "mean_value": np.mean(value_history),
        "best_value": np.max(value_history),
        "standard_deviation": np.std(value_history),
        "mean_iterations": np.mean(iterations_history),
        "mean_time": np.mean(time_execution_history)
    }

available_itens: list[tuple[int, int]] = get_itens(ITENS_CSV)
all_results = []

for alpha in ALPHAS:
    result_stats = knapsack_proplem_simulation(alpha, EXECUTIONS)
    all_results.append(result_stats)

with open(RESULTS_CSV, mode="w", encoding="utf-8", newline="") as file:
    fieldnames = ["alpha", "mean_value", "best_value", "standard_deviation", "mean_iterations", "mean_time"]
    writer = csv.DictWriter(file, fieldnames)

    writer.writeheader()
    for row in all_results:
        writer.writerow(row)