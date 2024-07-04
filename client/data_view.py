import requests
from colorama import Fore 

import client_config

def text_art() :
    return """ █▀▄ ▄▀▄ ▀█▀ ▄▀▄    █ █ █ ██▀ █   █
 █▄▀ █▀█  █  █▀█ ▀▀ ▀▄▀ █ █▄▄ ▀▄▀▄▀
"""

def api_request():
    try :
        request = requests.post(client_config.api_url ,{"user_name":client_config.username , "token":client_config.token})
        response = request.text
        response = eval(response)
        

        return [response["name"], response["ipv4"] , response["time"] ,response["temp"] , 
                (response["loadavg"])["loadavg(15min)"] , (response["loadavg"])["loadavg(5min)"] ,
                (response["loadavg"])["loadavg(1min)"] ,
                (response["loadavg"])["process"] , (response["loadavg"])["last_process"] ,
                (response["uptime"])["uptime_day"] , (response["uptime"])["uptime_hour"] ,
                (response["uptime"])["uptime_min"]]
    except Exception :
        return [None, None , None ,None , None , None , None , None , None , None , None , None]
    
    
def main():
    print()
    api_data = api_request()
    
    print(text_art())
    
    print(f"Name : {Fore.LIGHTGREEN_EX + api_data[0] + Fore.WHITE} , IPv4 : {Fore.LIGHTGREEN_EX + api_data[1] + Fore.WHITE}")
    print(f"Loadavg (15min , 5min , 1min) : {Fore.LIGHTGREEN_EX + api_data[4] + Fore.WHITE} , {Fore.LIGHTGREEN_EX + api_data[5] + Fore.WHITE} , {Fore.LIGHTGREEN_EX + api_data[6] + Fore.WHITE}")
    print(f"Process : {Fore.LIGHTGREEN_EX + api_data[7] + Fore.WHITE} , Last process ID: {Fore.LIGHTGREEN_EX + api_data[8] + Fore.WHITE}")
    print(f"UPtime (day , hour , min) : {Fore.LIGHTGREEN_EX + str(api_data[9]) + Fore.WHITE} , {Fore.LIGHTGREEN_EX + str(api_data[10]) + Fore.WHITE} , {Fore.LIGHTGREEN_EX + str(api_data[11]) + Fore.WHITE}")
    print(f"Time : {Fore.LIGHTGREEN_EX + str(api_data[2]) + Fore.WHITE} , Temp : {Fore.LIGHTGREEN_EX + str(api_data[3]) + Fore.WHITE}")
    
main()