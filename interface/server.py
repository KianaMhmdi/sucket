import socket  # ایمپورت ماژول socket برای عملیات شبکه
import threading  # ایمپورت ماژول threading برای ایجاد و مدیریت thread ها
import datetime  # ایمپورت ماژول datetime برای کار با تاریخ و زمان

HOST = '127.0.0.1'  # آدرس IP که سرور روی آن گوش می‌دهد (localhost در اینجا)
PORT = 5000  # شماره پورتی که سرور روی آن گوش می‌دهد

class ChatServer:
    def __init__(self, host, port):
        """
        سازنده کلاس ChatServer.
        :param host: آدرس IP که سرور روی آن گوش می‌دهد.
        :param port: شماره پورتی که سرور روی آن گوش می‌دهد.
        """
        self.host = host  # ذخیره آدرس هاست
        self.port = port  # ذخیره شماره پورت
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # ایجاد socket برای سرور
        self.clients = {}  # دیکشنری برای نگهداری اطلاعات کلاینت ها (username: socket)
        self.client_ips = {} # دیکشنری برای نگهداری IP کلاینت ها (username: ip address)

    def start(self):
        """
        شروع به کار سرور.
        """
        try:
            self.sock.bind((self.host, self.port))  # متصل کردن (bind) سوکت به آدرس و پورت
            self.sock.listen()  # شروع گوش دادن به اتصالات ورودی
            print(f"Server listening on {self.host}:{self.port}")  # چاپ پیام

            while True:  # حلقه بی نهایت برای پذیرش اتصالات جدید
                conn, addr = self.sock.accept()  # پذیرش یک اتصال جدید
                username = self.receive_username(conn)  # دریافت نام کاربری از کلاینت

                if username:  # اگر نام کاربری با موفقیت دریافت شد
                    self.clients[username] = conn  # ذخیره socket کلاینت در دیکشنری
                    self.client_ips[username] = addr[0] # ذخیره IP کلاینت در دیکشنری
                    self.broadcast(f"{username} has joined the chat.", username)  # ارسال پیام ورود به همه
                    self.send_user_list()  # ارسال لیست کاربران آنلاین به همه
                    threading.Thread(target=self.handle_client, args=(conn, username)).start()  # شروع thread برای مدیریت کلاینت
                else:  # اگر دریافت نام کاربری ناموفق بود
                    print(f"Failed to receive username from {addr}")  # چاپ پیام خطا
                    conn.close()  # بستن اتصال

        except Exception as e:  # مدیریت خطاها
            print(f"Server error: {e}")  # چاپ خطا
        finally:
            self.sock.close()  # بستن socket در صورت بروز خطا

    def receive_username(self, conn):
        """
        دریافت نام کاربری از کلاینت.
        :param conn: socket کلاینت.
        :return: نام کاربری اگر با موفقیت دریافت شود، در غیر این صورت None.
        """
        try:
            username = conn.recv(1024).decode()  # دریافت و رمزگشایی نام کاربری
            return username  # بازگرداندن نام کاربری
        except:
            return None  # بازگرداندن None در صورت خطا

    def broadcast(self, message, sender=None):
        """
        ارسال پیام به همه کلاینت ها (به جز فرستنده).
        :param message: پیام ارسالی.
        :param sender: نام کاربری فرستنده (اختیاری).
        """
        for username, conn in self.clients.items():  # پیمایش در لیست کلاینت ها
            if username != sender:  # اگر کلاینت، فرستنده پیام نباشد
                try:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # ایجاد timestamp
                    formatted_message = f"[{sender} - {timestamp}]: {message}" # ساخت پیام با فرمت مناسب
                    conn.sendall(formatted_message.encode())  # ارسال پیام به کلاینت
                except:
                    print(f"Error broadcasting to {username}")  # چاپ خطا
                    self.remove_client(username)  # حذف کلاینت

    def send_user_list(self):
        """
        ارسال لیست کاربران آنلاین به همه کلاینت ها.
        """
        user_list = ' '.join([f"{user}:{self.client_ips[user]}" for user in self.clients]) # ساخت لیست کاربران با فرمت مناسب
        for username, conn in self.clients.items(): # پیمایش در لیست کلاینت ها
            try:
                conn.sendall(f'@user_list {user_list}'.encode())  # ارسال لیست کاربران به کلاینت
            except:
                print(f"Error sending user list to {username}")  # چاپ خطا
                self.remove_client(username)  # حذف کلاینت

    def handle_client(self, conn, username):
        """
        مدیریت هر کلاینت در یک thread جداگانه.
        :param conn: socket کلاینت.
        :param username: نام کاربری کلاینت.
        """
        try:
            while True:  # حلقه بی نهایت برای دریافت پیام از کلاینت
                data = conn.recv(1024)  # دریافت پیام
                if not data:  # اگر پیامی دریافت نشد، اتصال قطع شده است
                    break

                message = data.decode()  # رمزگشایی پیام
                if message.startswith('@pm'):  # اگر پیام، پیام خصوصی است
                    parts = message.split(' ', 2)  # جدا کردن بخش های پیام
                    if len(parts) == 3: # اگر پیام ساختار درستی داشت
                        target_user = parts[1]  # دریافت نام کاربری گیرنده
                        private_message = parts[2]  # دریافت پیام خصوصی
                        self.send_private_message(username, target_user, private_message)  # ارسال پیام خصوصی
                elif message == '@list_users':  # اگر دستور درخواست لیست کاربران بود
                    self.send_user_list_to_client(conn)  # ارسال لیست کاربران به کلاینت درخواست کننده
                else:  # اگر پیام معمولی بود
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # ایجاد timestamp
                    formatted_message = f"[{username} - {timestamp}]: {message}"  # ساخت پیام با فرمت مناسب
                    self.broadcast(formatted_message, username)  # ارسال پیام به همه
        except Exception as e:  # مدیریت خطاها
            print(f"Error handling client {username}: {e}")  # چاپ خطا
        finally:
            self.remove_client(username)  # حذف کلاینت در صورت بروز خطا یا قطع اتصال

    def send_private_message(self, sender, target, message):
        """
        ارسال پیام خصوصی به یک کلاینت خاص.
        :param sender: نام کاربری فرستنده.
        :param target: نام کاربری گیرنده.
        :param message: پیام خصوصی.
        """
        if target in self.clients:  # اگر گیرنده در لیست کلاینت ها وجود داشت
            try:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") # ایجاد timestamp
                formatted_message = f"(Private from {sender} - {timestamp}): {message}"  # ساخت پیام با فرمت مناسب
                self.clients[target].sendall(formatted_message.encode())  # ارسال پیام به گیرنده
            except:
                print(f"Error sending private message to {target}")  # چاپ خطا
                self.remove_client(target)  # حذف گیرنده
        else:
            print(f"User {target} not found")  # چاپ پیام خطا در صورت عدم وجود گیرنده

    def send_user_list_to_client(self, conn):
        """
        ارسال لیست کاربران آنلاین به یک کلاینت خاص.
        :param conn: socket کلاینت.
        """
        user_list = ' '.join([f"{user}:{self.client_ips[user]}" for user in self.clients]) # ساخت لیست کاربران با فرمت مناسب
        try:
            conn.sendall(f'@user_list {user_list}'.encode())  # ارسال لیست کاربران به کلاینت
        except:
            print(f"Error sending user list")  # چاپ خطا

    def remove_client(self, username):
        """
        حذف کلاینت از لیست کلاینت ها.
        :param username: نام کاربری کلاینت.
        """
        if username in self.clients:  # اگر کلاینت در لیست وجود داشت
            del self.clients[username]  # حذف کلاینت از دیکشنری
            del self.client_ips[username] # حذف IP کلاینت از دیکشنری
            self.broadcast(f"{username} has left the chat.")  # ارسال پیام خروج به همه
            self.send_user_list()  # ارسال لیست کاربران آنلاین به همه

if __name__ == "__main__":
    server = ChatServer(HOST, PORT)  # ایجاد شیء از کلاس ChatServer
    server_thread = threading.Thread(target=server.start)  # ایجاد thread برای اجرای سرور
    server_thread.start()  # شروع thread سرور
