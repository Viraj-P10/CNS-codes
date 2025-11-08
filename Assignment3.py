def custom_encrypt(plain_text, key):
    cipher = ""
    for ch in plain_text:
        shifted = (ord(ch) + key) % 256
        encrypted = shifted ^ key
        cipher += format(encrypted, '02x') 
    return cipher

def custom_decrypt(cipher_text, key):
    plain = ""
    for i in range(0, len(cipher_text), 2):
        encrypted = int(cipher_text[i:i+2], 16)
        shifted = encrypted ^ key
        orig_ord = (shifted - key) % 256
        plain += chr(orig_ord)
    return plain

plain_text = input("Enter text to encrypt: ")
key = int(input("Enter numeric key (1-255): "))
cipher = custom_encrypt(plain_text, key)
print("Encrypted text:", cipher)
decrypted = custom_decrypt(cipher, key)
print("Decrypted text:", decrypted)
