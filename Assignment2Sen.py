import socket

# Connect to receiver
s = socket.socket()
s.connect(('localhost', 12345))

# Receive public key
data = s.recv(1024).decode()
e, n = map(int, data.split(','))
print(f"Received public key: e={e}, n={n}")

# Input plaintext (can be any integer)
plaintext = int(input("Enter plaintext (integer): "))
quotient = plaintext // n
remainder = plaintext % n
print(f"Plaintext quotient: {quotient}, remainder: {remainder}")

# Encrypt the remainder
cipher = pow(remainder, e, n)
print(f"Encrypted remainder (ciphertext): {cipher}")

# Send both ciphertext and quotient to receiver, as comma-separated values
s.send(f"{cipher},{quotient}".encode())
s.close()
