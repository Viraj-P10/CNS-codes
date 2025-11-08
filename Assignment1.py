def caesar_encrypt(text, shift):
    result = ""
    for c in text:
        if c.isupper():
            result += chr((ord(c) - ord('A') + shift) % 26 + ord('A'))
        elif c.islower():
            result += chr((ord(c) - ord('a') + shift) % 26 + ord('a'))
        else:
            result += c
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

key_monoalphabetic = "QWERTYUIOPASDFGHJKLZXCVBNM"

def monoalphabetic_encrypt(text):
    text = text.upper()
    result = ""
    for c in text:
        if c.isalpha():
            result += key_monoalphabetic[ord(c) - ord('A')]
        else:
            result += c
    return result

def monoalphabetic_decrypt(text):
    inverse_key = [''] * 26
    for i, char in enumerate(key_monoalphabetic):
        inverse_key[ord(char) - ord('A')] = chr(i + ord('A'))
    result = ""
    for c in text:
        if c.isalpha():
            result += inverse_key[ord(c) - ord('A')]
        else:
            result += c
    return result

def vigenere_encrypt(text, key):
    result = ""
    text = text.upper()
    key = key.upper()
    j = 0
    for c in text:
        if 'A' <= c <= 'Z':
            result += chr((ord(c) + ord(key[j]) - 2 * ord('A')) % 26 + ord('A'))
            j = (j + 1) % len(key)
        else:
            result += c
    return result

def vigenere_decrypt(text, key):
    result = ""
    text = text.upper()
    key = key.upper()
    j = 0
    for c in text:
        if 'A' <= c <= 'Z':
            result += chr((ord(c) - ord(key[j]) + 26) % 26 + ord('A'))
            j = (j + 1) % len(key)
        else:
            result += c
    return result

def rail_fence_encrypt(text, rails):
    rail = ['' for _ in range(rails)]
    dir = 1
    row = 0
    for c in text:
        rail[row] += c
        row += dir
        if row == 0 or row == rails - 1:
            dir *= -1
    return ''.join(rail)

def rail_fence_decrypt(ciphertext, rails):
    # Create an empty matrix to mark places
    matrix = [['\n' for _ in range(len(ciphertext))] for _ in range(rails)]
    dir_down = None
    row, col = 0, 0
    # Mark the places with '*'
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == rails - 1:
            dir_down = False
        matrix[row][col] = '*'
        col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
    # Fill the letters in marked places
    index = 0
    for i in range(rails):
        for j in range(len(ciphertext)):
            if matrix[i][j] == '*' and index < len(ciphertext):
                matrix[i][j] = ciphertext[index]
                index += 1
    # Read the matrix in zig-zag manner to construct message
    result = []
    row, col = 0, 0
    for i in range(len(ciphertext)):
        if row == 0:
            dir_down = True
        if row == rails - 1:
            dir_down = False
        if matrix[row][col] != '\n':
            result.append(matrix[row][col])
            col += 1
        if dir_down:
            row += 1
        else:
            row -= 1
    return ''.join(result)

def vernam_encrypt(text, key):
    text = text.upper()
    key = key.upper()
    if len(key) != len(text):
        return "Error: Key length must be equal to plaintext length"
    result = ""
    for i in range(len(text)):
        xor_val = (ord(text[i]) - ord('A')) ^ (ord(key[i]) - ord('A'))
        result += chr((xor_val % 26) + ord('A'))
    return result

def vernam_decrypt(ciphertext, key):
    # Vernam cipher decryption is same as encryption because XOR is symmetric
    return vernam_encrypt(ciphertext, key)

def main():
    while True:
        print("\nChoose cipher type:")
        print("1. Caesar Cipher")
        print("2. Monoalphabetic Cipher")
        print("3. Vigenère Cipher")
        print("4. Rail Fence Cipher")
        print("5. Vernam Cipher (One-Time Pad)")
        print("6. Exit")
        choice = input("Enter choice (1-6): ")

        if choice == '1':
            plaintext = input("Enter plaintext: ")
            shift = int(input("Enter shift value (integer): "))
            ciphertext = caesar_encrypt(plaintext, shift)
            decrypted = caesar_decrypt(ciphertext, shift)
            print("\nCaesar Cipher")
            print("Plaintext:", plaintext)
            print("Ciphertext:", ciphertext)
            print("Decrypted text:", decrypted)

        elif choice == '2':
            plaintext = input("Enter plaintext: ")
            ciphertext = monoalphabetic_encrypt(plaintext)
            decrypted = monoalphabetic_decrypt(ciphertext)
            print("\nMonoalphabetic Cipher")
            print("Plaintext:", plaintext)
            print("Ciphertext:", ciphertext)
            print("Decrypted text:", decrypted)

        elif choice == '3':
            plaintext = input("Enter plaintext: ")
            key = input("Enter key: ")
            ciphertext = vigenere_encrypt(plaintext, key)
            decrypted = vigenere_decrypt(ciphertext, key)
            print("\nVigenère Cipher")
            print("Plaintext:", plaintext)
            print("Key:", key)
            print("Ciphertext:", ciphertext)
            print("Decrypted text:", decrypted)

        elif choice == '4':
            plaintext = input("Enter plaintext: ")
            rails = int(input("Enter number of rails: "))
            ciphertext = rail_fence_encrypt(plaintext, rails)
            decrypted = rail_fence_decrypt(ciphertext, rails)
            print("\nRail Fence Cipher")
            print("Plaintext:", plaintext)
            print("Ciphertext:", ciphertext)
            print("Decrypted text:", decrypted)

        elif choice == '5':
            plaintext = input("Enter plaintext: ")
            key = input("Enter key (same length as plaintext): ")
            ciphertext = vernam_encrypt(plaintext, key)
            if ciphertext.startswith("Error"):
                print(ciphertext)
            else:
                decrypted = vernam_decrypt(ciphertext, key)
                print("\nVernam Cipher (One-Time Pad)")
                print("Plaintext:", plaintext)
                print("Key:", key)
                print("Ciphertext:", ciphertext)
                print("Decrypted text:", decrypted)

        elif choice == '6':
            print("Exiting program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
