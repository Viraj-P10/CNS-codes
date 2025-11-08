import random
import hashlib

def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def generate_keypair():
    p = q = 1
    while not is_prime(p):
        p = random.randint(100, 1000)
    while not is_prime(q) or p == q:
        q = random.randint(100, 1000)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randint(2, phi - 1)
    while gcd(e, phi) != 1:
        e = random.randint(2, phi - 1)
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def rsa_encrypt(message, key):
    e, n = key
    return [pow(ord(char), e, n) for char in message]

# --- UPDATED: Sign the full message hash as integer ---
def generate_signature(message, private_key):
    hashed = int(hashlib.sha256(message.encode()).hexdigest(), 16)
    d, n = private_key
    signature = pow(hashed % n, d, n)  # Sign just the integer hash
    return signature

# --- UPDATED: Main function ---
def main():
    print("Generating RSA Key Pair...")
    public_key, private_key = generate_keypair()
    print(f"Public Key (e, n): {public_key}")
    print(f"Private Key (d, n): {private_key}")
    message = input("\nEnter the message to be sent: ")
    encrypted_message = rsa_encrypt(message, public_key)
    signature = generate_signature(message, private_key)
    print("\nEncrypted Message:", encrypted_message)
    print("Digital Signature:", signature)  # Now a single integer
    print("\nCopy these and provide to the receiver:")
    print("Public Key:", public_key)
    print("Encrypted Message:", encrypted_message)
    print("Signature:", signature)
    print("Private Key (Keep secret):", private_key)

if __name__ == "__main__":
    main()