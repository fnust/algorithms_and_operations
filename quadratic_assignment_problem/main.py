import time
from local_search import look_search, calculate
from iterated_local_search import iterated_local_search


def time_and_answer(algorithm, distance: list, flow: list):
    all_time = 0
    count_experiments = 5
    results = []
    values = []
    count = len(distance)

    for exp in range(count_experiments):
        start = time.time()
        res = list(range(count))
        val, res = algorithm(distance, flow, res)
        end = time.time()

        results.append(res)
        values.append(val)

        all_time += end - start
    print('time = ', all_time / count_experiments)
    return values, results


files = ['tai20a', 'tai40a', 'tai60a', 'tai80a', 'tai100a']
algorithms = [look_search, iterated_local_search]

for file in files:
    for alg in algorithms:
        with open(f'test/{file}') as f:
            data = f.read().splitlines()
            distances = []
            flows = []
            n = int(data[0])
            for line in range(1, n + 1):
                distances.append(list(map(int, data[line].split())))

            for line in range(n + 2, 2 * n + 2):
                flows.append(list(map(int, data[line].split())))

            print(file, alg.__name__)
            total_val, total_res = time_and_answer(alg, distances, flows)
            print(min(total_val))

            with open(f'results/{alg.__name__}/{file}.sol', 'a+') as fout:
                print(' '.join(list(map(str, total_res))), file=fout)
