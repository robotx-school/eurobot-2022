import socket
import cv2
import numpy
import time
import terminal_color
import traceback


def connector():
    global sock
    # sock.close()
    connected = False
    while not connected:
        print(terminal_color.out_yellow("Connecting..."))
        try:
            sock.connect((IP, PORT))
            print(terminal_color.out_green("Connected"))
            connected = True
        except Exception:
            print(traceback.format_exc())
            print(terminal_color.out_red("Can't connect to NetServer"))
            time.sleep(2)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5.0)

IP = 'localhost'
PORT = 9093

connector()

#capture = cv2.VideoCapture(0)
while True:
    started = time.time()
    #ret, frame = capture.read()
    frame = cv2.imread("test.jpg")

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    result, imgencode = cv2.imencode('.jpg', frame, encode_param)
    data = numpy.array(imgencode)
    stringData = data.tostring()
    try:
        sock.send(str(len(stringData)).ljust(16).encode("utf-8"))
        print("Sending_0")
        sock.send(stringData)
        print("Sending_1")
    except BrokenPipeError:
        connector()
        continue
    data_recieved = False
    while not data_recieved:
        try:
            from_server = sock.recv(1024)
            print("Recv")
            if from_server:
                coords = from_server.decode("utf-8").split("|")
                print(coords)
            data_recieved = True
        except socket.timeout:
            print("Wait")
            time.sleep(1)
        except:
            time.sleep(5)
            connector()
            print("Reconnected")
            data_recieved = True
            break

    print("fps:", 1 / (time.time() - started))

sock.close()
