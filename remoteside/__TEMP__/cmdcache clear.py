from requests import post

res = post("https://ms32-sha2.onrender.com/command",json={"user":"103W"})
print(res.content)
while not "none" in res.content.decode('utf-8'):
    res = post("https://ms32-sha2.onrender.com/command",json={"user":"103W"})
    print(res.content)
print("cache cleared, ready for development")