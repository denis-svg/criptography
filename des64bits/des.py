from random import randint

# Generating keys
pc1 = [
    57, 49, 41, 33, 25, 17, 9, 1,
    58, 50, 42, 34, 26, 18, 10, 2,
    59, 51, 43, 35, 27, 19, 11, 3,
    60, 52, 44, 36, 63, 55, 47, 39,
    31, 23, 15, 7, 62, 54, 46, 38,
    30, 22, 14, 6, 61, 53, 45, 37,
    29, 21, 13, 5, 28, 20, 12, 4,
]
left_shift_schedule = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

pc2 = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]


def generate64bitMatrix():
    return [randint(0, 1) for i in range(64)]


def permutation(matrix: list, permutation_list: list):
    permuted_matrix = []
    for index_bit in permutation_list:
        permuted_matrix.append(matrix[index_bit - 1])

    return permuted_matrix


def performLeftShift(matrix: list, n: int):
    shifted_matrix = matrix[n:] + matrix[:n]
    return shifted_matrix


def splitMatrixHalf(matrix: list):
    matrix_length = len(matrix)
    split_point = matrix_length // 2
    left_half = matrix[:split_point]
    right_half = matrix[split_point:]

    return left_half, right_half


def generate16Keys(key: list):
    keypermuted = permutation(key, pc1)
    left_shifts_rounds = {}
    for i in range(16):
        previous_c, previous_d = [], []
        if i == 0:
            previous_c, previous_d = splitMatrixHalf(keypermuted)
        else:
            previous_c, previous_d = left_shifts_rounds[str(
                i - 1)]["c"], left_shifts_rounds[str(i - 1)]["d"]
        left_shifts_rounds[str(i)] = {
            "c": performLeftShift(previous_c, left_shift_schedule[i]),
            "d": performLeftShift(previous_d, left_shift_schedule[i])
        }
    final_keys = {}
    for key in left_shifts_rounds.keys():
        key48bit = permutation(
            left_shifts_rounds[key]['c'] + left_shifts_rounds[key]['d'], pc2)
        final_keys[key] = key48bit

    return final_keys


# Encrypting
ip_matrix = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

ip_1_matrix = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]


e_bit_selection_table = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

# https://en.wikipedia.org/wiki/DES_supplementary_material
s_boxes = {}
s_boxes["1"] = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]
s_boxes["2"] = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
]
s_boxes["3"] = [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
]
s_boxes["4"] = [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
]
s_boxes["5"] = [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
]
s_boxes["6"] = [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
]
s_boxes["7"] = [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
]
s_boxes["8"] = [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]

P = [
    16, 7, 20, 21, 
    29, 12, 28, 17,    
    1, 15, 23, 26, 
    5, 18, 31, 10,   
    2, 8, 24, 14, 
    32, 27, 3, 9,    
    19, 13, 30, 6, 
    22, 11, 4, 25
    ]


def round(l: list, r: list, key: list):
    """
    L<sub>n</sub> = R<sub>n - 1</sub>
    R<sub>n</sub> = L<sub>n - 1</sub> + f(R<sub>n - 1</sub>, K<sub>n</sub>)
    Let + denote XOR addition
    """
    def f(r: list, k: list):
        # expand r to 48 bits E(r)
        step1 = permutation(r, e_bit_selection_table)
        # E(r) + k
        step2 = xor(step1, k)
        # E(r) + k = B1, B2, B3, B4, B5, B6, B7, B8
        # S(B1), S(B2), S(B3), S(B4), S(B5), S(B6), S(B7), S(B8)
        step3 = []
        s_box_index = 0
        for i in range(0, len(step2), 6):
            group = step2[i:i+6]
            # Convert first + last bit into decimal
            i_index = int(str(group[0]) + str(group[5]), 2)
            j_index = int(str(group[1]) + str(group[2]) +
                          str(group[3]) + str(group[4]), 2)
            bin_string = format(
                s_boxes[str(s_box_index + 1)][i_index][j_index], '04b')
            s_box_index += 1
            for bit in bin_string:
                step3.append(int(bit))
        # apply a permutation p
        return permutation(step3, P)
    next_l = r
    next_r = xor(l, f(r, key))

    return next_l, next_r

def xor(matrix1: list, matrix2: list):
    result = []
    for bit1, bit2 in zip(matrix1, matrix2):
        result.append(bit1 ^ bit2)  # Use the ^ operator for XOR
    return result

def apply16Rounds(m:list, keys:dict, decrypt=False):
    ip = permutation(m, ip_matrix)
    l, r = splitMatrixHalf(ip)
    if decrypt:
        for i in range(15, -1, -1):
            l, r = round(l, r, keys[str(i)])
    if not decrypt:
        for i in range(16):
            l, r = round(l, r, keys[str(i)])
    
    return permutation(r + l, ip_1_matrix) # reverse the order of l and r

def binMatrixToHexStr(bin_matrix):
    bin_string = ''.join(map(str, bin_matrix))
    integer_value = int(bin_string, 2)
    hexadecimal_string = hex(integer_value)
    return hexadecimal_string[2:]

if __name__ == '__main__':
    key = [
        0, 0, 0, 1, 0, 0, 1, 1,
        0, 0, 1, 1, 0, 1, 0, 0,
        0, 1, 0, 1, 0, 1, 1, 1,
        0, 1, 1, 1, 1, 0, 0, 1,
        1, 0, 0, 1, 1, 0, 1, 1,
        1, 0, 1, 1, 1, 1, 0, 0,
        1, 1, 0, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 0, 0, 0, 1
    ]
    keys = generate16Keys(key)
    m = [
        0, 0, 0, 0, 0, 0, 0, 1,
        0, 0, 1, 0, 0, 0, 1, 1,
        0, 1, 0, 0, 0, 1, 0, 1,
        0, 1, 1, 0, 0, 1, 1, 1,
        1, 0, 0, 0, 1, 0, 0, 1,
        1, 0, 1, 0, 1, 0, 1, 1,
        1, 1, 0, 0, 1, 1, 0, 1,
        1, 1, 1, 0, 1, 1, 1, 1
    ]
    encrypted = apply16Rounds(apply16Rounds(m, keys, decrypt=False), keys, decrypt=True)
    for i in range(0, len(encrypted), 8):
        group = encrypted[i:i+8]
        print(group)

    # for testing
    # http://des.online-domain-tools.com/
    print(binMatrixToHexStr(m))
    print(binMatrixToHexStr(key))
    print(binMatrixToHexStr(apply16Rounds(m, keys, decrypt=False)))
    
