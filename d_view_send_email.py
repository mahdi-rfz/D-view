import requests

file = open("config.txt" , "r")
check_time = (eval(file.read()))["checktime"] #min 


file = open("config.txt" , "r")
url = (eval(file.read()))["api_url"]

file = open("user_token.txt" , "r")
user_token = eval(file.read())

request = requests.post(url , user_token)
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





def send_email(check_time):
    pass