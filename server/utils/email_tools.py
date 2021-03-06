from typing import List
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import get_config_json

def send_email(recipients: List[str], subject:str, text_content:str, html_content:str):
    smtp_cfg = get_config_json("config.json")['smtp']

    msg = MIMEMultipart("alternative")
    msg['Subject'] = subject
    msg['From'] = smtp_cfg['sender']
    msg['To'] = ', '.join(recipients)

    text_part = MIMEText(text_content, "plain")
    html_part = MIMEText(html_content, "html")
    msg.attach(text_part)
    msg.attach(html_part)

    s = smtplib.SMTP(
        smtp_cfg['smtp_server'],
        smtp_cfg['smtp_port']
    )
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(smtp_cfg['login'], smtp_cfg['password'])
    s.send_message(msg)
    s.quit()
