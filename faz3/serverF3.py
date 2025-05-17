import socket  # ایمپورت ماژول socket برای عملیات شبکه
import threading  # ایمپورت ماژول threading برای ایجاد و مدیریت thread ها

HOST = '127.0.0.1'  # آدرس IP که سرور روی آن گوش می‌دهد (localhost در اینجا)
PORT = 5000  # شماره پورتی که سرور روی آن گوش می‌دهد

clients = []  # لیستی برای نگهداری socket های متصل به سرور

# ایجاد یک socket برای سرور با استفاده از IPv4 و پروتکل TCP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# متصل کردن (bind) سرور به آدرس و پورت مشخص شده
server_socket.bind((HOST, PORT))
# سرور شروع به گوش دادن برای اتصالات ورودی می‌کند
server_socket.listen()
print(f"Server listening on {HOST} : {PORT}")  # چاپ پیامی مبنی بر اینکه سرور در حال گوش دادن است

# تابع برای مدیریت هر کلاینت به صورت جداگانه
def handle_client(client_socket):
    while True:  # یک حلقه بی نهایت برای دریافت پیام از کلاینت
        try:
            message = client_socket.recv(1024).decode()  # دریافت پیام (حداکثر 1024 بایت) و رمزگشایی آن
            for client in clients:  # ارسال پیام به تمامی کلاینت های دیگر
                if client != client_socket:  # به جز خود فرستنده
                    client.sendall(message.encode())  # ارسال پیام به کلاینت دیگر
        except:
            # اگر خطایی رخ داد (مثلاً اتصال کلاینت قطع شد)
            clients.remove(client_socket)  # حذف socket کلاینت از لیست
            client_socket.close()  # بستن اتصال کلاینت
            break  # خروج از حلقه

# حلقه اصلی سرور برای پذیرش اتصالات جدید
while True:
    client_socket, addr = server_socket.accept()  # پذیرش یک اتصال جدید
    clients.append(client_socket)  # افزودن socket کلاینت به لیست کلاینت ها
    # ایجاد یک thread جدید برای مدیریت کلاینت و اجرای تابع handle_client در آن
    threading.Thread(target=handle_client, args=(client_socket,)).start()

