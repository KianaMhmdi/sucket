import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
import datetime

HOST = '127.0.0.1'
PORT = 5000

class ChatClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None
        self.running = True

        # UI elements
        self.root = tk.Tk()
        self.root.title("Chat App")

        self.text_area = scrolledtext.ScrolledText(self.root, state='disabled', height=20, width=50)
        self.text_area.pack(padx=10, pady=10)

        self.input_area = tk.Text(self.root, height=3, width=50)
        self.input_area.pack(padx=10, pady=5)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.label = tk.Label(self.root, text="Enter username:")
        self.label.pack(padx=10, pady=5)
        self.username_input = tk.Entry(self.root, width=30)
        self.username_input.pack(padx=10, pady=5)
        self.login_button = tk.Button(self.root, text="Login", command=self.login)
        self.login_button.pack(pady=5)

        self.users = {}

    def login(self):
        self.username = self.username_input.get()
        if self.username:
            self.label.destroy()
            self.username_input.destroy()
            self.login_button.destroy()
            self.connect_to_server()

    def connect_to_server(self):
        try:
            self.sock.connect((self.host, self.port))
            self.sock.sendall(self.username.encode())  # Send username after connecting
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
        except Exception as e:
            self.display_message(f"Could not connect to server: {e}")

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, message + '\n')
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    def send_message(self):
        message = self.input_area.get("1.0", tk.END).strip()
        if message:
            if message.startswith('@list_users'):
                self.sock.sendall(message.encode())
            elif message.startswith('@pm'):
                parts = message.split(' ', 2)
                if len(parts) == 3:
                    target_user = parts[1]
                    private_message = parts[2]
                    self.sock.sendall(f'@pm {target_user} {private_message}'.encode())
            else:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                formatted_message = f"[{self.username} - {timestamp}]: {message}"
                self.sock.sendall(formatted_message.encode())
            self.input_area.delete("1.0", tk.END)

    def receive_messages(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    self.stop()
                    break

                message = data.decode()
                if message.startswith('@user_list'):
                    user_list = message.split(' ')[1:]
                    self.users = {user.split(':')[0]: user.split(':')[1] for user in user_list}
                    self.display_message(f"Current users: {', '.join(self.users.keys())}")
                else:
                    self.display_message(message)
            except Exception as e:
                self.display_message(f"Error receiving message: {e}")
                self.stop()
                break

    def stop(self):
        if self.running:
            self.running = False
            self.sock.close()
            self.display_message("Disconnected from server.")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    client = ChatClient(HOST, PORT)
    client.run()
