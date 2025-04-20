import socket
import threading
import datetime

HOST = '127.0.0.1'
PORT = 5000

class ChatServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.client_ips = {}

    def start(self):
        try:
            self.sock.bind((self.host, self.port))
            self.sock.listen()
            print(f"Server listening on {self.host}:{self.port}")

            while True:
                conn, addr = self.sock.accept()
                username = self.receive_username(conn)
                if username:
                    self.clients[username] = conn
                    self.client_ips[username] = addr[0]
                    self.broadcast(f"{username} has joined the chat.", username)
                    self.send_user_list()
                    threading.Thread(target=self.handle_client, args=(conn, username)).start()
                else:
                    print(f"Failed to receive username from {addr}")
                    conn.close()

        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.sock.close()

    def receive_username(self, conn):
        try:
            username = conn.recv(1024).decode()
            return username
        except:
            return None

    def broadcast(self, message, sender=None):
        for username, conn in self.clients.items():
            if username != sender:
                try:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    formatted_message = f"[{sender} - {timestamp}]: {message}"
                    conn.sendall(formatted_message.encode())
                except:
                    print(f"Error broadcasting to {username}")
                    self.remove_client(username)

    def send_user_list(self):
        user_list = ' '.join([f"{user}:{self.client_ips[user]}" for user in self.clients])
        for username, conn in self.clients.items():
            try:
                conn.sendall(f'@user_list {user_list}'.encode())
            except:
                print(f"Error sending user list to {username}")
                self.remove_client(username)

    def handle_client(self, conn, username):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                message = data.decode()
                if message.startswith('@pm'):
                    parts = message.split(' ', 2)
                    if len(parts) == 3:
                        target_user = parts[1]
                        private_message = parts[2]
                        self.send_private_message(username, target_user, private_message)
                elif message == '@list_users':
                    self.send_user_list_to_client(conn)
                else:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    formatted_message = f"[{username} - {timestamp}]: {message}"
                    self.broadcast(formatted_message, username)
        except Exception as e:
            print(f"Error handling client {username}: {e}")
        finally:
            self.remove_client(username)

    def send_private_message(self, sender, target, message):
        if target in self.clients:
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_message = f"(Private from {sender} - {timestamp}): {message}"
                self.clients[target].sendall(formatted_message.encode())
            except:
                print(f"Error sending private message to {target}")
                self.remove_client(target)
        else:
            print(f"User {target} not found")

    def send_user_list_to_client(self, conn):
        user_list = ' '.join([f"{user}:{self.client_ips[user]}" for user in self.clients])
        try:
            conn.sendall(f'@user_list {user_list}'.encode())
        except:
            print(f"Error sending user list")

    def remove_client(self, username):
        if username in self.clients:
            del self.clients[username]
            del self.client_ips[username]
            self.broadcast(f"{username} has left the chat.")
            self.send_user_list()

if __name__ == "__main__":
    server = ChatServer(HOST, PORT)
    server_thread = threading.Thread(target=server.start)
    server_thread.start()
