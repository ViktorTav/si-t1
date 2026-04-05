from random import randint, random
import math

def calculate_total_weight(itens: list[tuple[int, int]], selected_itens: list[int]):
    return sum(item[1] for item, selected in zip(itens, selected_itens) if selected)

def calculate_total_value(itens: list[tuple[int, int]], selected_itens: list[int]):
    return sum(item[0] for item, selected in zip(itens, selected_itens) if selected)

def simulated_annealing(itens: list[tuple[int, int]], capability: int, initial_temperature: int, final_temperature: int, alpha: float):
    current_solution = [0] * len(itens)
    current_total_value = calculate_total_value(itens, current_solution)
    
    best_solution = list(current_solution)
    best_total_value = current_total_value

    t = initial_temperature

    while t > final_temperature:
        
        # Gerar um vizinho/solução alterando um bit da solução atual (flip)
        neighbor = list(current_solution)
        random_index: int = randint(0, len(itens) - 1)
        neighbor[random_index] = 1 - neighbor[random_index]
        
        print(f"neighbor: {neighbor}")

        neighbor_total_weight = calculate_total_weight(itens, neighbor)

        print(f"neighbor_total_weight: {neighbor_total_weight}")

        if (neighbor_total_weight <= capability):
            neighbor_total_value = calculate_total_value(itens, neighbor)

            print(f"neighbor_total_value: {neighbor_total_value}")
            print(f"best_total_value: {best_total_value}")

            delta = neighbor_total_value - current_total_value

            print(f"delta: {delta}")

            random_number = random()

            print(f"random_number: {random_number}, probabilidade: {math.exp(delta/t)}, t: {t}, delta: {delta}")
            if (delta > 0 or random_number < math.exp(delta/t)):
                current_solution = list(neighbor)
                current_total_value = neighbor_total_value

                if (delta > 0):
                    print(f"Vizinho é uma solução melhor que a atual: {neighbor}")
                else:
                    print(f"Vizinho é uma solução pior, mas explorando outras possibilidades: {neighbor}")

                if (current_total_value > best_total_value):
                    print(f"Vizinho é a melhor solução, novo recorde: {neighbor}")

                    best_solution = list(current_solution)
                    best_total_value = current_total_value
            else:
                print(f"Vizinho é uma solução pior, continuando com a melhor solução: {best_solution}")
        else:
            print(f"Vizinho ultrapassa a capacidade da mochila. Continuando com a melhor solução: {best_solution}")
        
        print()

        t *= alpha

    return best_solution


itens = [
    (500, 2),
    (1000, 4),
    (150, 3),
    (200, 1),
    (5000, 10),
    (3214, 14),
    (100, 1),
    (275, 7)
]

initial_temperature = 10000
final_temperature = 1
alpha = 0.95
capability = 15

print(simulated_annealing(itens, capability, initial_temperature, final_temperature, alpha))




