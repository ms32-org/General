import requests

exe = requests.get("https://raw.githubusercontent.com/ms32-org/maksadPura/refs/heads/main/RunAsTI.zip")
with open("lol.zip","wb") as file:
    file.write(exe.content)