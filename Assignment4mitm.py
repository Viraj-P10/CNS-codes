import socket

p = 23  # Use shared constants
g = 5

print("MITM (Mallory) - Diffie-Hellman MITM Demo")
private_key = int(input("Enter MITM's private key: "))
mitm_public_key = pow(g, private_key, p)
print(f"MITM's Public Key: {mitm_public_key}")

HOST = '127.0.0.1'
SENDER_PORT = 5000
RECEIVER_PORT = 5001

# Connect to Sender
sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sender_socket.bind((HOST, SENDER_PORT))
sender_socket.listen(1)
print("Waiting for Sender to connect...")
s_conn, _ = sender_socket.accept()
print("Sender connected.")

# Connect to Receiver
receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receiver_socket.bind((HOST, RECEIVER_PORT))
receiver_socket.listen(1)
print("Waiting for Receiver to connect...")
r_conn, _ = receiver_socket.accept()
print("Receiver connected.")

# Step 1: Intercept Sender's Public Key, send MITM's
sender_pub = int(s_conn.recv(1024).decode())
print(f"Intercepted Sender's Public Key: {sender_pub}")
r_conn.sendall(str(mitm_public_key).encode())

# Step 2: Intercept Receiver's Public Key, send MITM's
receiver_pub = int(r_conn.recv(1024).decode())
print(f"Intercepted Receiver's Public Key: {receiver_pub}")
s_conn.sendall(str(mitm_public_key).encode())

# Step 3: Compute shared secrets
shared_with_sender = pow(sender_pub, private_key, p)
shared_with_receiver = pow(receiver_pub, private_key, p)
print(f"Shared secret with Sender: {shared_with_sender}")
print(f"Shared secret with Receiver: {shared_with_receiver}")

# Step 4: Intercept message, decrypt, (optional modify), re-encrypt
enc_msg = s_conn.recv(1024).decode()
print(f"Intercepted encrypted message from Sender: {enc_msg}")

# Simple Caesar Cipher for demonstration
plain = ''
for ch in enc_msg:
    if ch.isupper():
        plain += chr(((ord(ch) - 65 - shared_with_sender) % 26) + 65)
    else:
        plain += ch
print(f"Decrypted message (using Sender's secret): {plain}")

# Optionally modify
mod = input("Modify message before sending to Receiver (leave blank for no modification): ").strip()
if mod:
    plain = mod
    print(f"Modified message: {plain}")

# Re-encrypt with Receiver's shared secret
enc2 = ''
for ch in plain:
    if ch.isupper():
        enc2 += chr(((ord(ch) - 65 + shared_with_receiver) % 26) + 65)
    else:
        enc2 += ch
print(f"Forwarding encrypted message to Receiver: {enc2}")
r_conn.sendall(enc2.encode())

# Cleanup
s_conn.close()
r_conn.close()
sender_socket.close()
receiver_socket.close()
