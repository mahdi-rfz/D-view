from flask import Flask , request , jsonify


"""
read uptime on /proc/uptime file 
read system name on /etc/hostname
read loadavg on /proc/loadavg
read temp on (try find /sys -name temp and 
paste temp link in system_data_temp function)
"""

def system_data_uptime() : 
    read_uptime = open("/proc/uptime")
    raw_uptime = read_uptime.read()

    space_rm = raw_uptime.index(" ")
    uptime = raw_uptime[0:space_rm]
    
    uptime_day = ((float(uptime) / 60)/60)/24
    uptime_hour = (float(uptime) / 60)/60
    uptime_min = float(uptime) / 60
    
    return {"uptime_min" : uptime_min , "uptime_hour" : uptime_hour , "uptime_day" : uptime_day}




def system_data_system_name():
    read_name = open("/etc/hostname")
    system_name = read_name.read()
    
    f4edit = system_name.replace("\n" , "")
    
    return {"name" : f4edit}


def system_data_loadavg():
    read_loadavg = open("/proc/loadavg")
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
    
    return {"loadavg(1min)":finall_output[0] ,
            "loadavg(5min)":finall_output[1] ,
            "loadavg(15min)":finall_output[2] ,
            "process":finall_output[3] ,
            "last_process":finall_output[4]}


def system_data_temp():
    try :
        read_temp = open("/sys/devices/virtual/thermal/thermal_zone0/temp")
        temp = read_temp.read()
        temp = int(temp)
    except Exception:
        temp = False
    
    return {"temp":temp}



app = Flask(__name__)




@app.route('/data_view', methods=['POST'])
def data_view():
    if "user_name" not in request.form and "token" not in request.form:
        return jsonify({"Eror": "Your request format is incorrect(use user name and token)"}), 400
    
    file = open("user_token.txt" , "r")
    eval_file = eval(file.read())
    


    
    data = {"name":(system_data_system_name())["name"] ,
        "uptime":system_data_uptime() ,
        "loadavg":system_data_loadavg() ,
        "temp": (system_data_temp())["temp"]}
    
    if request.form["user_name"] == eval_file["user_name"] and request.form["token"] == eval_file["token"] :
        return jsonify(data)
    else :
        return False
    
    
    
    
if __name__ == ("__main__") :
    app.run(port="9887" , debug=True)