import socket  # ایمپورت کردن ماژول socket برای ارتباطات شبکه
import threading  # ایمپورت کردن ماژول threading برای مدیریت thread ها

HOST = '127.0.0.1'  # تعریف آدرس IP برای گوش دادن (در اینجا localhost)
PORT = 5000  # تعریف شماره پورت برای گوش دادن

# تعریف تابع برای مدیریت هر کلاینت به صورت جداگانه در یک thread
def client_handler(conn, addr):
    print(f"Connect: {addr}")  # چاپ آدرس کلاینتی که متصل شده است
    while True:
        data = conn.recv(1024)  # دریافت حداکثر 1024 بایت داده از کلاینت
        if not data: break  # اگر هیچ داده‌ای دریافت نشد، حلقه را بشکن (کلاینت قطع شده است)
        print(f"Receive: {data.decode()}")  # چاپ داده‌های دریافتی از کلاینت
        conn.sendall(f"Hello client!".encode())  # ارسال پاسخ به کلاینت
    print(f"Close: {addr}")  # چاپ آدرس کلاینتی که اتصالش قطع شده است
    conn.close()  # بستن اتصال با کلاینت

# ایجاد یک شیء socket با استفاده از خانواده آدرس IPv4 و پروتکل TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # اتصال (bind) سوکت به آدرس و پورت مشخص شده
    s.listen()  # شروع گوش دادن به اتصالات ورودی
    print(f"Listen: {HOST}:{PORT}")  # چاپ پیامی مبنی بر اینکه سرور در حال گوش دادن است
    while True:
        conn, addr = s.accept()  # پذیرش یک اتصال از یک کلاینت
        # ایجاد یک thread جدید برای مدیریت کلاینت و اجرای تابع client_handler در آن
        threading.Thread(target=client_handler, args=(conn, addr)).start()
        # چاپ تعداد thread های فعال (منهای thread اصلی که سرور را اجرا می کند)
        print(f"New con. Active: {threading.active_count() - 1}")



