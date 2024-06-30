from flask import Flask , request , jsonify

def system_data():
    read_name = open("/etc/hostname")
    system_name = read_name.read()
    
    read_temp = open("")
    temp = read_temp()
    
    read_uptime = open("/proc/uptime")
    uptime = read_uptime.read()
    uptime_day = ((int(uptime) / 60)/60)/24
    uptime_hour = (int(uptime) / 60)/60
    uptime_min = int(uptime) / 60
    
    read_loadavg = open("/proc/loadavg")
    loadavg = read_loadavg.read()

    return system_name , uptime , loadavg


app = Flask(__name__)



@app.route('/data_view', methods=['POST'])
def data_view():
    if "user_name" not in request.form and "token" not in request.form:
        return jsonify({"Eror": "Your request format is incorrect(use user name and token)"}), 400
    
    file = open("user_token.txt" , "r")
    eval_file = eval(file.read())
    
    
    data = system_data()
    
    if request.form["user_name"] == eval_file["user_name"] and request.form["token"] == eval_file["token"] :
        return jsonify(data)
    else :
        return False
    
    
    
    
if __name__ == ("__main__") :
    app.run(port="9887" , debug=True)