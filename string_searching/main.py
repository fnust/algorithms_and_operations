import time
import openpyxl


def naive(text: str, words: str) -> list:
    counter = 0
    len_text = len(text)
    len_words = len(words)
    for i in range(len_text - len_words + 1):
        for j in range(len_words):
            counter += 1
            if words[j] != text[i + j]:
                break
            if j == len_words - 1:
                return [i, counter]
    return [-1, counter]


def boyer_moore_horspool(text: str, words: str) -> list:
    counter = 0
    len_text = len(text)
    len_words = len(words)
    symbols = {words[len_words - 1]: len_words, 'end': len_words}
    for i in range(len_words - 1):
        symbols[words[i]] = len_words - 1 - i

    i = len_words - 1
    j = len_words - 1
    while j <= len_text - 1:
        counter += 1
        if words[i] == text[j]:
            i -= 1
            j -= 1
            if i == 0:
                return [j, counter]
        elif text[j] in words:
            i = len_words - 1
            j += symbols[text[j]]
        else:
            i = len_words - 1
            j += symbols['end']
    return [-1, counter]


def knuth_morris_pratt(text: str, words: str) -> list:
    counter = 0
    len_text = len(text)
    len_words = len(words)
    prefix = [0] * len_words
    j = 0
    for i in range(1, len_words):
        counter += 1
        if words[i] == words[j]:
            prefix[i] = j + 1
            j += 1
        else:
            j = 0

    i = 0
    j = 0

    while i < len_text:
        counter += 1
        if words[j] == text[i]:
            i += 1
            j += 1
            if j == len_words:
                return [i - len_words, counter]
        elif j > 0:
            j = prefix[j - 1]
        else:
            i += 1

    return [-1, counter]


if __name__ == '__main__':
    exel = openpyxl.load_workbook('results.xlsx')
    sheet = exel.active
    sheet['B1'] = 'naive'
    sheet['C1'] = 'boyer_moore_horspool'
    sheet['D1'] = 'knuth_morris_pratt'

    sheet['H1'] = 'naive'
    sheet['I1'] = 'boyer_moore_horspool'
    sheet['J1'] = 'knuth_morris_pratt'
    for i in range(4):
        with open(f'benchmarks/good_t_{i + 1}.txt', 'r', encoding='utf8') as f_text:
            t = f_text.read()
        with open(f'benchmarks/good_w_{i + 1}.txt', 'r', encoding='utf8') as w_text:
            w = w_text.read()
        print(f'----- case: good {i + 1} -----')
        print('len text =', len(t))
        print('len words =', len(w))
        print()
        sheet[f'A{i + 2}'] = f'good {i + 1}'
        sheet[f'G{i + 2}'] = f'good {i + 1}'

        print('naive:')
        start_time = time.perf_counter()
        output = naive(t, w)
        end_time = time.perf_counter()
        print('time = %f seconds' % (end_time - start_time))
        print('count =', output[1])
        print('result =', output[0])
        print()
        sheet[f'B{i + 2}'] = output[1]
        sheet[f'H{i + 2}'] = end_time - start_time

        print('boyer_moore_horspool:')
        start_time = time.perf_counter()
        output = boyer_moore_horspool(t, w)
        end_time = time.perf_counter()
        print('time = %f seconds' % (end_time - start_time))
        print('count =', output[1])
        print('result =', output[0])
        print()
        sheet[f'C{i + 2}'] = output[1]
        sheet[f'I{i + 2}'] = end_time - start_time

        print('knuth_morris_pratt:')
        start_time = time.perf_counter()
        output = knuth_morris_pratt(t, w)
        end_time = time.perf_counter()
        print('time = %f seconds' % (end_time - start_time))
        print('count =', output[1])
        print('result =', output[0])
        print()
        sheet[f'D{i + 2}'] = output[1]
        sheet[f'J{i + 2}'] = end_time - start_time

    for i in range(4):
        with open(f'benchmarks/bad_t_{i + 1}.txt', 'r', encoding='utf8') as f_text:
            t = f_text.read()
        with open(f'benchmarks/bad_w_{i + 1}.txt', 'r', encoding='utf8') as w_text:
            w = w_text.read()
        print(f'----- case: bad {i + 1} -----')
        print('len text =', len(t))
        print('len words =', len(w))
        print()
        sheet[f'A{i + 6}'] = f'bad {i + 1}'
        sheet[f'G{i + 6}'] = f'bad {i + 1}'

        print('naive:')
        start_time = time.perf_counter()
        output = naive(t, w)
        end_time = time.perf_counter()
        print('time = %f seconds' % (end_time - start_time))
        print('count =', output[1])
        print('result =', output[0])
        print()
        sheet[f'B{i + 6}'] = output[1]
        sheet[f'H{i + 6}'] = end_time - start_time

        print('boyer_moore_horspool:')
        start_time = time.perf_counter()
        output = boyer_moore_horspool(t, w)
        end_time = time.perf_counter()
        print('time = %f seconds' % (end_time - start_time))
        print('count =', output[1])
        print('result =', output[0])
        print()
        sheet[f'C{i + 6}'] = output[1]
        sheet[f'I{i + 6}'] = end_time - start_time

        print('knuth_morris_pratt:')
        start_time = time.perf_counter()
        output = knuth_morris_pratt(t, w)
        end_time = time.perf_counter()
        print('time = %f seconds' % (end_time - start_time))
        print('count =', output[1])
        print('result =', output[0])
        print()
        sheet[f'D{i + 6}'] = output[1]
        sheet[f'J{i + 6}'] = end_time - start_time

    exel.save('results.xlsx')
