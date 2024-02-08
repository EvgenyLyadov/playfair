import collections
import random
import math
import copy
from enc import *

# не используем

#вычисление частот букв
def freq(string):
    letters_cr = dict(collections.Counter(string))
    # print(letters_cr)
    alphabet = letters_cr.keys()
    summa = 0
    for ltr in alphabet:
        summa += letters_cr[ltr]
    # print(summa)
    for ltr in alphabet:
        letters_cr[ltr] = letters_cr[ltr] / summa
    # print(letters_cr)
    return letters_cr


# не используем
def hi(basic_fr, this_fr):
    alphabet = this_fr.keys()
    val = 0
    for letter in alphabet:
        val += math.log10(basic_fr[letter] * this_fr[letter])
    return val

# не используем
def Prob(hi_old, hi_new, temperature):
    # print(hi_old, hi_new, temperature)
   # math.exp(-(hi_old - hi_new) / temperature)
    probs = math.exp((hi_new - hi_old) / temperature)
    # print("probs = ", probs)
    return probs

#перестановка случайных столбцов
def swap_columns(matrix, col1=random.randint(0, 4), col2=random.randint(0, 4)):
    key_mtrx = copy.deepcopy(matrix)
    for row in matrix:
        row[col1], row[col2] = row[col2], row[col1]
    return key_mtrx

#перестановка случайных строк
def swap_rows(matrix, row1=random.randint(0, 4), row2=random.randint(0, 4)):
    key_mtrx = copy.deepcopy(matrix)
    matrix[row1], matrix[row2] = matrix[row2], matrix[row1]
    return key_mtrx


def reverse_rows(matrix):
    key_mtrx = copy.deepcopy(matrix)
    for row in key_mtrx:
        row.reverse()
    return key_mtrx


def reverse_columns(key_mtrx):
    matrix = copy.deepcopy(key_mtrx)

    num_rows = len(matrix)
    num_cols = len(matrix[0]) if matrix else 0

    for col in range(num_cols):
        column_values = [matrix[row][col] for row in range(num_rows)]
        column_values.reverse()

        for row in range(num_rows):
            matrix[row][col] = column_values[row]

    return matrix
 
 

def reverse_matrix(key_mtrx):
    matrix = copy.deepcopy(key_mtrx)

    # Переворачиваем строки матрицы
    matrix.reverse()

    # Переворачиваем значения в каждой строки матрицы
    for row in matrix:
        row.reverse()
    return matrix


def print_matrix(matrix):
    for row in matrix:
        for item in row:
            print(item, end='\t')
        print()

#функция изменения ключа
def change_key(mtrx_key):

    key_mtrx = copy.deepcopy(mtrx_key)

    x1 = random.randint(0, 4)
    y1 = random.randint(0, 4)

    x2 = random.randint(0, 4)
    y2 = random.randint(0, 4)

    while (x1 == x2 and y1 == y2):
        x2 = random.randint(0, 4)
        y2 = random.randint(0, 4)
    tmp = key_mtrx[x1][y1]
    key_mtrx[x1][y1] = key_mtrx[x2][y2]
    key_mtrx[x2][y2] = tmp

    return key_mtrx

# функция для оценки текста
def function_quality(d_quadrams, text, total_sum):
    qual_mark = 0
    for i in range(0, len(text)-3):
        # print(text[i:i+4])
        if text[i:i+4] in d_quadrams:
            k_vak = math.log10(d_quadrams[text[i:i+4]] / total_sum)
        else:
            k_vak = math.log10(1 / total_sum)
        # print("log10 = ", k_vak)
        qual_mark += k_vak
    return qual_mark


f = open("book1.txt", 'r')
text = f.read()
out_text = ''.join(e for e in text if e.isalnum() and not e.isnumeric())
first_text = out_text #исходный текст, преобразованный для шифра
letters = dict(collections.Counter(out_text))
key = "password" #ключ шифрования
matrix_key = matrix(key)

print_matrix(matrix_key)
f.close()

text = str(encrypt(out_text, matrix_key))
out_text = ''.join(e for e in text if e.isalnum() and not e.isnumeric())

f = open("playfair.txt", 'w')
f.write(out_text)
f.close()


# пытаемся расшифровать матрицу рандномным ключом

key_rand = 'rfclkjfg'
matrix_key_rand = matrix(key_rand)

f = open("playfair.txt", 'r')
text = f.read()
out_text = ''.join(e for e in text if e.isalnum() and not e.isnumeric())

# print(out_text[0:50])
dc_tx = decrypt(out_text, matrix_key_rand)
# old_freq = freq(dc_tx)
# old_hi = hi(basic_freq, old_freq)
# print(dt[0:50])
f.close()


d_quadrams = {}
total_sum = 0
with open("4grams.txt") as f:
    for line in f:
        (key, val) = line.split()
        d_quadrams[key] = int(val)
        total_sum += int(val)

# test = "HAPPYDAYSNZQZ"
# mrks = function_quality(d_quadrams, test)
# print(mrks)


T_0 = 1

best_hi = -10000000000000000
best_text = ""

old_hi = function_quality(d_quadrams, dc_tx, total_sum)
while T_0 >= 1:
    for i in range(0, 50000):
        # мы должны рандомно выбрать способ изменения
        selected_function = random.choices([change_key, swap_columns, swap_rows, reverse_rows,
                                            reverse_columns, reverse_matrix], weights=[100, 0, 0, 0, 0, 0], k=1)[0]
        iter_matrix_key_rand = selected_function(matrix_key_rand)

        dc_tx = decrypt(out_text, iter_matrix_key_rand)
        new_hi = function_quality(d_quadrams, dc_tx, total_sum)
        dF = new_hi - old_hi
        print("new = ", new_hi, "old = ", old_hi)
        print("dF = ", dF)
        #если новый ключ лучше
        if dF >= 0:
            print("ABBOBA")
            old_hi = new_hi
            matrix_key_rand = copy.deepcopy(iter_matrix_key_rand)
        else:
            prob_iter = math.exp(dF / T_0)
            print(dF)
           # if prob_iter > random.random():
            if dF > (-1)*random.randrange(0,100)/i:
                print("abobba")
                old_hi = new_hi
                print("=== abb === ","new = ", new_hi, "old = ", old_hi)
                matrix_key_rand = copy.deepcopy(iter_matrix_key_rand)

        if old_hi > best_hi:
            best_hi = old_hi
            best_text = dc_tx
            best_key = copy.deepcopy(matrix_key_rand)
            print("NEW BEST = ", best_hi)

    T_0 = T_0 - 1
    print("T_0 = ", T_0)


# print(matrix_key)
# print(matrix_key_rand)

print(best_hi)
print(best_key)
print(first_text[0:50])
print(best_text[0:50])
# # print(old_hi)
