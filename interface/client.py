import socket  # ایمپورت ماژول socket برای عملیات شبکه
import threading  # ایمپورت ماژول threading برای ایجاد و مدیریت thread ها
import tkinter as tk  # ایمپورت ماژول tkinter برای رابط کاربری گرافیکی
from tkinter import scrolledtext  # ایمپورت ماژول scrolledtext برای ایجاد کادر متن با قابلیت پیمایش
import datetime  # ایمپورت ماژول datetime برای کار با تاریخ و زمان

HOST = '127.0.0.1'  # آدرس IP سرور
PORT = 5000  # پورت سرور

class ChatClient:
    def __init__(self, host, port):
        """
        سازنده کلاس ChatClient.
        :param host: آدرس IP سرور.
        :param port: پورت سرور.
        """
        self.host = host  # ذخیره آدرس هاست
        self.port = port  # ذخیره شماره پورت
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ایجاد socket
        self.username = None  # نام کاربری کلاینت
        self.running = True  # نشان دهنده وضعیت اجرای کلاینت

        # ایجاد عناصر رابط کاربری
        self.root = tk.Tk()  # ایجاد پنجره اصلی
        self.root.title("Chat App")  # تنظیم عنوان پنجره

        self.text_area = scrolledtext.ScrolledText(self.root, state='disabled', height=20, width=50)  # ایجاد کادر متن برای نمایش پیام ها
        self.text_area.pack(padx=10, pady=10)  # اضافه کردن کادر متن به پنجره

        self.input_area = tk.Text(self.root, height=3, width=50)  # ایجاد کادر متن برای ورود پیام
        self.input_area.pack(padx=10, pady=5)  # اضافه کردن کادر متن به پنجره

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)  # ایجاد دکمه ارسال پیام
        self.send_button.pack(pady=5)  # اضافه کردن دکمه به پنجره

        self.label = tk.Label(self.root, text="Enter username:")  # ایجاد برچسب برای ورود نام کاربری
        self.label.pack(padx=10, pady=5)  # اضافه کردن برچسب به پنجره
        self.username_input = tk.Entry(self.root, width=30)  # ایجاد کادر ورود نام کاربری
        self.username_input.pack(padx=10, pady=5)  # اضافه کردن کادر ورود به پنجره
        self.login_button = tk.Button(self.root, text="Login", command=self.login)  # ایجاد دکمه ورود
        self.login_button.pack(pady=5)  # اضافه کردن دکمه به پنجره

        self.users = {}  # دیکشنری برای نگهداری لیست کاربران آنلاین

    def login(self):
        """
        ورود به حساب کاربری.
        """
        self.username = self.username_input.get()  # دریافت نام کاربری از کادر ورود
        if self.username:  # اگر نام کاربری وارد شده باشد
            self.label.destroy()  # حذف برچسب
            self.username_input.destroy()  # حذف کادر ورود
            self.login_button.destroy()  # حذف دکمه ورود
            self.connect_to_server()  # اتصال به سرور

    def connect_to_server(self):
        """
        اتصال به سرور.
        """
        try:
            self.sock.connect((self.host, self.port))  # اتصال به سرور
            self.sock.sendall(self.username.encode())  # ارسال نام کاربری به سرور
            self.receive_thread = threading.Thread(target=self.receive_messages)  # ایجاد thread برای دریافت پیام ها
            self.receive_thread.start()  # شروع thread دریافت پیام ها
        except Exception as e:  # مدیریت خطاها
            self.display_message(f"Could not connect to server: {e}")  # نمایش پیام خطا

    def display_message(self, message):
        """
        نمایش پیام در کادر متن.
        :param message: پیام برای نمایش.
        """
        self.text_area.config(state='normal')  # فعال کردن کادر متن
        self.text_area.insert(tk.END, message + '\n')  # اضافه کردن پیام به کادر متن
        self.text_area.config(state='disabled')  # غیرفعال کردن کادر متن
        self.text_area.see(tk.END)  # پیمایش به انتهای کادر متن

    def send_message(self):
        """
        ارسال پیام به سرور.
        """
        message = self.input_area.get("1.0", tk.END).strip()  # دریافت پیام از کادر ورود
        if message:  # اگر پیامی وجود داشته باشد
            if message.startswith('@list_users'):  # اگر دستور درخواست لیست کاربران بود
                self.sock.sendall(message.encode())  # ارسال دستور به سرور
            elif message.startswith('@pm'):  # اگر پیام خصوصی بود
                parts = message.split(' ', 2)  # جدا کردن بخش های پیام
                if len(parts) == 3:  # اگر پیام ساختار درستی داشت
                    target_user = parts[1]  # دریافت نام کاربری گیرنده
                    private_message = parts[2]  # دریافت پیام خصوصی
                    self.sock.sendall(f'@pm {target_user} {private_message}'.encode())  # ارسال پیام خصوصی به سرور
            else:  # اگر پیام معمولی بود
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # ایجاد timestamp
                formatted_message = f"[{self.username} - {timestamp}]: {message}"  # ایجاد پیام با فرمت مناسب
                self.sock.sendall(formatted_message.encode())  # ارسال پیام به سرور
            self.input_area.delete("1.0", tk.END)  # پاک کردن کادر ورود

    def receive_messages(self):
        """
        دریافت پیام ها از سرور.
        """
        while self.running:  # تا زمانی که کلاینت در حال اجرا است
            try:
                data = self.sock.recv(1024)  # دریافت پیام
                if not data:  # اگر پیامی دریافت نشد، اتصال قطع شده است
                    self.stop()  # توقف کلاینت
                    break

                message = data.decode()  # رمزگشایی پیام
                if message.startswith('@user_list'):  # اگر پیام حاوی لیست کاربران است
                    user_list = message.split(' ')[1:]  # جدا کردن لیست کاربران از پیام
                    self.users = {user.split(':')[0]: user.split(':')[1] for user in user_list}  # ایجاد دیکشنری از لیست کاربران
                    self.display_message(f"Current users: {', '.join(self.users.keys())}")  # نمایش لیست کاربران
                else:  # اگر پیام معمولی بود
                    self.display_message(message)  # نمایش پیام
            except Exception as e:  # مدیریت خطاها
                self.display_message(f"Error receiving message: {e}")  # نمایش پیام خطا
                self.stop()  # توقف کلاینت
                break

    def stop(self):
        """
        توقف کلاینت.
        """
        if self.running:  # اگر کلاینت در حال اجرا است
            self.running = False  # تنظیم وضعیت به غیر فعال
            self.sock.close()  # بستن socket
            self.display_message("Disconnected from server.")  # نمایش پیام قطع اتصال

    def run(self):
        """
        اجرای کلاینت.
        """
        self.root.mainloop()  # شروع حلقه اصلی tkinter

if __name__ == "__main__":
    client = ChatClient(HOST, PORT)  # ایجاد شیء از کلاس ChatClient
    client.run()  # اجرای کلاینت
