  # فاز اول:
#### این پروژه یک پروژه سوکت برای برقراری ارتباط سوکتی بین سرور و کلاینت است که توانایی ارسال و دریافت پیام‌های متنی را دارد.

<div dir='rtl'>
   فایل های پروژه: <br>
serverF1.py :سرور   <br>
clientF1.py : کالینت

  #### نحوه اجرای کد:
  * این کد ها در ترمینال اجرا می شوند.<br><br>
**سرور:**<br>
`python serverF1.py`<br>
سرور شروع به گوش دادن در آدرس IP و پورت مشخص شده می‌کند.<br>
پیام “Listening on 127.0.0.1 : 5000” نشان می‌دهد که سرور با موفقیت راه‌اندازی شده و منتظر اتصالات کلاینت‌ها است.<br><br>
**کلاینت:**<br>
`python clientF1.py`<br>
لاینت به سرور متصل می‌شود، پیام “hello server!” را ارسال می‌کند و منتظر دریافت پاسخ از سرور می‌ماند.<br>
پس از دریافت پاسخ از سرور، پیام “received: Hello client!” در خروجی کلاینت نمایش داده می‌شود و سپس اتصال بسته می‌شود.<br><br>

  #### توضیحات پیاده‌سازی کد: <br>
  **سرور:**<br>
1- ماژول socket وارد می‌شود.<br>
2- آدرس IP (HOST) و پورت (PORT) سرور تعریف می‌شوند.<br>
3- یک سوکت جدید ایجاد می‌شود و به آدرس IP و پورت مشخص شده متصل می‌شود.<br>
4- سرور شروع به گوش دادن به اتصالات ورودی می‌کند.<br>
5- وقتی یک کلاینت متصل می‌شود، اتصال پذیرفته می‌شود و یک سوکت جدید برای ارتباط با کلاینت ایجاد می‌شود.<br>
6- سرور منتظر دریافت پیام از کلاینت می‌ماند.<br>
7- وقتی یک پیام دریافت می‌شود، آن را چاپ می‌کند و یک پیام پاسخ به کلاینت ارسال می‌کند.<br>
8- این فرآیند تا زمانی که کلاینت اتصال را قطع کند، ادامه دارد.<br>
  
  **کلاینت:**<br>
