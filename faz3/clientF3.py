import socket  # ایمپورت ماژول socket برای ایجاد ارتباطات شبکه
import threading  # ایمپورت ماژول threading برای مدیریت thread ها

HOST = '127.0.0.1'  # آدرس IP سرور (localhost)
PORT = 5000        # پورت سرور

def receive_messages(sock):
    """
    تابعی برای دریافت پیام ها از سرور.
    :param sock: سوکت ارتباطی با سرور.
    """
    while True:
        message = sock.recv(1024).decode()  # دریافت پیام از سرور (حداکثر 1024 بایت) و رمزگشایی
        if not message:  # اگر پیامی دریافت نشد (اتصال بسته شده)
            break  # از حلقه خارج شو
        print(f"recieved: {message}")  # چاپ پیام دریافتی

s = socket.socket()  # ایجاد یک سوکت TCP/IP
s.connect((HOST, PORT))  # اتصال به سرور
print("Connected to the server.")  # چاپ پیام موفقیت آمیز بودن اتصال

threading.Thread(target=receive_messages, args=(s,), daemon=True).start()  # ایجاد و شروع thread برای دریافت پیام ها

while True:
    message = input()  # دریافت ورودی از کاربر
    if message.lower() == "/exit":  # اگر ورودی کاربر "/exit" بود
        s.sendall(message.encode())  # ارسال دستور خروج به سرور
        break  # از حلقه خارج شو
    s.sendall(message.encode())  # ارسال پیام به سرور

s.close()  # بستن سوکت
print("Disconnected from the server.")  # چاپ پیام قطع اتصال

