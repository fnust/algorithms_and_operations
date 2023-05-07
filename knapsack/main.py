import time
import openpyxl as openpyxl
from ptas import ptas
from dynamic_programming import dynamic_programming
from two_approx import two_approx


def time_and_operations(name: str, algorithm, w: int, costs: list, weights: list,
                        sheet: openpyxl.workbook.workbook.Worksheet, case: int, id_al: int) -> None:
    all_time = 0
    count_experiments = 3
    result, cost, weight, count_operations = 0, 0, 0, 0
    for exp in range(count_experiments):
        start = time.perf_counter()
        result, cost, weight, count_operations = algorithm(w, costs, weights)
        end = time.perf_counter()
        all_time += end - start

    print(name + ':')
    print('time = %f seconds' % (all_time / count_experiments))
    print('count operations =', count_operations)
    print('result =', *result)
    print('cost =', cost)
    print('weight =', weight)
    print()

    sheet[f'{chr(66 + id_al)}{case + 1}'] = all_time / count_experiments
    sheet[f'{chr(71 + id_al)}{case + 1}'] = count_operations
    sheet[f'{chr(76 + id_al)}{case + 1}'] = ' '.join(map(str, result))
    sheet[f'{chr(81 + id_al)}{case + 1}'] = cost
    sheet[f'{chr(86 + id_al)}{case + 1}'] = weight


def print_names(sheet: openpyxl.workbook.workbook.Worksheet) -> None:
    for i in range(5):
        sheet[f'{chr(66 + i * 5)}1'] = 'two approx'
        sheet[f'{chr(67 + i * 5)}1'] = 'dynamic programming'
        sheet[f'{chr(68 + i * 5)}1'] = '?'
        sheet[f'{chr(69 + i * 5)}1'] = 'PTAS'


if __name__ == '__main__':
    exel = openpyxl.load_workbook('results.xlsx')
    sheet = exel.active
    print_names(sheet)

    for i in range(1, 8):
        with open(f'test/p0{i}_c.txt') as file:
            w = int(file.read())

        costs = []
        with open(f'test/p0{i}_p.txt') as file:
            for line in file:
                costs.append(int(line))

        weights = []
        with open(f'test/p0{i}_w.txt') as file:
            for line in file:
                weights.append(int(line))

        answer = []
        with open(f'test/p0{i}_s.txt') as file:
            for line in file:
                answer.append(int(line))

        print(f'----- case: {i} -----')
        sheet[f'A{i + 1}'] = f'case {i}'
        time_and_operations('two approx', two_approx, w, costs, weights, sheet, i, 0)
        time_and_operations('dynamic programming', dynamic_programming, w, costs, weights, sheet, i, 1)
        # time_and_operations('name', name, w, costs, weights, sheet, i, 2)
        time_and_operations('PTAS', ptas, w, costs, weights, sheet, i, 3)

    exel.save('results.xlsx')
