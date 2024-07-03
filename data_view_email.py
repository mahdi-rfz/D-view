import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import time 
import datetime

import configs.config as config
import configs.email_config as email_config
import configs.user_token as user_token


def api_request():
    try :
        request = requests.post(config.api_url ,{"user_name":user_token.user_name , "token":user_token.token})
        response = request.text
        response = eval(response)

        return [response["name"], response["ipv4"] , response["time"] ,response["temp"] , 
                (response["loadavg"])["loadavg(15min)"] , (response["loadavg"])["loadavg(5min)"] ,
                (response["loadavg"])["loadavg(1min)"] ,
                (response["loadavg"])["process"] , (response["loadavg"])["last_process"] ,
                (response["uptime"])["uptime_day"] , (response["uptime"])["uptime_hour"] , (response["uptime"])["uptime_min"]]
    except Exception :
        return [None, None , None ,None , None , None , None , None , None , None , None , None]



def main():

    api_data = api_request()


    name = api_data[0]
    ip = api_data[1]
    
    uptime_day = api_data[9]
    uptime_hour = api_data[10]
    uptime_min = api_data[11]

    loadavg_15 = api_data[4]
    loadavg_5 = api_data[5]
    loadavg_1 = api_data[6]
    
    process = api_data[7]
    last_process = api_data[8]
    
    temp = api_data[3]
    sys_time = api_data[2]
    
    

    html_content = ("""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>D-view</title>

        <style>
    table, th, td {
    border: 2px solid #e0e1dd;
    border-collapse: collapse;
    }
    th, td {
    background-color: #8e9dae;
    }
    table {
    width: 100%;
    }
        </style>

    """) + (f"""    </head>
    <body>
        <center>
            <div >
            <h1>D-VIEW</h1>
            </div>
        </center>


        <center>
        <table>
            <tr>
                <th>Name</th>
                <td>{name}</td>
                <th>IP</th>
                <td>{ip}</td>
            </tr>

            <tr>
                <th>Uptime </th>
                <th>Day</th>
                <th>Hour</th>
                <th>Min</th>
            </tr>

            <tr>
                <th>UT</th>
                <td>{uptime_day}</td>
                <td>{uptime_hour}</td>
                <td>{uptime_min}</td>
                
            </tr>

            <tr>
                <th>Loadavg</th>
                <th>15min</th>
                <th>5min</th>
                <th>1min</th>
            </tr>
            
            <tr>
                <th>LA</th>
                <td>{loadavg_15}</td>
                <td>{loadavg_5}</td>
                <td>{loadavg_1}</td>
            </tr>

            <tr>
                <th>Process</th>
                <td>{process}</td>
                <th>Last Process</th>
                <td>{last_process}</td>
            </tr>

            <tr>
                <th>Temp</th>
                <td>{temp}</td>
                <th>Time</th>
                <td>{sys_time}</td>
            </tr>
        </table> 
        </center>

    </body>
    </html>""")
    
    
    send_email_html(f"D-view {ip}" , html_content , config.email)
    
    
    time.sleep(config.check_time * 60)
    main()




def system_time():
    cu = datetime.datetime.now()
    time = cu.strftime('%H:%M %p')
    return time



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
        print(f"sent {system_time()}")
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



main()