import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 8888))
s.listen(5)


client, addr = s.accept()


while True:
    command = input('Enter command: ')
    client.send(command.encode())
    if command.lower() == 'exit':
        break
    result_output = client.recv(4096).decode()
    print(result_output)


client.close()
s.close()