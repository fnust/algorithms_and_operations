def calculate(distance: list, flow: list, res: list):
    count = len(distance)
    sum_d = 0

    for i in range(count):
        for j in range(count):
            sum_d += distance[i][j] * flow[res[i]][res[j]]
    # print(sum_d)

    return sum_d


def swap_and_recalculate(distance: list, flow: list, res: list, k: int, m: int, sum_d: int):
    new_res = res.copy()
    new_res[k], new_res[m] = res[m], res[k]
    count = len(distance)

    delta = 0
    for i in range(count):
        if i != new_res[m] or i != new_res[k]:
            delta += (flow[new_res[m]][new_res[i]] - flow[new_res[k]][new_res[i]]) * (distance[m][i] - distance[k][i])

    # print(delta1, 2 * delta2)
    return new_res, sum_d + 2 * delta


def look_search(distance: list, flow: list, result: list):
    count = len(distance)

    value = calculate(distance, flow, result)
    # print(value)
    dont_look_bits = [0] * count
    k = 0

    while k < count:
        if dont_look_bits[k] == 1:
            k += 1
            continue

        improvement = False
        for m in range(count):
            if m != k:
                new_result, new_value = swap_and_recalculate(distance, flow, result, k, m, value)

                if new_value < value:
                    # print(new_value)
                    result = new_result
                    value = new_value
                    improvement = True
                    dont_look_bits[k] = 0
                    k = 0
                    break

        if not improvement:
            dont_look_bits[k] = 1

        k += 1
    return value, result
