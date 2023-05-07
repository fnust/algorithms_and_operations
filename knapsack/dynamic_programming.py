def findAns(weights, table, k, s):
    if table[k][s] == 0:
        return
    if table[k - 1][s] == table[k][s]:
        findAns(weights, table, k - 1, s)
    else:
        findAns(weights, table, k - 1, s - weights[k - 1])
        ans_alg[k - 1] = 1


def dynamic_programming(W, cost, weights):
    n = len(cost)
    count_operations = 0
    global ans_alg
    ans_alg = [0 for i in range(0, n)]
    table = [[0 for x in range(W + 1)] for x in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, W + 1):
            count_operations += 1
            if weights[i - 1] <= j:
                table[i][j] = max(cost[i - 1] + table[i - 1][j - weights[i - 1]], table[i - 1][j])
            else:
                table[i][j] = table[i - 1][j]

    findAns(weights, table, n, W)

    sum_weight = 0
    for i in range(n):
        if ans_alg[i] == 1:
            sum_weight += weights[i]
    return ans_alg, table[n][W], sum_weight, count_operations
