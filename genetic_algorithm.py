from random import randint, sample

def generate_chromosome(n: int) -> list[int]:
    return [randint(0, 1) for _ in range(n)]

def generate_initial_population(population_size: int, chromosome_size: int) -> list[list[int]]:
    return [generate_chromosome(chromosome_size) for _ in range(population_size)]

def calculate_total_weight(itens: list[tuple[int, int]], selected_itens: list[int]) -> int:
    return sum(item[1] for item, selected in zip(itens, selected_itens) if selected)

def calculate_total_value(itens: list[tuple[int, int]], selected_itens: list[int]) -> int:
    return sum(item[0] for item, selected in zip(itens, selected_itens) if selected)

# Talvez implementar uma função para calcular o fitness através do valor - penalidade por excesso de peso?
def calculate_chromosome_fitness(chromosome: list[int], itens: list[tuple[int, int]]) -> int:
    return calculate_total_value(itens, chromosome)

def chromosome_mutation(chromosome: list[int]) -> list[int]:
    random_index: int = randint(0, len(chromosome) - 1)

    chromosome[random_index] = 1 - chromosome[random_index]

    return chromosome

def chromosome_selection(k: int, population: list[list[int]], itens: list[int]):
    random_chromosomes = sample(population, k)

    return max(random_chromosomes, key=lambda chromosome: calculate_chromosome_fitness(chromosome, itens))

def crossover(chromosome_a: list[int], chromosome_b: list[int]) -> list[int]:
    crossover_point: int = randint(1, len(chromosome_a) - 1)

    return chromosome_a[:crossover_point] + chromosome_b[crossover_point:]

def genetic_algorithm(itens: list[tuple[int, int]], generations: int, crossover_rate: float, mutation_rate: float):
    population: list[list[int]] = generate_initial_population(itens, len(itens))

    for i in range(len(generations)):
        