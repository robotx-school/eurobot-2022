import threading
import port_killer
import time
import net
import socket
import cv2
import numpy
import terminal_color

SERVER_PORT = 9093
LOCAL_RUN = False

# Linux
# При запуске клиента на другом компе
if not LOCAL_RUN:
    port_killer.KillPort(SERVER_PORT)

time.sleep(3)


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf:
            return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def client_worker(conn):
    while True:
        length = recvall(conn, 16)
        stringData = recvall(conn, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg = cv2.imdecode(data, 1)
        img, _ = net.get_colored_img(decimg)
        #cv2.imwrite("RES.jpg", img)
        # Что - то происходит
        x = 5
        y = 5
        fake_coords = str(x) + "|" + str(y)
        dt = str(fake_coords).encode("utf-8")
        conn.send(dt)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("", SERVER_PORT))
s.listen(True)
print(terminal_color.out_green(f"NetServer started on port {SERVER_PORT}"))
while True:
    conn, addr = s.accept()
    threading.Thread(target=client_worker, args=(conn, )).start()

s.close()
