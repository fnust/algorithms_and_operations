from simulated_annealing import init_params, get_init_res, cycle


def algorithm(machines_lst: list, m: int, p: int):
    parts_lst = [[] for _ in range(p)]
    count_clusters = 2
    best_count_clusters = count_clusters

    for i in range(m):
        for part in machines_lst[i]:
            parts_lst[part].append(i)

    cur_res = get_init_res(machines_lst, parts_lst, m, p, count_clusters)
    best_res_count_cell = cur_res.copy()
    best_res_far = cur_res.copy()

    d = 5
    t_f = 1
    check = 10

    counter, counter_mc, counter_trapped, counter_stagnant, t, alpha, l = init_params(p * m)
    # print(t, alpha, l)

    while True:
        counter_mc, counter_trapped, counter_stagnant, \
        cur_res, best_res_count_cell = cycle(counter, counter_mc, counter_trapped, counter_stagnant, l, d, t,
                                             cur_res,
                                             best_res_count_cell, machines_lst, parts_lst, m, p, count_clusters)
        print('---', cur_res[0], count_clusters, '---')
        # print(t, counter_stagnant)
        if t > t_f and counter_stagnant <= check:
            t = t * alpha
            counter_mc = 0
            counter += 1
            continue

        if best_res_count_cell[0] > best_res_far[0]:
            best_res_far = best_res_count_cell.copy()
            best_count_clusters = count_clusters
            count_clusters += 1

            cur_res = get_init_res(machines_lst, parts_lst, m, p, count_clusters)
            counter, counter_mc, counter_trapped, counter_stagnant, t, alpha, l = init_params(p * m)
        else:
            break

    return best_res_far


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

            result = algorithm(machines, mach, par)
            print(result[0])

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
                for r in result[2]:
                    num += 1
                    if num != par + 1:
                        print(r, file=f_out, end=f' p{num}_')
                    else:
                        print(r, file=f_out)

