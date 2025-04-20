import socket
import threading

HOST = '127.0.0.1'
PORT = 5000

def client_handler(conn, addr):
    print(f"Connect: {addr}")
    while True:
        data = conn.recv(1024)
        if not data: break
        print(f"Receive: {data.decode()}")
        conn.sendall(f"Hello client!".encode())
    print(f"Close: {addr}")
    conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Listen: {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=client_handler, args=(conn, addr)).start()
        print(f"New con. Active: {threading.active_count() - 1}")


