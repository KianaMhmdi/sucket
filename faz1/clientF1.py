import socket

HOST = '127.0.0.1'  
PORT = 5000       

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    message = "hello server!"
    s.sendall(message.encode('utf-8'))
    data = s.recv(1024)
    print(f"received: {data.decode('utf-8')}")
    print("The connection was closed.")
