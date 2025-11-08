import socket
import math

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def modinv(a, m):
    # Extended Euclidean Algorithm for modular inverse
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = extended_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

# Key Generation
p = int(input("Enter prime number p: "))
q = int(input("Enter prime number q: "))
if not (is_prime(p) and is_prime(q)):
    raise ValueError("Both numbers must be prime.")
n = p * q
phi = (p-1)*(q-1)
e = 3
while math.gcd(e, phi) != 1:
    e += 2
d = modinv(e, phi)
print(f"Public Key: (e={e}, n={n})")
print(f"Private Key: (d={d}, n={n})")

# Networking (acts as server)
s = socket.socket()
s.bind(('localhost', 12345))
s.listen(1)
print("Receiver is listening...")
conn, addr = s.accept()
print(f"Connected by {addr}")

# Send public key to sender as e,n
conn.send(f"{e},{n}".encode())

# Receive ciphertext and quotient
cipher_data = conn.recv(1024).decode()
cipher, quotient = map(int, cipher_data.split(','))
print(f"Received ciphertext: {cipher} and quotient: {quotient}")

# Decrypt only the remainder part
decrypted_remainder = pow(cipher, d, n)
# Reconstruct original plaintext
plaintext = quotient * n + decrypted_remainder
print(f"Recovered plaintext: {plaintext}")
conn.close()
