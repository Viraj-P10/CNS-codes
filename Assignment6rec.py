import hashlib

def rsa_decrypt(cipher, key):
    d, n = key
    return ''.join([chr(pow(char, d, n)) for char in cipher])

# --- UPDATED: Verify single integer signature ---
def verify_signature(message, signature, public_key):
    hashed = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    e, n = public_key
    decrypted_hash = pow(signature, e, n)
    return decrypted_hash == (hashed % n)

# --- UPDATED: Main function ---
def main():
    print("Enter Public Key (e,n) as comma separated (e.g. 65537,99991):")
    public_key_str = input().strip()
    e, n = map(int, public_key_str.strip('()').split(','))
    print("Enter Encrypted Message as list of integers (e.g. [12345, 67890]):")
    encrypted_message_str = input().strip()
    encrypted_message = list(map(int, encrypted_message_str.strip('[]').split(',')))
    print("Enter Digital Signature as integer (e.g. 11111):")
    signature_str = input().strip()
    signature = int(signature_str)
    print("Enter Private Key (d,n) as comma separated (e.g. 123456,99991):")
    private_key_str = input().strip()
    d, n2 = map(int, private_key_str.strip('()').split(','))
    if n2 != n:
        print("Warning: n values in public and private key differ!")
    decrypted_message = rsa_decrypt(encrypted_message, (d, n))
    print("\nDecrypted Message:", decrypted_message)
    is_valid = verify_signature(decrypted_message, signature, (e, n))
    if is_valid:
        print("Signature is valid. Message integrity verified.")
    else:
        print("Invalid Signature. Message may have been tampered with.")

if __name__ == "__main__":
    main()
