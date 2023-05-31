from random import randint
import random

def fitness_function(vec, costs):
    ans = 0
    weight_vec = 0
    for i in range(0, len(vec)):
        ans += vec[i]*costs[i]
    return ans

def check_weight(vec, W, weights):
    weight_vec = W + 1
    while (weight_vec > W):
        weight_vec = 0
        index_obj = []
        for i in range(0, len(vec)):
            if vec[i] == 1:
                index_obj.append(i)
                weight_vec += weights[i]
        if weight_vec > W:
            index_del = random.choice(index_obj)
            vec[index_del] = 0
            weight_vec -= weights[index_del]
    return vec



def knapsack(W, costs, weights):
    n = 400  # размер популяции
    count_obj = len(costs)
    # создание популяции
    population = []
    for i in range(0, n):
        life = []
        for j in range(0, count_obj):
            life.append(randint(0, 1))

        life = check_weight(life, W, weights)
        population.append(life)

    for i in range(50):
        fitnesses = [fitness_function(i, costs) for i in population]
        indexes = [i for i in range(n)]
        x = zip(fitnesses, indexes)
        xs = sorted(x, key=lambda tup: tup[0], reverse=True)
        fitnesses_sorted = [x[0] for x in xs]
        indexes_sorted = [x[1] for x in xs]

        # selection for crossover and crossover
        new_population = []

        for i in range(n//2):
            rand_numb_1 = randint(1, 100)
            if (rand_numb_1 <= 50):
                parent_1 = population[random.choice(indexes_sorted[:n//4])]
            if (51 <= rand_numb_1 <= 80):
                parent_1 = population[random.choice(indexes_sorted[n//4 : n//2])]
            if (81 <= rand_numb_1 <= 95):
                parent_1 = population[random.choice(indexes_sorted[n//2 : 3* (n//4)])]
            if (96 <= rand_numb_1 <= 100):
                parent_1 = population[random.choice(indexes_sorted[3* (n//4):n])]

            rand_numb_2 = randint(1, 100)
            if (rand_numb_2 <= 50):
                parent_2 = population[random.choice(indexes_sorted[:n // 4])]
            if (51 <= rand_numb_2 <= 80):
                parent_2 = population[random.choice(indexes_sorted[n // 4: n // 2])]
            if (81 <= rand_numb_2 <= 95):
                parent_2 = population[random.choice(indexes_sorted[n // 2: 3 * (n // 4)])]
            if (96 <= rand_numb_2 <= 100):
                parent_2 = population[random.choice(indexes_sorted[3 * (n // 4):n])]

            gene = randint(0, count_obj-1)
            child1 = parent_1[0:gene] + parent_2[gene:count_obj]
            child2 = parent_2[0:gene] + parent_1[gene:count_obj]
            child1 = check_weight(child1, W, weights)
            child2 = check_weight(child2, W, weights)
            new_population.append(child1)
            new_population.append(child2)

        #mutation
        for chrom in new_population:
            for gene in chrom:
                mutation_val = randint(1,10)
                if (mutation_val <= 3):
                    gene = (gene + 1) % 2

        population = new_population.copy()
    return population[indexes_sorted[0]]
