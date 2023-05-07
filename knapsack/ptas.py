import itertools


def weight_and_cost_of_set(items: set, weights: list, costs: list) -> [int, int]:
    weight = 0
    cost = 0

    for i in items:
        weight += weights[i]
        cost += costs[i]

    return weight, cost


def transform(items: set, size: int) -> list:
    result = [0] * size
    for i in items:
        result[i] = 1
    return result


def ptas(w: int, costs: list, weights: list, k: int = 3) -> [list, int, int, int]:
    results = []
    n = len(costs)
    all_m = []

    for i in range(k + 1):
        all_m += list(itertools.combinations(range(n), i))
    for m in all_m:
        m = set(m)
        cur_weight, cur_cost = weight_and_cost_of_set(m, weights, costs)
        if cur_weight < w:
            not_in_m = set(range(n)) - m
            cur_set = m
            for i in not_in_m:
                if cur_weight + weights[i] <= w:
                    cur_weight += weights[i]
                    cur_cost += costs[i]
                    cur_set.add(i)
                else:
                    break
            results.append({'items': cur_set, 'cost': cur_cost, 'weight': cur_weight})
        elif cur_weight == w:
            results.append({'items': m, 'cost': cur_cost, 'weight': cur_weight})

    results = sorted(results, key=lambda x: x['cost'], reverse=True)
    result = results[0]
    return transform(result['items'], n), result['cost'], result['weight'], len(results)

