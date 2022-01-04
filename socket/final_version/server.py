import numpy as np
import cv2
import time
import socket
import pickle
import struct
import threading

#Cam setup
dims = (1280, 720)
cap = cv2.VideoCapture(0)
cap.set(3, dims[0])
cap.set(4, dims[1])

def worker(connection):
    #Thread for client
    global cap
    while True:
        try:
            while True: 
                ret, img = cap.read()
                img = cv2.resize(img,(512,512))
                img = np.array(img)
                data = pickle.dumps(np.array(img))
                connection.sendall(struct.pack("I", len(data)) + data)
                print(connection.recv(32))
        except ConnectionResetError:
            print('Соединение разорвано...',time.ctime())
            cap.release()
            break
        except ConnectionAbortedError:
            print('Соединение разорвано...',time.ctime())
            cap.release()
            break
        except:
            print('Соединение разорвано...',time.ctime())
            cap.release()
            break
        finally:
            print('Соединение разорвано...',time.ctime())
            cap.release()
            connection.close()
            sock.close()
            time.sleep(2)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('', 10006)
print('Старт сервера на {} порт {}'.format(*server_address))
sock.bind(server_address)
sock.listen(10)
while True:
    print('Ожидание соединения...',time.ctime())
    connection, client_address = sock.accept()
    print('Соединение установлено',time.ctime())
    threading.Thread(target=worker, args=(connection, )).start()

