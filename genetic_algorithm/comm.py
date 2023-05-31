import random
import numpy as np

def PMX_crossover(parent1, parent2):
    rng = np.random.default_rng()
    cutoff_1, cutoff_2 = np.sort(rng.choice(np.arange(len(parent1) + 1), size=2, replace=False))

    def PMX_one_child(p1, p2):
        child = np.zeros(len(p1), dtype=p1.dtype)
        child[cutoff_1:cutoff_2] = p1[cutoff_1:cutoff_2]

        for i in np.concatenate([np.arange(0, cutoff_1), np.arange(cutoff_2, len(p1))]):
            candidate = p2[i]
            while candidate in p1[cutoff_1:cutoff_2]:
                candidate = p2[np.where(p1 == candidate)[0][0]]
            child[i] = candidate
        return child

    child1 = PMX_one_child(parent1, parent2)
    child2 = PMX_one_child(parent2, parent1)

    return child1, child2

def fitness_function(vec, matrix):
    cost = matrix[vec[-1]][vec[0]]
    for i in range(len(vec)-1):
        cost += matrix[vec[i]][vec[i+1]]
    return cost

def comm(matrix):
    count_cities = len(matrix)
    n = 50  # размер популяции
    population = []
    for i in range(0, n):
        life = []
        edges = [i for i in range(count_cities)]

        for j in range(count_cities):
            rand_edge = random.choice(edges)
            life.append(rand_edge)
            edges.remove(rand_edge)

        population.append(life)

    for i in range(4000):
        fitnesses = [fitness_function(i, matrix) for i in population]
        indexes = [i for i in range(n)]
        x = zip(fitnesses, indexes)
        xs = sorted(x, key=lambda tup: tup[0], reverse=False)
        fitnesses_sorted = [x[0] for x in xs]
        indexes_sorted = [x[1] for x in xs]

        # selection for crossover and crossover
        new_population = []
        for i in range(n // 2):
            rand_numb_1 = random.randint(1, 100)
            if (rand_numb_1 <= 50):
                parent_1 = population[random.choice(indexes_sorted[:n // 4])]
            if (51 <= rand_numb_1 <= 80):
                parent_1 = population[random.choice(indexes_sorted[n // 4: n // 2])]
            if (81 <= rand_numb_1 <= 95):
                parent_1 = population[random.choice(indexes_sorted[n // 2: 3 * (n // 4)])]
            if (96 <= rand_numb_1 <= 100):
                parent_1 = population[random.choice(indexes_sorted[3 * (n // 4):n])]

            rand_numb_2 = random.randint(1, 100)
            if (rand_numb_2 <= 50):
                parent_2 = population[random.choice(indexes_sorted[:n // 4])]
            if (51 <= rand_numb_2 <= 80):
                parent_2 = population[random.choice(indexes_sorted[n // 4: n // 2])]
            if (81 <= rand_numb_2 <= 95):
                parent_2 = population[random.choice(indexes_sorted[n // 2: 3 * (n // 4)])]
            if (96 <= rand_numb_2 <= 100):
                parent_2 = population[random.choice(indexes_sorted[3 * (n // 4):n])]

            child1,child2 = PMX_crossover((np.array(parent_1)),np.array(parent_2))
            new_population.append(list(child1))
            new_population.append(list(child2))

            # mutation
            for chrom in new_population:
                for ind_gene in range(len(chrom)):
                    mutation_val = random.randint(1,100)
                    if (mutation_val == 1):
                        t = chrom[ind_gene]
                        chrom[ind_gene] = chrom[len(chrom)-ind_gene-1]
                        chrom[len(chrom) - ind_gene - 1] = t

        population = new_population.copy()
    return population[indexes_sorted[0]],fitness_function(population[indexes_sorted[0]],matrix)

