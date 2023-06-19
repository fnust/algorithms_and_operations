import time
from cell_formation_problem.simulated_annealing import algorithm, count_score


def time_and_answer(machines_lst: list, m: int, p: int):
    all_time = 0
    count_experiments = 3
    results = []

    for exp in range(count_experiments):
        print('exp', exp)
        start = time.time()
        res = algorithm(machines_lst, m, p)
        end = time.time()

        results.append(res)
        all_time += end - start

    print('time = ', all_time / count_experiments)
    return sorted(results, key=lambda x: x[0], reverse=True)[0]


if __name__ == '__main__':
    files = ['20x20.txt', '24x40.txt', '30x50.txt', '30x90.txt', '37x53.txt']
    for file in files:
        with open(f'tests/{file}') as f:
            print(file)
            data = f.read().splitlines()
            mach, par = map(int, data[0].split())
            machines = []
            for line in range(1, mach + 1):
                machines.append(list(map(lambda x: x - 1, map(int, data[line].split())))[1:])

            result = time_and_answer(machines, mach, par)
            print('result =', result[0])
            print('******************************')

            with open(f'results/{file[:-4]}.sol', 'w') as f_out:
                num = 1
                print('m1_', file=f_out, end='')
                for r in result[2]:
                    num += 1
                    if num != mach + 1:
                        print(r, file=f_out, end=f' m{num}_')
                    else:
                        print(r, file=f_out)

                num = 1
                print('p1_', file=f_out, end='')
                for r in result[1]:
                    num += 1
                    if num != par + 1:
                        print(r, file=f_out, end=f' p{num}_')
                    else:
                        print(r, file=f_out)
