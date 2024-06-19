import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import logging


def log_message(message):
    logging.info(message)


def send_email(smtp_server, sender_email, sender_password, receiver_email, subject, content, attachment_path=None):
    """
    发送邮件
    :param smtp_server:
    :param sender_email:
    :param sender_password:
    :param receiver_email:
    :param subject:
    :param content:
    :return:
    """

    # 创建一个SMTP客户端
    client = smtplib.SMTP(smtp_server)

    # 启动TLS模式
    client.starttls()

    # 登录到邮箱
    try:
        client.login(sender_email, sender_password)
        log_message("Email Login successful.")
    except smtplib.SMTPAuthenticationError:
        log_message("Failed to login. Please check your email and password. Use SMTP authorization code.")

    # 创建一封邮件
    message = MIMEMultipart()
    # message['From'] = Header(sender_email, 'utf-8')
    # qq邮箱 不需要 utf-8
    message['From'] = Header(sender_email)
    message['To'] = Header(receiver_email, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    message.attach(MIMEText(content, 'plain', 'utf-8'))

    # 如果有附件路径，添加附件
    if attachment_path is not None:
        with open(attachment_path, 'rb') as f:
            # 创建一个MIMEBase对象，并设置相关属性
            mime = MIMEBase('image', 'png', filename='screenshot.png')
            mime.add_header('Content-Disposition', 'attachment', filename='screenshot.png')
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 读取附件内容并添加到MIMEBase对象
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            message.attach(mime)

    # 发送邮件
    client.sendmail(sender_email, [receiver_email], message.as_string())
    log_message("Email sent.")

    # 关闭SMTP客户端
    client.quit()
