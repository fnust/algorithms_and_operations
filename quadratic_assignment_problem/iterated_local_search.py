import random

from local_search import look_search


def stochastic_2opt(result: list, i: int, j: int):
    if i == 0:
        return result[:i] + result[j::-1] + result[j + 1:]

    return result[:i] + result[j:i - 1:-1] + result[j + 1:]


def iterated_local_search(distance: list, flow: list, result: list):
    value, result = look_search(distance, flow, result)

    iteration = 0
    count = len(distance)

    while iteration < 10:
        iteration += 1

        i = random.randint(0, count - 2)
        rnd = i + random.randint(2, count // 2)
        j = rnd if rnd < count else count - 1
        new_result = stochastic_2opt(result, i, j)
        new_value, new_result = look_search(distance, flow, new_result)

        if new_value < value:
            value = new_value
            result = new_result
            iteration = 0

    return value, result
