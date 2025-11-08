import socket

p = 23
g = 5
print("Receiver (Bob) - Diffie-Hellman MITM Demo")
private_key = int(input("Enter Receiver's private key: "))
receiver_public_key = pow(g, private_key, p)
print(f"Receiver's Public Key: {receiver_public_key}")

HOST = '127.0.0.1'
MITM_PORT = 5001  # Connect to MITM

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, MITM_PORT))
sock.sendall(str(receiver_public_key).encode())
received_pub = int(sock.recv(1024).decode())
print(f"Received public key from MITM (spoofed sender): {received_pub}")
shared_secret = pow(received_pub, private_key, p)
print(f"Receiver's shared secret: {shared_secret}")

# Receive (and decrypt) message
enc = sock.recv(1024).decode()
print(f"Encrypted message received: {enc}")
plain = ''
for ch in enc:
    if ch.isupper():
        plain += chr(((ord(ch) - 65 - shared_secret) % 26) + 65)
    else:
        plain += ch
print(f"Decrypted message: {plain}")
sock.close()