1- ماژول socket وارد می‌شود.<br>
2- آدرس IP (HOST) و پورت (PORT) سرور تعریف می‌شوند.<br>
3-یک سوکت جدید ایجاد می‌شود و به سرور متصل می‌شود.<br>
4- یک پیام (“hello server!”) به سرور ارسال می‌شود.<br>
5- کلاینت منتظر دریافت پاسخ از سرور می‌ماند.<br>
6- وقتی یک پاسخ دریافت می‌شود، آن را چاپ می‌کند و اتصال را می‌بندد.<br><br>
  **اسکرین شات های فاز اول:**<br><br>
  ![Screenshot (117)](https://github.com/user-attachments/assets/31ccaa25-bb6a-4a44-a7e7-cfbfdfd6adba)
  ![Screenshot (118)](https://github.com/user-attachments/assets/55b0dde2-d661-4084-a1e1-02db35d0758e)
![Screenshot (119)](https://github.com/user-attachments/assets/71e9dfa8-3651-4853-b268-831e8c5dc238)


  ***
 # فاز دوم:
 #### این پروژه یک نمونه پیاده‌سازی از ارتباط بین کلاینت و سرور با استفاده از سوکت‌ها در پایتون است، با این تفاوت که سرور از قابلیت چندنخی بهره می‌برد تا بتواند به طور همزمان به چندین کلاینت پاسخ دهد.
 #### نحوه اجرای کد:
 **سرور:**<br>
 `python serverF2.py`<br><br>
 **کلاینت:**<br>
 `python clientF2.py`<br><br>
   #### توضیحات پیاده‌سازی کد: <br>
   `def client_handler(conn, addr):`<br>
    `print(f"Connect: {addr}")`<br>
    `while True:`<br>
        `data = conn.recv(1024)`<br>
        `if not data: break`<br>
        `print(f"Receive: {data.decode()}")`<br>
        `conn.sendall(f"Hello client!".encode())`<br>
    `print(f"Close: {addr}")`<br>
    `conn.close()`<br>
    <div dir='rtl'>
    این تابع در یک حلقه بی‌نهایت، پیام‌های دریافتی از کلاینت را دریافت و چاپ می‌کند، سپس یک پاسخ به کلاینت ارسال می‌کند.<br>
    اگر هیچ داده‌ای دریافت نشود، حلقه متوقف شده و اتصال بسته می‌شود.<br><br><br>
    </div>
     <div dir='ltr'>
    `with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:`<br>
    `s.bind((HOST, PORT))`<br>
    `s.listen()`<br>
    `print(f"Listen: {HOST}:{PORT}")`<br>
    `while True:`<br>
        `conn, addr = s.accept()`<br>
        `threading.Thread(target=client_handler, args=(conn, addr)).start()`<br>
        `print(f"New con. Active: {threading.active_count() - 1}")`<br>
         </div>
 سرور در یک حلقه بی‌نهایت منتظر اتصالات جدید می‌ماند.<br>
هر بار که یک اتصال جدید پذیرفته می‌شود، یک نخ جدید برای مدیریت آن اتصال ایجاد می‌شود.<br>
تعداد نخ‌های فعال (به جز نخ اصلی سرور) چاپ می‌شود تا نشان داده شود که سرور به طور همزمان در حال سرویس‌دهی به چند کلاینت است.<br><br>
 **اسکرین شات های فاز دوم:**<br><br>
![Screenshot (120)](https://github.com/user-attachments/assets/1be7f502-fe5f-4ce1-9cf1-32dd5794a230)
![Screenshot (121)](https://github.com/user-attachments/assets/65d3fdc1-061c-4a66-a818-3582a5ca6387)
![Screenshot (122)](https://github.com/user-attachments/assets/cd619585-70e9-4f96-8c3f-1d733fa90365)
![Screenshot (123)](https://github.com/user-attachments/assets/f95b8b2e-ca7c-4031-a5b0-c37c95284871)
![Screenshot (124)](https://github.com/user-attachments/assets/57eb4641-242f-48ac-ad21-4557e6f802b4)
 ***
 # فاز سوم:
 #### این پروژه یک چت گروهی ساده را با استفاده از سوکت‌ها در پایتون پیاده‌سازی می‌کند. در این چت، هر کاربری که به سرور متصل شود می‌تواند پیام‌های خود را برای سایر کاربران ارسال کند و پیام‌های دیگران را دریافت کند.
 #### نحوه اجرای کد:
 **سرور:**<br>
 `python serverF3.py`<br><br>
 **کلاینت:**<br>
 `python clientF3.py`<br><br>
  **اسکرین شات های فاز سوم:**<br><br>
  ![Screenshot (125)](https://github.com/user-attachments/assets/6d1b65e0-9af9-44bd-be3a-28a2e3abcb57)
  ![Screenshot (126)](https://github.com/user-attachments/assets/23d71168-f632-4f28-91d8-2d35cc917b29)
![Screenshot (128)](https://github.com/user-attachments/assets/f59391cb-1dac-4112-bc88-54da89a62f7a)
![Screenshot (132)](https://github.com/user-attachments/assets/0e3c4d73-0d48-4573-b7d1-4e1aa4f9e595)
![Screenshot (131)](https://github.com/user-attachments/assets/12770245-b367-4f66-9c2a-d8044678d3c2)


 ***
 # فاز چهارم:
 #### این پروژه یک چت گروهی پیشرفته‌تر با قابلیت ارسال پیام خصوصی بین کاربران و نمایش لیست کاربران آنلاین را پیاده‌سازی می‌کند. این پروژه از رابط کاربری گرافیکی (GUI) با استفاده از کتابخانه tkinter بهره می‌برد.
 #### نحوه اجرای کد:
 **سرور:**<br>
 `python server.py`<br><br>
 **کلاینت:**<br>
 `python client.py`<br><br>
  **اسکرین شات های فاز چهارم:**<br><br>
  ![Screenshot (133)](https://github.com/user-attachments/assets/5af7f106-c7b1-4870-a9cf-b75c441c860e)
![Screenshot (134)](https://github.com/user-attachments/assets/dd7b31be-dc2d-42d9-bba5-55ed185b3c10)
![Screenshot (135)](https://github.com/user-attachments/assets/2b744da6-85d1-4823-a51e-410bba209355)
![Screenshot (134)](https://github.com/user-attachments/assets/dd7b31be-dc2d-42d9-bba5-55ed185b3c10)
![Screenshot (135)](https://github.com/user-attachments/assets/2b744da6-85d1-4823-a51e-410bba209355)
![Screenshot (138)](https://github.com/user-attachments/assets/7e4b6b51-2795-49aa-9265-6efeb50ebafa)
![Screenshot (139)](https://github.com/user-attachments/assets/91ed1174-638c-4b4a-b078-31e8223cd091)


  </div>

