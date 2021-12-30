import socket
from _thread import start_new_thread

def threaded(c):
    fp = open('received.png','wb')
    while True:
        data = c.recv(512)
        print(data)
        if not data:
            break
        fp.write(data)
    fp.close()
    c.close()
    print('done')
 
host = '192.168.0.168'
port = 8080
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host, port))
s.listen(5)
try:
    while True:
        sock, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (sock,))

except KeyboardInterrupt:
    print('\nServer closed')
