# -*- coding: utf8 -*-
from numpy import *
import numpy as np
from termcolor import colored


def color_pick(i):
    """Выбираем цвет"""
    color = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white', 'grey']
    index = i - int(i / 8) * 8
    return color[index]


def read_data(_fname):
    """Чтение файла"""

    # открытие файла
    with open(_fname + ".dat") as ifs:
        lines = ifs.readlines()

    # кол. деталей
    lines[0].split()
    _n = int(lines[0][0])

    # создание пустых списков
    _det = empty((_n, 4), dtype=int)

    # считывание и формирование СЛАУ
    for i in range(_n):
        lines[i] = lines[i + 1].split()
        for j in range(3):
            _det[i, j] = int(lines[i][j])

    for i in range(_n):
        _det[i, 3] = i + 1

    return _det


def print_list_2(_det):
    """Вывод"""
    print("d\t\t e\t\t N%")

    for i in range(len(_det)):
        print("\t\t".join([colored(str(round(k, 10)), color_pick(i)) for k in _det[i]]))
    print("")


def print_list_3(_det):
    """Вывод"""
    print("a\t\t b\t\t c\t\t N%")

    for i in range(len(_det)):
        print("\t\t".join([colored(str(round(k, 10)), color_pick(i)) for k in _det[i]]))
    print("")


def write_data_3(_seq):
    """Запись результата в виде графика Ганта и цветной вывод"""

    ofs = open("ans.dat", "w")

    x = []
    y = []
    a = []
    b = []
    c = []

    # формирование a, b, c
    for i in range(len(_seq)):
        a.append(_seq[i, 0])
        b.append(_seq[i, 1])
        c.append(_seq[i, 2])

    x.append(_seq[0, 0])
    y.append(_seq[0, 0] + _seq[0, 1])

    # запись в файл результатов 1 станка
    for i in range(len(_seq)):
        for j in range(_seq[i, 0]):
            ofs.write(str(_seq[i, 3]) + " ")
            print(colored(str(_seq[i, 3]) + " ", color_pick(i)), end=" ")

    ofs.write("\n")
    print("")

    # подсчет простоя 2 станка
    for i in range(1, len(_seq)):
        suma = 0
        for sa in range(i + 1):
            suma += a[sa]

        sumb = 0
        for sb in range(i):
            sumb += b[sb]

        sumx = 0
        for sx in range(i):
            sumx += x[sx]

        x.append(max(suma - sumx - sumb, 0))

    # запись рузультатов 2 станка
    for i in range(len(_seq)):
        for j in range(x[i]):
            ofs.write("  ")
            print(colored("  ", color_pick(i)), end=" ")

        for k in range(_seq[i, 1]):
            ofs.write(str(_seq[i, 3]) + " ")
            print(colored(str(_seq[i, 3]) + " ", color_pick(i)), end=" ")

    ofs.write("\n")
    print("")

    # подсчет простоя 3 станка
    for i in range(1, len(_seq)):
        sumb = 0
        for sb in range(i + 1):
            sumb += b[sb]

        sumx = 0
        for sx in range(i + 1):
            sumx += x[sx]

        sumc = 0
        for sc in range(i):
            sumc += c[sc]

        sumy = 0
        for sy in range(i):
            sumy += y[sy]

        y.append(max(sumx + sumb - sumy - sumc, 0))

    # запись рузультатов 3 станка
    for i in range(len(_seq)):
        for j in range(y[i]):
            ofs.write("  ")
            print(colored("  ", color_pick(i)), end=" ")

        for k in range(_seq[i, 2]):
            ofs.write(str(_seq[i, 3]) + " ")
            print(colored(str(_seq[i, 3]) + " ", color_pick(i)), end=" ")

    ofs.write("\n")
    print("")

    _X = sum(x)  # сумарный простой второго станка X
    print("Суммарный простой второго станка: " + colored(str(_X), color_pick(7)))
    _Y = sum(y)  # сумарный простой третьего станка Y
    print("Суммарный простой третьего станка: " + colored(str(_Y), color_pick(7)))


def min_detail(_det):
    """Поиск минимального в списке деталей"""

    m = _det[0, 0]
    ind_m = [0, 0]

    for i in range(len(_det)):
        for j in range(2):
            if _det[i, j] <= m:
                m = _det[i, j]
                ind_m = [i, j]

    return ind_m


def delete_row(_det, _i):
    """Удаление строки"""
    _det = np.delete(_det, _i, axis=0)
    return _det


def add_seq(_det, _seq, _ind, _place_a, _place_b):
    """Добавление в последовательность"""

    # добавляем в начало последовательности
    if _ind[1] == 0:
        _seq[_place_a] = _det[_ind[0]]
        _place_a += 1
    # добавляем в конец последовательности
    elif _ind[1] == 1:
        _seq[_place_b] = _det[_ind[0]]
        _place_b -= 1

    return _seq, _place_a, _place_b


def method_conditions(_det):
    """Проверка условия для задачи"""
    a = []
    b = []
    c = []

    # формирование a, b, c
    for i in range(len(_det)):
        a.append(_det[i, 0])
        b.append(_det[i, 1])
        c.append(_det[i, 2])

    if min(a) >= min(b) or min(c) >= min(b):
        return True
    else:
        return False


def merge_details(_det):
    """Получение E и D"""
    _seq = empty((len(_det), 3), dtype=int)

    for i in range(len(_det)):
        _seq[i, 0] = _det[i, 0] + _det[i, 1]
        _seq[i, 1] = _det[i, 1] + _det[i, 2]
        _seq[i, 2] = _det[i, 3]

    return _seq


def create_seq_2(_det):
    """Создание последовательности"""
    _seq = empty((len(_det), 3), dtype=int)
    _pa = 0
    _pb = len(_det) - 1

    for i in range(len(_det)):
        _ind = min_detail(_det)
        _seq, _pa, _pb = add_seq(_det, _seq, _ind, _pa, _pb)
        _det = delete_row(_det, _ind[0])

    return _seq


def create_seq_3(_det, _seq_2):
    """Создание последовательности"""
    _seq = empty((len(_det), 4), dtype=int)

    for i in range(len(_det)):
        _seq[i] = _det[_seq_2[i, 2] - 1]

    return _seq


def main():
    """Основная функция"""

    file_name = input("Введите номер примера: ")
    details = read_data(file_name)

    print("Детали их время на обработку: ")
    print_list_3(details)
    print("")

    if method_conditions(details):
        sequence = create_seq_2(merge_details(details))
        print("Полученная оптимальная последовательность: ")
        print_list_2(sequence)
        print("")

        main_sequence = create_seq_3(details, sequence)
        print("Полученный график Ганта для данной задачи: ")
        write_data_3(main_sequence)
    else:
        print("Условия на поиск оптимального не выполнен!")


if __name__ == '__main__':
    main()
