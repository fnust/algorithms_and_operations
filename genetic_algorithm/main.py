import time
from knapsack import knapsack
from comm import comm
import xml.etree.ElementTree as ET
import numpy as np

def parsing(filename: str, fill_same: float):
    tree = ET.parse(f'test_comm/{filename}.xml')
    root = tree.getroot()
    graph = root.find('graph')
    matrix = []
    n = len(graph.findall('vertex'))
    for i, ver in enumerate(graph.findall('vertex')):
        matrix.append([fill_same for _ in range(n)])
        for edge in ver.findall('edge'):
            matrix[i][int(edge.text)] = float(edge.get('cost'))
    return matrix


def time_and_answer(alg, W, cost, weights, answer):
    all_time = 0
    count_experiments = 1
    for exp in range(count_experiments):
        start = time.time()
        ans_alg = alg(W, cost, weights)
        end = time.time()

        answer_val = 0
        answer_alg_val = 0
        for i in range(0, len(answer)):
            answer_val += answer[i] * cost[i]
            answer_alg_val += ans_alg[i] * cost[i]
        print(answer_alg_val, answer_val)
        #print(ans_alg, answer)
        all_time += end - start
    print('time = ',all_time / count_experiments)

#knapsack
for i in range(1,8):
    with open(f'test_knapsack/p0{i}_c.txt') as file:
        W = int(file.read())

    cost = []
    with open(f'test_knapsack/p0{i}_p.txt') as file:
        for line in file:
            cost.append(int(line))

    weights = []
    with open(f'test_knapsack/p0{i}_w.txt') as file:
        for line in file:
            weights.append(int(line))

    answer = []
    with open(f'test_knapsack/p0{i}_s.txt') as file:
        for line in file:
            answer.append(int(line))

    time_and_answer(knapsack,W,cost,weights,answer)


# comm
matrix_gr17 = parsing('gr17',0)

start = time.time()
answer_alg = comm(matrix_gr17)
end = time.time()
print(answer_alg[1])
print(f'time = {end - start}')

matrix_att48 = parsing('att48',0)

start = time.time()
answer_alg = comm(matrix_att48)
end = time.time()
print(answer_alg[1])
print(f'time = {end - start}')


matrix_bays29 = parsing('bays29',0)

start = time.time()
answer_alg = comm(matrix_bays29)
end = time.time()
print(answer_alg[1])
print(f'time = {end - start}')


matrix_ch150 = parsing('ch150',0)

start = time.time()
answer_alg = comm(matrix_ch150)
end = time.time()
print(answer_alg[1])
print(f'time = {end - start}')


matrix_a280 = parsing('a280',0)

start = time.time()
answer_alg = comm(matrix_a280)
end = time.time()
print(answer_alg[1])
print(f'time = {end - start}')


matrix_fl417 = parsing('fl417',0)

start = time.time()
answer_alg = comm(matrix_fl417)
end = time.time()
print(answer_alg[1])
print(f'time = {end - start}')






