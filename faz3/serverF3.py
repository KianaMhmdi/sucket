import socket
import threading

HOST = '127.0.0.1'
PORT = 5000
clients = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server listening on {HOST} : {PORT}")

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            for client in clients:
                if client != client_socket:
                    client.sendall(message.encode())
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

while True:
    client_socket, addr = server_socket.accept()
    clients.append(client_socket)
    threading.Thread(target=handle_client, args=(client_socket,)).start()
