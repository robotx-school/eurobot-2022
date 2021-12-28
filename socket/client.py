from ctypes import sizeof
from os import extsep
import socket
import sys
import time, cv2
import numpy as np

def encode_image(image):
    stringData = str(image.tolist()).encode("utf-8")
    return stringData
    
    

def group(iterable, count): 
    return zip(*[iter(iterable)] * count)

def out_red(text):
    return "\033[31m {}" .format(text)
def out_yellow(text):
    return "\033[33m {}" .format(text)
def out_green(text):
    return "\033[32m {}" .format(text)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.0.125', 10001)
print(f'Подключено к {server_address[0]} порт {server_address[1]}')

attempts = 0
connected = False
while not connected:
    print(out_yellow("Connecting..."))
    try:
        sock.connect(server_address)
        print(out_green("Connected"))
        connected = True
    except ConnectionRefusedError:
        print(out_red("Can't connect to server"))
        time.sleep(2)

#mess = [1, 2, 2, 3, 3, 3]
#mess = str(mess)
#print(f'Отправка: {mess}')
#message = mess.encode()
img = cv2.imread("small.jpg")
message = encode_image(img)
#message 
try:
    sock.sendall(message[])
except:
    print("Error")


amount_received = 0
amount_expected = len(message)
while amount_received < amount_expected:
    data = sock.recv(1024)
    amount_received += len(data)
    mess = data.decode()
    print(f'Получено: {data.decode()}')

print('Закрываем сокет')
sock.close()
