def build_playfair_matrix(key):
    key = key.upper()
    matrix = [['' for _ in range(6)] for _ in range(6)]
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZĂÂÎȘȚ'
    key_set = set()

    row, col = 0, 0
    for letter in key:
        if letter not in key_set:
            matrix[row][col] = letter
            key_set.add(letter)
            col += 1
            if col == 6:
                col = 0
                row += 1

    for letter in alphabet:
        if letter != 'J' and letter not in key_set:
            matrix[row][col] = letter
            key_set.add(letter)
            col += 1
            if col == 6:
                col = 0
                row += 1

    return matrix

def find_letter_positions(matrix, letter):
    for i in range(6):
        for j in range(6):
            if matrix[i][j] == letter:
                return (i, j)
    return None

def playfair_encrypt(plain_text, key):
    matrix = build_playfair_matrix(key)
    print(matrix)
    plain_text = plain_text.upper().replace('J', 'I')
    plain_text = ''.join(filter(str.isalnum, plain_text))
    encrypted_text = []

    i = 0
    while i < len(plain_text):
        letter1 = plain_text[i]
        letter2 = ''
        if i + 1 < len(plain_text):
            letter2 = plain_text[i + 1]

        if letter1 == letter2:
            letter2 = 'X'
            i += 1

        (row1, col1) = find_letter_positions(matrix, letter1)
        (row2, col2) = find_letter_positions(matrix, letter2)

        if row1 == row2:
            encrypted_text.append(matrix[row1][(col1 + 1) % 6])
            encrypted_text.append(matrix[row2][(col2 + 1) % 6])
        elif col1 == col2:
            encrypted_text.append(matrix[(row1 + 1) % 6][col1])
            encrypted_text.append(matrix[(row2 + 1) % 6][col2])
        else:
            encrypted_text.append(matrix[row1][col2])
            encrypted_text.append(matrix[row2][col1])

        i += 2

    return ''.join(encrypted_text)

def playfair_decrypt(encrypted_text, key):
    matrix = build_playfair_matrix(key)
    decrypted_text = []

    i = 0
    while i < len(encrypted_text):
        letter1 = encrypted_text[i]
        letter2 = encrypted_text[i + 1]

        (row1, col1) = find_letter_positions(matrix, letter1)
        (row2, col2) = find_letter_positions(matrix, letter2)

        if row1 == row2:
            decrypted_text.append(matrix[row1][(col1 - 1) % 6])
            decrypted_text.append(matrix[row2][(col2 - 1) % 6])
        elif col1 == col2:
            decrypted_text.append(matrix[(row1 - 1) % 6][col1])
            decrypted_text.append(matrix[(row2 - 1) % 6][col2])
        else:
            decrypted_text.append(matrix[row1][col2])
            decrypted_text.append(matrix[row2][col1])

        i += 2

    return ''.join(decrypted_text)

def main():
    while True:
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")

        if choice == '1':
            key = input("Enter the key: ")
            plain_text = input("Enter the plain text: ")
            encrypted_text = playfair_encrypt(plain_text, key)
            print("Encrypted text:", encrypted_text)
        elif choice == '2':
            key = input("Enter the key: ")
            encrypted_text = input("Enter the encrypted text: ")
            decrypted_text = playfair_decrypt(encrypted_text, key)
            print("Decrypted text:", decrypted_text)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
