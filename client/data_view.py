import requests
import colorama

import client_config

def text_art() :
    return """ █▀▄ ▄▀▄ ▀█▀ ▄▀▄    █ █ █ ██▀ █   █
 █▄▀ █▀█  █  █▀█ ▀▀ ▀▄▀ █ █▄▄ ▀▄▀▄▀
"""

def api_request():
    # try :
        request = requests.post(client_config.api_url ,{"user_name":client_config.username , "token":client_config.token})
        response = request.text
        response = eval(response)

        return [response["name"], response["ipv4"] , response["time"] ,response["temp"] , 
                (response["loadavg"])["loadavg(15min)"] , (response["loadavg"])["loadavg(5min)"] ,
                (response["loadavg"])["loadavg(1min)"] ,
                (response["loadavg"])["process"] , (response["loadavg"])["last_process"] ,
                (response["uptime"])["uptime_day"] , (response["uptime"])["uptime_hour"] , (response["uptime"])["uptime_min"]]
    # except Exception :
    #     return [None, None , None ,None , None , None , None , None , None , None , None , None]
    
    
print(api_request())