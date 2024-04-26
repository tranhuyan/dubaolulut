import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, receiver_email, subject, body, smtp_server="smtp-mail.outlook.com", smtp_port=587):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = ", ".join(receiver_email)

    message["Subject"] = subject
    # Nội dung email
    message.attach(MIMEText(body, "plain"))
    # Kết nối đến máy chủ SMTP
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    # Đăng nhập vào tài khoản email
    server.login(sender_email, sender_password)
    # Gửi email
    text = message.as_string()
    # server.sendmail(sender_email, receiver_email, text)
    server.sendmail(sender_email, receiver_email, text)
    # Đóng kết nối
    server.quit()
    print("Email sent successfully!")
