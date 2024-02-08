# Функция формирования ключа - матрицы
def matrix(key):
    matrix = []
    for e in key.upper():
        if e not in matrix:
            matrix.append(e)
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

    for e in alphabet:
        if e not in matrix:
            matrix.append(e)

    # initialize a new list. Is there any elegant way to do that?
    matrix_group = []
    for e in range(5):
        matrix_group.append('')

    # Break it into 5*5
    matrix_group[0] = matrix[0:5]
    matrix_group[1] = matrix[5:10]
    matrix_group[2] = matrix[10:15]
    matrix_group[3] = matrix[15:20]
    matrix_group[4] = matrix[20:25]
    return matrix_group




# преобразование текста в биграммам для шифрования
def message_to_digraphs(message_original):
    # Change it to Array. Because I want used insert() method
    message = []
    print("Start Bigrams")
    # for e in message_original:
    #     message.append(e)

    # # Delet space
    # for unused in range(len(message)):
    #     if " " in message:
    #         message.remove(" ")
    message = list(message_original)
    # If both letters are the same, add an "X" after the first letter.
    i = 0
    half_len = int(len(message)/2)
    for e in range(half_len):
        if message[i] == message[i+1]:
            message.insert(i+1, 'X')
        i = i+2

    # If it is odd digit, add an "X" at the end
    if len(message) % 2 == 1:
        message.append("X")
    # Grouping
    i = 0
    new = []
    for x in range(1, int(len(message)/2)+1):
        new.append(message[i:i+2])
        i = i+2
  #  print("------- BIGRAMS ARE DONE -----------------")
    return new


#функция нахождения позиции буквы в матрице
def find_position(key_matrix, letter):
    x = y = 0
    for i in range(5):
        for j in range(5):
            if key_matrix[i][j] == letter:
                x = i
                y = j

    return x, y


# функция зашифровывания
def encrypt(message, key_matrix):
    message = message_to_digraphs(message)
    # key_matrix = matrix(key)
    cipher = []
    for e in message:
        p1, q1 = find_position(key_matrix, e[0])
        p2, q2 = find_position(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            cipher.append(key_matrix[p1][q1+1])
            cipher.append(key_matrix[p1][q2+1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1
            if p2 == 4:
                p2 = -1
            cipher.append(key_matrix[p1+1][q1])
            cipher.append(key_matrix[p2+1][q2])
        else:
            cipher.append(key_matrix[p1][q2])
            cipher.append(key_matrix[p2][q1])
    return cipher

#функция разбиения шифра на биграммы
def cipher_to_digraphs(cipher):
    i = 0
    new = []
    for x in range(int(len(cipher)/2)):
        new.append(cipher[i:i+2])
        i = i+2
    return new

#функция расшифрования
def decrypt(cipher, key_matrix):
  #  print("----- STAGE 0 ---------")
    cipher = cipher_to_digraphs(cipher)
    # key_matrix = matrix(key)
    plaintext = []

 #   print("----- STAGE 1 ---------")

    for e in cipher:
        p1, q1 = find_position(key_matrix, e[0])
        p2, q2 = find_position(key_matrix, e[1])
        if p1 == p2:
            if q1 == 4:
                q1 = -1
            if q2 == 4:
                q2 = -1
            plaintext.append(key_matrix[p1][q1-1])
            plaintext.append(key_matrix[p1][q2-1])
        elif q1 == q2:
            if p1 == 4:
                p1 = -1
            if p2 == 4:
                p2 = -1
            plaintext.append(key_matrix[p1-1][q1])
            plaintext.append(key_matrix[p2-1][q2])
        else:
            plaintext.append(key_matrix[p1][q2])
            plaintext.append(key_matrix[p2][q1])

 #  print("----- STAGE 2 ---------")

    # for unused in range(len(plaintext)):
    #     if "X" in plaintext:
    #         plaintext.remove("X")

    # plaintext = plaintext.replace('X', "")
    output = ""
    for e in plaintext:
        if "X" in e:
            e = e.replace('X', "")
        output += e
    return output