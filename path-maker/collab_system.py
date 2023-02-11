import socket
import threading

connected_clients = []
# Host
def host_client_waiter(sock):
    global connected_clients
    while True:
        connection, client_address = sock.accept()
        print(f"New client with {client_address}")
        connected_clients.append(connection)
        threading.Thread(target=connected_client_thread, args=(connection, )).start()

def connected_client_thread(connection):
    global connected_clients
    while True:
        data = connection.recv(1024)
        if data:
            print(data)
            broadcast(connected_clients, data, connection)

def broadcast(clients_list, data, sender):
    for conn in clients_list:
        if conn != sender:
            conn.send(data)

