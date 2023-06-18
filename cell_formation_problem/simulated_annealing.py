import math
from random import random

import pandas as pd
from sklearn.cluster import KMeans

global counter, counter_mc, counter_trapped, counter_stagnant


def clustering_m(machines_lst: list, cluster_parts: list, count_m: int, count_p: int, count: int):
    cluster = []
    temp = [[0 for _ in range(count)] for _ in range(count_m)]
    for i in range(count_m):
        for j in range(count_p):
            temp[i][cluster_parts[j]] += 1 if j not in machines_lst[i] else 0
            for k in range(count):
                if k != cluster_parts[j]:
                    temp[i][k] += 1 if j in machines_lst[i] else 0
        cluster.append(temp[i].index(min(temp[i])))
    return cluster


def clustering_p(machines_lst: list, count_p: int, count: int):
    matrix = []
    for i in range(count_p):
        matrix.append([])
        for j in range(count_p):
            a = len([machine for machine in machines_lst if i in machine and j in machine])
            b = len([machine for machine in machines_lst if i in machine and j not in machine])
            c = len([machine for machine in machines_lst if i not in machine and j in machine])
            matrix[i].append(a / (a + b + c))

    matrix_pd = pd.DataFrame(matrix)
    model = KMeans(n_clusters=count, n_init='auto')

    model.fit(matrix_pd)

    print(count)
    return list(model.predict(matrix_pd))


def count_score(parts_lst: list, count_m: int, count_p: int, cluster_parts: list, cluster_machines: list):
    n_1 = sum([len(i) for i in parts_lst])
    n_1_out = 0
    n_0_in = 0

    for i in range(count_p):
        for j in range(count_m):
            if cluster_parts[i] == cluster_machines[j]:
                n_0_in += 1 if j not in parts_lst[i] else 0
            else:
                n_1_out += 1 if j in parts_lst[i] else 0

    return (n_1 - n_1_out) / (n_1 + n_0_in)


def single_move(machines_lst: list, parts_lst: list, cluster_part: list, count_m: int, count_p: int, count: int):
    clusters = set(cluster_part)
    result = [0, [], []]

    for i in range(count_p):
        for cluster in clusters:
            if cluster != cluster_part[i]:
                temp_cl_p = cluster_part.copy()
                temp_cl_p[i] = cluster
                if len(set(cluster_part)) != count:
                    continue
                temp_cl_m = clustering_m(machines_lst, temp_cl_p, count_m, count_p, count)
                temp_f = count_score(parts_lst, count_m, count_p, temp_cl_p, temp_cl_m)

                if result[0] < temp_f:
                    result = [temp_f, temp_cl_p, temp_cl_m]

    return result


def exchange_move(machines_lst: list, parts_lst: list, cluster_part: list, count_m: int, count_p: int, count: int):
    result = [0, [], []]

    for i in range(count_p):
        for j in range(i + 1, count_p):
            if cluster_part[i] != cluster_part[j]:
                temp_cl_p = cluster_part.copy()
                temp_cl_p[i], temp_cl_p[j] = temp_cl_p[j], temp_cl_p[i]

                temp_cl_m = clustering_m(machines_lst, temp_cl_p, count_m, count_p, count)
                temp_f = count_score(parts_lst, count_m, count_p, temp_cl_p, temp_cl_m)

                if result[0] < temp_f:
                    result = [temp_f, temp_cl_p, temp_cl_m]

    return result


def get_init_res(machines_lst: list, parts_lst: list, count_m: int, count_p: int, count: int):
    cluster_parts = clustering_p(machines_lst, count_p, count)
    cluster_machines = clustering_m(machines_lst, cluster_parts, count_m, count_p, count)
    f_value = count_score(parts_lst, count_m, count_p, cluster_parts, cluster_machines)
    return [f_value, cluster_parts, cluster_machines]


def cycle(n: int, mc: int, counter_t: int, counter_s: int, lib: int, dv: int, cur_t: int, res: list, best_res: list,
          machines_lst: list, parts_lst: list, count_m: int, count_p: int, count: int):
    while mc < lib and counter_t < lib / 2:
        if n % dv != 0:
            new_res = single_move(machines_lst, parts_lst, res[1], count_m, count_p, count)
        else:
            new_res = exchange_move(machines_lst, parts_lst, res[1], count_m, count_p, count)

        if new_res[0] > best_res[0]:
            res = new_res.copy()
            best_res = new_res.copy()
            counter_s = 0
            mc += 1
            continue

        if new_res[0] == best_res[0]:
            res = new_res.copy()
            counter_s += 1
            mc += 1
            continue

        x = random()
        delta = new_res[0] - res[0]
        if math.exp(delta / cur_t) > x:
            res = new_res.copy()
            counter_t = 0
        else:
            counter_t += 1
        mc += 1
    return mc, counter_t, counter_s, res, best_res


def init_params(values_m: int):
    n, mc, counter_t, counter_s = 0, 0, 0, 0
    temp = 30 - min([values_m * 0.03, 10])
    a = min([0.7 + (50 / values_m), 0.9])
    lib = min([5 + math.ceil(8000 / values_m), 20])

    return n, mc, counter_t, counter_s, temp, a, lib
