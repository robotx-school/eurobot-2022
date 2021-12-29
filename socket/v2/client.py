import socket
import time

while True:
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address1 = ('192.168.0.168', 8080)
    # print('Подключено к {} порт {}'.format(*server_address1))
    try:
        sock1.connect(server_address1)
        while 1:
            image_result = open("image2.png", "rb")
            while True:
                string = image_result.read(512)
                print(string)
                if not string:
                    break
                sock1.send(string)
            image_result.close()
            # mess = [1, 2, 2, 3, 3, 3]
            # mess = str(mess)
            # message = pickle.dumps(image_result)
            # sock1.sendall(message)
            print(f'Отправка: {image_result}')
            # data_string = pickle.dumps()
            # sock1.send(data_string)
            print("wait recieve")
            data = sock1.recv(32)
            print("recieve:", data)
            time.sleep(3)
    except ConnectionRefusedError:
        print("no connection")
        time.sleep(5)
    except BrokenPipeError:
        print("port was closed")
        time.sleep(10)
    except ConnectionResetError:
        print("virubili")
        time.sleep(3)
