import socket  # ایمپورت کردن ماژول socket برای ارتباطات شبکه

HOST = '127.0.0.1'  # تعریف آدرس IP سروری که می خواهیم به آن متصل شویم (در اینجا localhost)
PORT = 5000  # تعریف شماره پورت سروری که می خواهیم به آن متصل شویم

# ایجاد یک شیء socket با استفاده از خانواده آدرس IPv4 و پروتکل TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))  # اتصال به سرور در آدرس و پورت مشخص شده

    message = "hello server!"  # تعریف پیامی که می خواهیم به سرور ارسال کنیم
    s.sendall(message.encode('utf-8'))  # کدگذاری پیام به بایت با استفاده از UTF-8 و ارسال آن به سرور

    data = s.recv(1024)  # دریافت حداکثر 1024 بایت داده از سرور
    print(f"received: {data.decode('utf-8')}")  # رمزگشایی داده های دریافتی از UTF-8 و چاپ آن

    print("The connection was closed.")  # چاپ پیامی مبنی بر اینکه اتصال بسته شده است
