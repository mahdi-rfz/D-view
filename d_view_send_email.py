import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests

import config
import email_config
import user_token



request = requests.post(config.api_url ,{"user_name":user_token.user_name , "token":user_token.token})
response = request.text

name = response["name"]
ipv4 = response["ipv4"]
time = response["time"]
temp = response["temp"]

loadavg15 = response["loadavg(15min)"]
loadavg5 = response["loadavg(5min)"]
loadavg1 = response["loadavg(1min)"]

process = response["process"]
last_process = response["last_process"]

uptime_day = response["uptime_day"]
uptime_hour = response["uptime_hour"]
uptime_min = response["uptime_min"]




def send_email_html(subject, html_content, receiver_email):
    from_email = email_config.email
    password = email_config.password
    
    smtp_server = "smtp.office365.com"
    smtp_port = 587
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, receiver_email, text)
        server.quit()
        print("sent")
    except Exception as e:
        print(f"eror: {e}")
    





def send_email_text(subject, body, receiver_email):
    from_email = email_config.email
    password = email_config.password

    smtp_server = "smtp.office365.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, receiver_email, text)
        server.quit()
        print("sent")
    except Exception as e:
        print(f"eror {e}")
