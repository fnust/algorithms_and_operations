def quality_greed(W, cost, weights):
    vec = [0 for i in range(0, len(cost))]
    qual = []
    num_item = 0
    for item_cost, item_weight in zip(cost, weights):
        qual.append((item_cost / item_weight, item_weight, item_cost, num_item))
        num_item += 1
    qual.sort(reverse=True)
    weight = 0
    val = 0
    for it, item_weight, item_cost, num in qual:
        if weight + item_weight <= W:
            vec[num] = 1
            weight += item_weight
            val += item_cost
    return vec, val


def profit_greed(W, cost, weights):
    vec = [0 for i in range(0, len(cost))]
    prof = []
    num_item = 0
    for item_cost, item_weight in zip(cost, weights):
        prof.append((item_cost, item_weight, num_item))
        num_item += 1
    prof.sort(reverse=True)
    weight = 0
    val = 0
    for item_cost, item_weight, num in prof:
        if weight + item_weight <= W:
            vec[num] = 1
            weight += item_weight
            val += item_cost
    return vec, val


def two_approx(W, cost, weights):
    count_operations = len(cost) * (len(cost) - 1) // 2
    qual_greed_vec, qual_greed_ans = quality_greed(W, cost, weights)
    prof_greed_vec, prof_greed_ans = profit_greed(W, cost, weights)
    if qual_greed_ans > prof_greed_ans:
        sum_weight = 0
        for i in range(len(cost)):
            if qual_greed_vec[i] == 1:
                sum_weight += weights[i]
        return qual_greed_vec, qual_greed_ans, sum_weight, count_operations
    else:
        sum_weight = 0
        for i in range(len(cost)):
            if prof_greed_vec[i] == 1:
                sum_weight += weights[i]
        return prof_greed_vec, prof_greed_ans, sum_weight, count_operations
