#!/usr/bin/env python

import random
import string

# Calculate max fitness based on population
def calculate_max_fitness():
    i = board_size - 1
    max_fitness = 0
    while i > 0:
        max_fitness += i
        i -= 1
    return max_fitness

# Generate a random individual based on the board size
def random_individual(board_size):
    return [ random.randint(1, board_size) for _ in range(board_size) ]

# Define the fitness of an individual based on the number of pairs of non-attacking queens
def fitness(individual):
    horizontal_collisions = sum([individual.count(queen)-1 for queen in individual])/2
    diagonal_collisions = 0

    n = len(individual)
    left_diagonal = [0] * 2*n
    right_diagonal = [0] * 2*n
    for i in range(n):
        left_diagonal[i + individual[i] - 1] += 1
        right_diagonal[len(individual) - i + individual[i] - 2] += 1

    for i in range(2*n-1):
        counter = 0
        if left_diagonal[i] > 1:
            counter += left_diagonal[i]-1
        if right_diagonal[i] > 1:
            counter += right_diagonal[i]-1
        diagonal_collisions += counter / (n-abs(i-n+1))
    return int(max_fitness - (horizontal_collisions + diagonal_collisions))

# Calculate the probability of an individual based on his fitness compared to max_fitness
def probability(individual, fitness):
    return fitness(individual) / max_fitness

# Take a random individual based on population by probabilitie
def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"

# Return one new individual, his genes are from two individual x and y with a random with a random separator
def reproduce(x, y):
    n = len(x)
    #c = 4
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]

# Return an individual with one random gene modified between 1 and n (board_size)
def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n)
    x[c] = m
    return x

# Loop of creation of new populations with random individuals 
def genetic_queen(population, fitness):
    # Probability of mutation
    new_population = []
    probabilities = [probability(n, fitness) for n in population]
    for i in range(len(population)):
        x = random_pick(population, probabilities)
        y = random_pick(population, probabilities)
        child = reproduce(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        new_population.append(child)
        if fitness(child) == max_fitness: break
    return new_population

# Print one individual with his genes, his probability and his fitness score
def print_individual(x):
    print("{},  fitness = {}, probability = {:.6f}"
        .format(str(x), fitness(x), probability(x, fitness)))

# Asks the user for main variables
def get_settings():
    while True:
        try:
            board_size = int(input("Please choose the board size (default 8): "))
            if board_size > 3:
                break;
            else:
                print("Please enter a number > 4.")
        except ValueError:
            print("Please enter a valid number.")
    while True:
        try:
            max_pop = int(input("Please choose the size of population (default 500): "))
            if max_pop > 3:
                break;
            else:
                print("Please enter a number > 1.")
        except ValueError:
            print("Please enter a valid number.")
    while True:
        try:
            mutation_probability = float(input("Please choose the mutation probability (default 0.05): "))
            if mutation_probability > 0 and mutation_probability < 1:
                break;
            else:
                print("Please enter a number > 0 and < 1.")
        except ValueError:
            print("Please enter a valid number.")
    return board_size, max_pop, mutation_probability

# Main loop
if __name__ == "__main__":
    board_size, max_pop, mutation_probability = get_settings()
    max_fitness = calculate_max_fitness()
    population = [random_individual(board_size) for _ in range(max_pop)]
    generation = 1
    while not max_fitness in [fitness(x) for x in population]:
        population = genetic_queen(population, fitness)
        print("Generation = " + str(generation) + " | Maximum fitness = {}".format(max([fitness(n) for n in population])))
        generation += 1
    print("Solved in Generation {}!".format(generation-1))
    for x in population:
        if fitness(x) == max_fitness:
            print_individual(x)
