import socket
import time


def send_image(filename, socket):
    img = open(filename, 'rb')
    print(f'Sending: {img.name}')

    while True:
        data = img.read(4096)
        print(data)

        if not data:
            break

        socket.send(data)
        time.sleep(0.1)

    img.close()
    print(f'Sent: {img.name}')


def main():
    try:
        server = ('localhost', 8080)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                s.connect(server)
                print('Connected to {}:{}'.format(*server))

                send_image('transmitted.png', s)
                break

            except ConnectionRefusedError:
                print('No connection')
                time.sleep(5)
                pass

            except BrokenPipeError:
                print('Port was closed')
                time.sleep(10)

            except ConnectionResetError:
                print('Server was closed')
                time.sleep(3)

    except KeyboardInterrupt:
        print('\nClient exited')


if __name__ == '__main__':
    main()
