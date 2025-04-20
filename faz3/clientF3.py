import socket
import threading

HOST = '127.0.0.1'  
PORT = 5000        

def receive_messages(sock):
    while True:
        message = sock.recv(1024).decode()
        if not message: break
        print(f"recieved: {message}")

s = socket.socket()
s.connect((HOST, PORT))
print("Connected to the server.")

threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

while True:
    message = input()
    if message.lower() == "/exit":
        s.sendall(message.encode())
        break
    s.sendall(message.encode())

s.close()
print("Disconnected from the server.")
