from flask import Flask , request , jsonify #v3.3
import requests #v2.31.0
import datetime 
import configs.user_token as user_token

from configs import config


"""
read uptime on /proc/uptime file 
read system name on /etc/hostname
read loadavg on /proc/loadavg
read temp on (try find /sys -name temp and 
paste temp link in system_data_temp function)
"""

def system_data_uptime() : 
    try :
        read_uptime = open("/proc/uptime") #uptime in linux on /proc/uptime file
        raw_uptime = read_uptime.read()

        space_rm = raw_uptime.index(" ")
        uptime = raw_uptime[0:space_rm]
        
        uptime_day = ((float(uptime) / 60)/60)/24
        uptime_hour = (float(uptime) / 60)/60
        uptime_min = float(uptime) / 60
        
    except Exception :
        uptime_day = "Not found"
        uptime_hour = "Not found"
        uptime_min = "Not found"
    
    return {"uptime_min" : uptime_min , "uptime_hour" : uptime_hour , "uptime_day" : uptime_day}




def system_data_system_name():
    try :
        read_name = open("/etc/hostname")#hostname in linux on /etc/hostname file
        system_name = read_name.read()
        
        f4edit = system_name.replace("\n" , "")
    except Exception :
        f4edit = "Not found"
    
    return {"name" : f4edit}




def system_data_loadavg():
    try :
        read_loadavg = open("/proc/loadavg")#loadavg in linux on /proc/loadavg file
        loadavg = read_loadavg.read()

        counter = (0)

        middle = ("")
        finall_output = []
        while True :
            memory = loadavg[counter]
            if memory != " ":
                middle = middle + memory
                counter = counter + 1
            else :
                finall_output.append(middle)
                middle = ("")
                counter = counter + 1

            if counter == len(loadavg) :
                finall_output.append(middle)
                break

        f4edit = finall_output[4]
        f4edit = f4edit.replace("\n" , "")
        finall_output[4] = f4edit
        
    except Exception :
        finall_output = ["Not found" , "Not found" , "Not found" , "Not found" , "Not found"]
    
    return {"loadavg(1min)":finall_output[0] ,
            "loadavg(5min)":finall_output[1] ,
            "loadavg(15min)":finall_output[2] ,
            "process":finall_output[3] ,
            "last_process":finall_output[4]}



"""
import temp address file for use read in file because temp 
file address is difrent on other system for edit temp address 
go on configs/config.py
"""
def system_data_temp():
    try :
        read_temp = open(config.temp_file_address) 
        temp = read_temp.read()
        temp = int(temp)
    except Exception:
        temp = " Not found" 
    
    return {"temp":temp}





def system_data_ip():
    try :
        request_url = 'https://geolocation-db.com/jsonp/' #use geolocation for pubic ipv4
        response = requests.get(request_url)
        response = response.text
        response = response.replace("callback(" , "")
        response = response.replace(")" , "")
        response = response.replace("null" , "False")
        
        return (eval(response))["IPv4"]
    
    except OSError as e :
        return " Not found" 




def system_data_time():
    cu = datetime.datetime.now()
    time = cu.strftime('%H:%M %p')
    return time



app = Flask(__name__)


"""
for edit api username and password go on /configs/user_token.py 
im set default username and password :
username = user
token = ealkcjveafgDAtg
use this user name and pasword for request to api on internet
"""

#eror 400 : request format is incorrect
#eror 401 : Username or token is incorrect


@app.route('/d_view', methods=['POST'])
def data_view():
    if "user_name" not in request.form and "token" not in request.form:
        return jsonify({"Eror": "Your request format is incorrect(use user name and token)"}), 400
    

    data = {"name":(system_data_system_name())["name"] ,
        "uptime":system_data_uptime() ,
        "loadavg":system_data_loadavg() ,
        "temp": (system_data_temp())["temp"], 
        "ipv4":system_data_ip() ,
        "time":system_data_time()}
    
    if request.form["user_name"] == user_token.user_name and request.form["token"] == user_token.token :
        return (jsonify(data))
    else :
        return [("Username or token is incorrect") , 401 ]
    
    
    
if __name__ == ("__main__") :
    app.run(port="9887" , debug=True)