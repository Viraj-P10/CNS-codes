import socket

p = 23
g = 5
print("Sender (Alice) - Diffie-Hellman MITM Demo")
private_key = int(input("Enter Sender's private key: "))
sender_public_key = pow(g, private_key, p)
print(f"Sender's Public Key: {sender_public_key}")

HOST = '127.0.0.1'
MITM_PORT = 5000  # Connect to MITM

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, MITM_PORT))
sock.sendall(str(sender_public_key).encode())
received_pub = int(sock.recv(1024).decode())
print(f"Received public key from MITM (spoofed receiver): {received_pub}")
shared_secret = pow(received_pub, private_key, p)
print(f"Sender's shared secret: {shared_secret}")

# Send message encrypted with shared secret
plain = input("Enter message (): ").strip().upper()
enc = ''
for ch in plain:
    if ch.isupper():
        enc += chr(((ord(ch) - 65 + shared_secret) % 26) + 65)
    else:
        enc += ch
print(f"Encrypted message sent: {enc}")
sock.sendall(enc.encode())
sock.close()
