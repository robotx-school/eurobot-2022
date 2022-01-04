import socket
import numpy as np
from _thread import start_new_thread


def threaded(c):
    img = open('received.png', 'wb')

    while True:
        data = c.recv(4096)
        print(data)
        if not data:
            break

        img.write(data)

    img.close()
    c.close()
    print(f'Saved: {img}{type(img)}')


def main():
    server = ('localhost', 8080)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(server)
    print('Created server on {}:{}'.format(*server))
    s.listen(5)
    print('Listening...')

    try:
        while True:
            sock, addr = s.accept()
            print('Connected to :', addr[0], ':', addr[1])
            start_new_thread(threaded, (sock,))

    except KeyboardInterrupt:
        print('\nServer closed')


if __name__ == '__main__':
    main()
