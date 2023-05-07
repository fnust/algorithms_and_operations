def branch_and_bound(w: int, costs: list, weights: list): # -> [list, int, int, int]:
    items = []
    for i in range (len(costs)):
        items.append(tuple([costs[i], weights[i]]))

    items = sorted(items, key=lambda x: x[1]/x[0], reverse=True)
    len_items = len(items)
    max_cost = 0
    num_opns = 0

    stack = [(0, 0, w, 0)]
    sum_weights = 0
    # curr_items = set()

    while stack:
        i, curr_cost, curr_weight, bound = stack.pop()

        if i == len_items:
            if curr_cost > max_cost:
                sum_weights = w - curr_weight
                max_cost = curr_cost
            continue

        if items[i][0] <= curr_weight:
            num_opns = num_opns + 1
            with_i = (i + 1, curr_cost+items[i][1], curr_weight - items[i][0], bound)
            if with_i[1] + with_i[3] > max_cost:
                stack.append(with_i)
        without_i = (i + 1, curr_cost, curr_weight, bound + items[i][1])

        if without_i[3] > max_cost:
            stack.append(without_i)
        num_opns = num_opns + 1

    return -1, max_cost, sum_weights, num_opns