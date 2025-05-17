import socket  # ایمپورت کردن ماژول socket برای ارتباطات شبکه

HOST = '127.0.0.1'  # تعریف آدرس IP برای گوش دادن (در اینجا localhost)
PORT = 5000  # تعریف شماره پورت برای گوش دادن

# ایجاد یک شیء socket با استفاده از خانواده آدرس IPv4 و پروتکل TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))  # اتصال (bind) سوکت به آدرس و پورت مشخص شده
    s.listen()  # شروع گوش دادن به اتصالات ورودی
    print(f"Listening on {HOST} : {PORT}")  # چاپ پیامی مبنی بر اینکه سرور در حال گوش دادن است

    conn, addr = s.accept()  # پذیرش یک اتصال از یک کلاینت
    print(f"Connected by {addr}")  # چاپ آدرس کلاینت متصل شده

    # ورود به یک حلقه برای دریافت و ارسال داده
    while True:
        data = conn.recv(1024)  # دریافت حداکثر 1024 بایت داده از کلاینت
        if not data:  # اگر هیچ داده‌ای دریافت نشد، حلقه را بشکن (کلاینت قطع شده است)
            break
        print(f"Received: {data.decode()}")  # رمزگشایی داده‌های دریافتی و چاپ آن

        conn.sendall(f"Hello client!".encode())  # ارسال یک پاسخ به کلاینت (رمزگذاری شده به عنوان بایت)

